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
from models import AdminUser, AuditLog
from pydantic import BaseModel
import shutil
import csv
import json
import os 
import io
import time

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

# --- NEW: WRITE TO AUDIT LOG ---
    new_log = AuditLog(AdminID=user.AdminID, ActionType="ADMIN_LOGIN")
    db.add(new_log)
    await db.commit()

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

# 1. Define the expected data structure from the frontend
class CourseUpdate(BaseModel):
    title: str
    specialization: str
    technical_skills: List[str]

# 2. The Update Endpoint
@app.put("/api/courses/{course_id}")
async def update_course(course_id: str, update_data: CourseUpdate):
    # Path to your JSON data (adjust if your folder structure is slightly different)
    file_path = "data/courses.json" 
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Curriculum data not found.")

    # Read the current graph data
    with open(file_path, "r") as f:
        courses = json.load(f)

    # Find the course and apply the updates
    course_found = False
    for course in courses:
        if course.get("course_id") == course_id:
            course["title"] = update_data.title
            course["specialization"] = update_data.specialization
            course["technical_skills"] = update_data.technical_skills
            course_found = True
            break

    if not course_found:
        raise HTTPException(status_code=404, detail="Course not found in database.")

    # Save the updated data back to the JSON file
    with open(file_path, "w") as f:
        json.dump(courses, f, indent=4)

    return {"message": f"Successfully updated {course_id}"}

# --- PYDANTIC MODELS FOR VALIDATION ---
class ValidatedCourse(BaseModel):
    course_id: str
    title: str
    specialization: Optional[str] = "Core Computer Science"
    technical_skills: List[str]
    # Add any other fields your JSON graph uses (credits, prerequisites, etc.)

class CommitRequest(BaseModel):
    courses: List[ValidatedCourse]
    import_mode: str = "update" # Defaults to update, can be "overwrite"

# --- STEP 1: THE AI PREVIEW ENDPOINT ---
@app.post("/api/upload/preview")
async def preview_curriculum_data(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported.")
    
    content = await file.read()
    decoded_content = content.decode('utf-8')
    csv_reader = csv.DictReader(StringIO(decoded_content))
    
    extracted_courses = []
    
    for row in csv_reader:
        course_id = row.get('course_id', '').strip()
        title = row.get('title', '').strip()
        credits_str = row.get('credits', '3')
        synopsis = row.get('synopsis', '').strip()
        
        if not course_id or not title:
            continue
            
        # --- YOUR ACTUAL AI PARSER LOGIC ---
        nlp_results = parser.extract_metadata(synopsis)
        
        course_data = {
            "course_id": course_id,
            "title": title,
            "credits": int(credits_str) if credits_str.isdigit() else 3,
            "specialization": nlp_results["suggested_specialization"],
            "technical_skills": nlp_results["extracted_skills"],
            "prerequisites": [],
            "synopsis": synopsis
        }
        extracted_courses.append(course_data)
        
    # Return it to the frontend for Admin Validation!
    return {"extracted_courses": extracted_courses}


# --- STEP 2: THE SECURE COMMIT ENDPOINT ---
@app.post("/api/upload/commit")
async def commit_curriculum_data(request: CommitRequest, db: AsyncSession = Depends(get_db)):
    file_path = "data/courses.json"
    archive_dir = "data/archive"
    
    # 1. HANDLE ARCHIVING IF OVERWRITING
    if request.import_mode == "overwrite" and os.path.exists(file_path):
        os.makedirs(archive_dir, exist_ok=True)
        timestamp = int(time.time())
        archive_path = os.path.join(archive_dir, f"courses_archive_{timestamp}.json")
        shutil.copy(file_path, archive_path)
    
    # 2. LOAD EXISTING OR START FRESH
    existing_courses = []
    if request.import_mode == "update" and os.path.exists(file_path):
        with open(file_path, "r") as f:
            existing_courses = json.load(f)

    # 3. MERGE OR OVERWRITE DATA
    if request.import_mode == "overwrite":
        # If overwrite, the new graph is strictly what was just validated
        existing_courses = [course.dict() for course in request.courses]
    else:
        # If update, perform the dictionary merge we built earlier
        existing_ids = {c.get('course_id'): i for i, c in enumerate(existing_courses)}
        for new_course in request.courses:
            course_dict = new_course.dict()
            if course_dict['course_id'] in existing_ids:
                idx = existing_ids[course_dict['course_id']]
                existing_courses[idx].update(course_dict)
            else:
                existing_courses.append(course_dict)
            
    # 4. SAVE THE GRAPH
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        json.dump(existing_courses, f, indent=4)
        
    # 5. AUDIT LOGGING
    try:
        action_type = "BULK_OVERWRITE_GRAPH" if request.import_mode == "overwrite" else "BULK_UPDATE_GRAPH"
        new_log = AuditLog(AdminID=1, ActionType=action_type)
        db.add(new_log)
        await db.commit()
    except Exception as e:
        print(f"Failed to write audit log: {e}")

    return {"message": f"Successfully committed data in '{request.import_mode}' mode!"}