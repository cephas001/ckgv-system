import spacy
from spacy.pipeline import EntityRuler
import json
import os

class CurriculumParser:
    def __init__(self):
        # Load the core model
        self.nlp = spacy.load("en_core_web_md")
        
        if self.nlp.has_pipe("entity_ruler"):
            self.nlp.remove_pipe("entity_ruler")
            
        self.ruler = self.nlp.add_pipe("entity_ruler", before="ner")
        
        # --- DYNAMIC PATH RESOLUTION ---
        # 1. Get the directory where this script lives (.../backend/services)
        CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

        # 2. Go up one level to the backend root (.../backend)
        BASE_DIR = os.path.dirname(CURRENT_DIR)

        # 3. Point to the data directory (.../backend/data)
        DATA_DIR = os.path.join(BASE_DIR, "data")
        ontology_path = os.path.join(DATA_DIR, "ontology.json")
        
        # --- LOAD THE CENTRALIZED ONTOLOGY ---
        try:
            with open(ontology_path, "r") as f:
                self.cs_ontology = json.load(f)
        except FileNotFoundError:
            print(f"ERROR: {ontology_path} not found. Using empty dictionary.")
            self.cs_ontology = {}
        
        # Convert Ontology into spaCy patterns
        patterns = []
        for specialization, skills in self.cs_ontology.items():
            for skill in skills:
                # We label the entity with its specialization (e.g., "Software Engineering")
                patterns.append({
                    "label": specialization, 
                    "pattern": [{"LOWER": word.lower()} for word in skill.replace("-", " ").split()],
                    "id": skill
                })
            
        self.ruler.add_patterns(patterns)

    def extract_metadata(self, course_text: str):
        doc = self.nlp(course_text)
        found_skills = set()
        specialization_scores = {spec: 0 for spec in self.cs_ontology.keys()}
        
        # Extract based on the Entity Ruler
        for ent in doc.ents:
            if ent.label_ in self.cs_ontology:
                # NEW: Use ent.ent_id_ (the exact ontology string) instead of ent.text.title()
                exact_skill_name = ent.ent_id_ if ent.ent_id_ else ent.text
                found_skills.add(exact_skill_name)
                specialization_scores[ent.label_] += 1

        # Determine Specialization based on highest score
        suggested_spec = "Core Computer Science"
        highest_score = 0
        for spec, score in specialization_scores.items():
            if score > highest_score:
                highest_score = score
                suggested_spec = spec

        return {
            "extracted_skills": list(found_skills),
            "suggested_specialization": suggested_spec
        }