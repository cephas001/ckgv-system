import json
import os
from nlp_processor import CurriculumParser # Import the class we built!

# --- DYNAMIC PATH RESOLUTION ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR)
DATA_DIR = os.path.join(BASE_DIR, "data")

RAW_DATA_PATH = os.path.join(DATA_DIR, "raw_courses.json")
ACTIVE_DB_PATH = os.path.join(DATA_DIR, "courses.json") 

def run_ontology_ner():
    # 1. Initialize our single source of truth parser
    parser = CurriculumParser()

    # 2. Load the raw data
    try:
        with open(RAW_DATA_PATH, "r") as f:
            courses = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: {RAW_DATA_PATH} not found. Ensure raw data is present.")
        return
        
    print(f"AI Engine Armed! Scanning {len(courses)} courses...\n")
    
    # 3. Process each course
    for course in courses:
        synopsis = course.get("synopsis", "")
        
        # Let the CurriculumParser handle the heavy lifting
        metadata = parser.extract_metadata(synopsis)
        
        course["technical_skills"] = metadata["extracted_skills"]
        course["specialization"] = metadata["suggested_specialization"]
        
        # Ensure prerequisites exist
        if "prerequisites" not in course:
            course["prerequisites"] = []
        
        print(f"[{course.get('course_id', 'N/A')}] {course.get('title', 'Unknown Title')}")
        print(f"  -> Skills: {course['technical_skills']}")
        print(f"  -> Track:  {course['specialization']}\n")

    # 4. Save to the active backend database
    with open(ACTIVE_DB_PATH, "w") as f:
        json.dump(courses, f, indent=4)
        
    print(f"SUCCESS: Knowledge Graph Database successfully built at {ACTIVE_DB_PATH}")

if __name__ == "__main__":
    run_ontology_ner()