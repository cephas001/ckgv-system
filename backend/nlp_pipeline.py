import spacy
import json
import os

RAW_DATA_PATH = os.path.join("data", "raw_courses.json")
FINAL_GRAPH_PATH = os.path.join("data", "final_graph_data.json")

# 1. THE ONTOLOGY (The Dictionary of Truth)
# We map exactly what skills belong to what specialization.
CS_ONTOLOGY = {
    "Software Engineering": ["Scrum Framework", "Version Control", "Git", "Continuous Integration", "CI/CD", "Software Testing", "Object-Oriented Programming", "Java", "C++", "HTML5", "CSS3", "JavaScript", "RESTful APIs", "UML", "Agile Methodology", "Entity-Relationship Diagrams", "User Experience"],
    "Artificial Intelligence": ["Machine Learning", "Neural Networks", "Natural Language Processing", "Heuristic Search", "Artificial Intelligence", "Predictive Models"],
    "Cybersecurity": ["Public Key Infrastructure", "PKI", "Advanced Encryption Standard", "AES", "Hash Functions", "Penetration Testing", "Cryptography", "Network Security"],
    "Data & Algorithms": ["Linked Lists", "Binary Search Trees", "Big-O Notation", "Dynamic Programming", "SQL", "Relational Database", "RDBMS", "Normalization", "NoSQL"],
   "Systems & Architecture": [
    "Process Scheduling", "Memory Management", "POSIX Threads", 
    "Bash Scripting", "Instruction Set Architecture", "ISA", 
    "CPU Pipelining", "Cache Coherence", "Parallel Processing",
    "Code Optimization", "Register Allocation", "Intermediate Code Generation", "Target Machine Code"]
}

def run_ontology_ner():
    print("Initializing spaCy NLP Engine with Custom Ontology...")
    
    # Load the English language model
    nlp = spacy.load("en_core_web_sm")
    
    # Create an Entity Ruler (This tells the AI to prioritize our dictionary)
    ruler = nlp.add_pipe("entity_ruler", before="ner")
    
    # Load our Ontology into the AI's brain
    patterns = []
    for specialization, skills in CS_ONTOLOGY.items():
        for skill in skills:
            # We tell spaCy: "If you see this exact phrase, tag it with this Specialization"
            patterns.append({"label": specialization, "pattern": [{"LOWER": word.lower()} for word in skill.split()]})
            
    ruler.add_patterns(patterns)

    # Load the raw PDF data
    with open(RAW_DATA_PATH, "r") as f:
        courses = json.load(f)
        
    print(f"AI Engine Armed! Scanning {len(courses)} courses...\n")
    
    for course in courses:
        synopsis = course.get("synopsis", "")
        extracted_skills = []
        specialization_scores = {spec: 0 for spec in CS_ONTOLOGY.keys()}
        
        if synopsis:
            # The NLP engine reads the paragraph
            doc = nlp(synopsis)
            
            # Extract ONLY the entities that match our Custom CS Ontology
            for ent in doc.ents:
                if ent.label_ in CS_ONTOLOGY:
                    if ent.text not in extracted_skills:
                        extracted_skills.append(ent.text)
                    specialization_scores[ent.label_] += 1
                    
        # Determine the Specialization based on the majority of extracted skills
        assigned_specialization = "Core Computer Science"
        highest_score = 0
        for spec, score in specialization_scores.items():
            if score > highest_score:
                highest_score = score
                assigned_specialization = spec

        # Attach pristine data to the course
        course["technical_skills"] = extracted_skills
        course["specialization"] = assigned_specialization
        
        print(f"[{course['course_id']}] {course['title']}")
        print(f"  -> Skills: {course['technical_skills']}")
        print(f"  -> Track:  {course['specialization']}\n")

    # Save the perfect JSON for the D3.js frontend
    with open(FINAL_GRAPH_PATH, "w") as f:
        json.dump(courses, f, indent=4)
        
    print(f"SUCCESS: Perfect, presentation-ready graph data generated at {FINAL_GRAPH_PATH}")

if __name__ == "__main__":
    run_ontology_ner()