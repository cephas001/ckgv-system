from fastapi import FastAPI, HTTPException, UploadFile, File, Depends, status
from fastapi.middleware.cors import CORSMiddleware 
from pydantic import BaseModel 
from typing import List, Optional 
from nlp_processor import CurriculumParser
from io import StringIO
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from models import AdminUser
from pydantic import BaseModel
import shutil
import csv
import json
import os 

DATA_PATH = os.path.join("data", "courses.json")

app = FastAPI()
parser = CurriculumParser()

# --- JWT CONFIGURATION ---
SECRET_KEY = "mcpherson_ckgv_secret_key_2026"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class LoginRequest(BaseModel):
    username: str
    password: str

# --- AUTHENTICATION ENDPOINT ---
@app.post("/api/auth/login")
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    # 1. Search for the user in the PostgreSQL Database
    result = await db.execute(select(AdminUser).where(AdminUser.Username == request.username))
    user = result.scalars().first()

    # 2. Verify user exists and password matches
    if not user or not pwd_context.verify(request.password, user.PasswordHash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    # 3. Generate a secure JWT Token
    expiration = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data = {"sub": user.Username, "role": user.Role, "exp": expiration}
    access_token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": access_token, "token_type": "bearer"}

# Create a Schema for the incoming course
class CourseCreate(BaseModel):
    course_id: str
    title: str
    specialization: str
    prerequisites: List[str]
    technical_skills: List[str]
    synopsis: Optional[str] = ""
    credits: Optional[int] = 3

# CRITICAL: Allows the Frontend (Nuxt) to talk to the Backend (FastAPI)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, change this to your specific URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "CKGV API is running"}

@app.get("/api/graph")
def get_graph_data():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r") as f:
            return json.load(f)
    return {"error": "Data file not found"}

@app.post("/api/courses")
async def add_course(course: CourseCreate):
    # 1. Load your existing data file
    # Replace 'courses.json' with whatever your data source file name is
    try:
        with open('data/courses.json', 'r') as f:
            data = json.load(f)
        
        # 2. Add the new course
        data.append(course.dict())
        
        # 3. Save it back
        with open('data/courses.json', 'w') as f:
            json.dump(data, f, indent=4)
            
        return {"message": "Course added successfully", "course": course}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/api/nlp/analyze")
async def analyze_course_description(payload: dict):
    # The payload will contain {"description": "..."}
    text = payload.get("description", "")
    if not text:
        raise HTTPException(status_code=400, detail="No text provided")
    
    results = parser.extract_metadata(text)
    print(results)
    return results

@app.post("/api/courses/bulk")
async def bulk_import_courses(file: UploadFile = File(...)):
    # Check if it's a CSV
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported for bulk import.")

    # --- STEP 1: ARCHIVE CURRENT DATA ---
    db_path = 'data/courses.json'
    archive_dir = 'data/archive'
    
    # Create archive folder if it doesn't exist
    os.makedirs(archive_dir, exist_ok=True)
    
    # If we have existing data, back it up with a timestamp
    if os.path.exists(db_path):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_path = os.path.join(archive_dir, f"courses_backup_{timestamp}.json")
        shutil.copy2(db_path, archive_path)

    # --- STEP 2: READ THE UPLOADED CSV ---
    content = await file.read()
    # Decode the bytes to a string
    decoded_content = content.decode('utf-8')
    csv_reader = csv.DictReader(StringIO(decoded_content))
    
    new_courses = []
    
    # --- STEP 3: RUN THE NLP PIPELINE ---
    for row in csv_reader:
        # We expect the CSV to have headers: course_id, title, credits, synopsis
        course_id = row.get('course_id', '').strip()
        title = row.get('title', '').strip()
        credits_str = row.get('credits', '3')
        synopsis = row.get('synopsis', '').strip()
        
        if not course_id or not title:
            continue # Skip empty rows
            
        # Run the AI on the synopsis!
        nlp_results = parser.extract_metadata(synopsis)
        
        # Format the course object
        course_data = {
            "course_id": course_id,
            "title": title,
            "credits": int(credits_str) if credits_str.isdigit() else 3,
            "specialization": nlp_results["suggested_specialization"],
            "technical_skills": nlp_results["extracted_skills"],
            "prerequisites": [], # Can be added to CSV later if needed
            "synopsis": synopsis
        }
        new_courses.append(course_data)

    # --- STEP 4: SAVE THE NEW KNOWLEDGE GRAPH ---
    # (Note: This overwrites the old DB. If you want to merge, you'd load the old DB first and append)
    try:
        with open(db_path, 'w') as f:
            json.dump(new_courses, f, indent=4)
        return {
            "status": "success", 
            "message": f"Successfully processed and imported {len(new_courses)} courses.",
            "archived_to": f"courses_backup_{timestamp}.json" if os.path.exists(db_path) else "No previous data to archive."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database Write Error: {str(e)}")