from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
import csv
import json
import os
import shutil
import time
from io import StringIO

from core.database import get_db
from models.domain import AuditLog
from services.nlp_processor import CurriculumParser

router = APIRouter(prefix="/api", tags=["NLP Extraction & Upload"])
parser = CurriculumParser()
DATA_PATH = os.path.join("data", "courses.json")

class ValidatedCourse(BaseModel):
    course_id: str
    title: str
    specialization: Optional[str] = "Core Computer Science"
    technical_skills: List[str]
    synopsis: Optional[str] = ""
    credits: Optional[int] = 3
    prerequisites: Optional[List[str]] = []

class CommitRequest(BaseModel):
    courses: List[ValidatedCourse]
    import_mode: str = "update"

@router.post("/nlp/analyze")
async def analyze_course_description(payload: dict):
    """Runs a single string of text through the spaCy NLP pipeline."""
    text = payload.get("description", "")
    if not text:
        raise HTTPException(status_code=400, detail="No text provided")
    
    results = parser.extract_metadata(text)
    return results

@router.post("/upload/preview")
async def preview_curriculum_data(file: UploadFile = File(...)):
    """Processes a bulk CSV file through the NLP pipeline and returns a preview."""
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
            
        nlp_results = parser.extract_metadata(synopsis)
        
        course_data = {
            "course_id": course_id,
            "title": title,
            "credits": int(credits_str) if credits_str.isdigit() else 3,
            "specialization": nlp_results.get("suggested_specialization", ""),
            "technical_skills": nlp_results.get("extracted_skills", []),
            "prerequisites": [],
            "synopsis": synopsis
        }
        extracted_courses.append(course_data)
        
    return {"extracted_courses": extracted_courses}

@router.post("/upload/commit")
async def commit_curriculum_data(request: CommitRequest, db: AsyncSession = Depends(get_db)):
    """Securely commits the validated preview data into the JSON graph database."""
    archive_dir = "data/archive"
    
    # 1. HANDLE ARCHIVING
    if request.import_mode == "overwrite" and os.path.exists(DATA_PATH):
        os.makedirs(archive_dir, exist_ok=True)
        timestamp = int(time.time())
        archive_path = os.path.join(archive_dir, f"courses_archive_{timestamp}.json")
        shutil.copy(DATA_PATH, archive_path)
    
    # 2. LOAD EXISTING
    existing_courses = []
    if request.import_mode == "update" and os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r") as f:
            existing_courses = json.load(f)

    # 3. MERGE OR OVERWRITE
    if request.import_mode == "overwrite":
        existing_courses = [course.dict() for course in request.courses]
    else:
        existing_ids = {c.get('course_id'): i for i, c in enumerate(existing_courses)}
        for new_course in request.courses:
            course_dict = new_course.dict()
            if course_dict['course_id'] in existing_ids:
                idx = existing_ids[course_dict['course_id']]
                existing_courses[idx].update(course_dict)
            else:
                existing_courses.append(course_dict)
            
    # 4. SAVE
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, "w") as f:
        json.dump(existing_courses, f, indent=4)
        
    # 5. AUDIT LOGGING
    try:
        action_type = "BULK_OVERWRITE_GRAPH" if request.import_mode == "overwrite" else "BULK_UPDATE_GRAPH"
        # Using AdminID 1 as a placeholder for the system/current admin
        new_log = AuditLog(AdminID=1, ActionType=action_type) 
        db.add(new_log)
        await db.commit()
    except Exception as e:
        print(f"Failed to write audit log: {e}")

    return {"message": f"Successfully committed data in '{request.import_mode}' mode!"}