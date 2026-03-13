import spacy
import json
import os

# We read raw data, but now save to our active Database file
RAW_DATA_PATH = os.path.join("data", "raw_courses.json")
ACTIVE_DB_PATH = os.path.join("data", "courses.json") 
ONTOLOGY_PATH = os.path.join("data", "ontology.json")

def run_ontology_ner():
    print("Initializing spaCy NLP Engine with Centralized Ontology...")
    nlp = spacy.load("en_core_web_md") # Changed to _md to match processor
    ruler = nlp.add_pipe("entity_ruler", before="ner")
    
    # --- LOAD THE CENTRALIZED ONTOLOGY ---
    try:
        with open(ONTOLOGY_PATH, "r") as f:
            cs_ontology = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: {ONTOLOGY_PATH} not found.")
        return

    patterns = []
    for specialization, skills in cs_ontology.items():
        for skill in skills:
            patterns.append({"label": specialization, "pattern": [{"LOWER": word.lower()} for word in skill.split()]})
            
    ruler.add_patterns(patterns)

    # Load the raw PDF data
    try:
        with open(RAW_DATA_PATH, "r") as f:
            courses = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: {RAW_DATA_PATH} not found. Ensure raw data is present.")
        return
        
    print(f"AI Engine Armed! Scanning {len(courses)} courses...\n")
    
    for course in courses:
        synopsis = course.get("synopsis", "")
        extracted_skills = []
        specialization_scores = {spec: 0 for spec in cs_ontology.keys()}
        
        if synopsis:
            doc = nlp(synopsis)
            for ent in doc.ents:
                if ent.label_ in cs_ontology:
                    # Use Title Case for consistency
                    clean_skill = ent.text.title()
                    if clean_skill not in extracted_skills:
                        extracted_skills.append(clean_skill)
                    specialization_scores[ent.label_] += 1
                    
        assigned_specialization = "Core Computer Science"
        highest_score = 0
        for spec, score in specialization_scores.items():
            if score > highest_score:
                highest_score = score
                assigned_specialization = spec

        course["technical_skills"] = extracted_skills
        course["specialization"] = assigned_specialization
        # Ensure prerequisites exist
        if "prerequisites" not in course:
            course["prerequisites"] = []
        
        print(f"[{course['course_id']}] {course['title']}")
        print(f"  -> Skills: {course['technical_skills']}")
        print(f"  -> Track:  {course['specialization']}\n")

    # Save to the active backend database!
    with open(ACTIVE_DB_PATH, "w") as f:
        json.dump(courses, f, indent=4)
        
    print(f"SUCCESS: Knowledge Graph Database successfully built at {ACTIVE_DB_PATH}")

if __name__ == "__main__":
    run_ontology_ner()