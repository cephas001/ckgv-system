import spacy
import json
import os

class CurriculumParser:
    def __init__(self):
        print("Initializing spaCy NLP Engine with Centralized Ontology...")
        self.nlp = spacy.load("en_core_web_md")
        
        if self.nlp.has_pipe("entity_ruler"):
            self.nlp.remove_pipe("entity_ruler")
            
        self.ruler = self.nlp.add_pipe("entity_ruler", before="ner")
        
        # --- DYNAMIC PATH RESOLUTION ---
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.dirname(current_dir)
        ontology_path = os.path.join(base_dir, "data", "ontology.json")
        
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
                patterns.append({
                    "label": specialization, 
                    "pattern": [{"LOWER": word.lower()} for word in skill.replace("-", " ").split()],
                    "id": skill
                })
            
        self.ruler.add_patterns(patterns)

    def extract_metadata(self, course_text: str):
        # Handle empty synopses gracefully
        if not course_text or not isinstance(course_text, str):
            return {
                "extracted_skills": [],
                "suggested_specialization": "Core Computer Science"
            }

        doc = self.nlp(course_text)
        found_skills = set()
        specialization_scores = {spec: 0 for spec in self.cs_ontology.keys()}
        
        # Extract based on the Entity Ruler
        for ent in doc.ents:
            if ent.label_ in self.cs_ontology:
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