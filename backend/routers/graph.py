from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import json
import os

router = APIRouter(prefix="/api", tags=["Knowledge Graph"])

DATA_PATH = os.path.join("data", "courses.json")

class CourseCreate(BaseModel):
    course_id: str
    title: str
    specialization: str
    prerequisites: List[str]
    technical_skills: List[str]
    synopsis: Optional[str] = ""
    credits: Optional[int] = 3

class CourseUpdate(BaseModel):
    title: str
    specialization: str
    technical_skills: List[str]

@router.get("/graph")
def get_graph_data():
    """Fetches the complete JSON knowledge graph for the D3.js frontend."""
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r") as f:
            return json.load(f)
    return {"error": "Data file not found"}

@router.post("/courses")
async def add_course(course: CourseCreate):
    """Manually adds a single course to the JSON database."""
    try:
        with open(DATA_PATH, 'r') as f:
            data = json.load(f)
        
        data.append(course.dict())
        
        with open(DATA_PATH, 'w') as f:
            json.dump(data, f, indent=4)
            
        return {"message": "Course added successfully", "course": course}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/courses/{course_id}")
async def update_course(course_id: str, update_data: CourseUpdate):
    """Updates an existing course node in the knowledge graph."""
    if not os.path.exists(DATA_PATH):
        raise HTTPException(status_code=404, detail="Curriculum data not found.")

    with open(DATA_PATH, "r") as f:
        courses = json.load(f)

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

    with open(DATA_PATH, "w") as f:
        json.dump(courses, f, indent=4)

    return {"message": f"Successfully updated {course_id}"}