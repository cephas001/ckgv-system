import os
import json
import spacy
import sys

# --- PATH RESOLUTION ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR)
DATA_DIR = os.path.join(BASE_DIR, "data")

# Add the backend root to the system path so we can import your custom parser
sys.path.append(BASE_DIR)
from services.nlp_processor import CurriculumParser

# --- LOAD DATA ---
RAW_DATA_PATH = os.path.join(DATA_DIR, "raw_courses.json")
GROUND_TRUTH_PATH = os.path.join(DATA_DIR, "ground_truth.json")
ONTOLOGY_PATH = os.path.join(DATA_DIR, "ontology.json")

with open(GROUND_TRUTH_PATH, "r") as f:
    ground_truth = json.load(f)

with open(RAW_DATA_PATH, "r") as f:
    all_courses = json.load(f)

with open(ONTOLOGY_PATH, "r") as f:
    ontology = json.load(f)

# Flatten ontology into a single list of keywords for Baseline 1
flat_ontology_skills = []
for skills in ontology.values():
    flat_ontology_skills.extend([s.lower() for s in skills])

# Filter our raw courses to ONLY the ones in our ground truth file
eval_courses = [c for c in all_courses if c["course_id"] in ground_truth]

# --- INITIALIZE MODELS ---
print("Loading Models...")
# Baseline 2: Standard spaCy (No custom rules)
vanilla_nlp = spacy.load("en_core_web_md")
# Proposed Model: Your custom CurriculumParser
proposed_parser = CurriculumParser()

def calculate_metrics(name, total_extracted, true_positives, false_positives, false_negatives):
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    print(f"\n--- {name} ---")
    print(f"Total Extracted: {total_extracted}")
    print(f"Correct (TP): {true_positives} | Missed (FN): {false_negatives} | Garbage (FP): {false_positives}")
    print(f"Precision: {precision * 100:.1f}%")
    print(f"Recall:    {recall * 100:.1f}%")
    print(f"F1-Score:  {f1 * 100:.1f}%")

def run_evaluation():
    # Trackers for our 3 models
    results = {
        "Baseline 1: Keyword Matching": {"extracted": 0, "tp": 0, "fp": 0, "fn": 0},
        "Baseline 2: Vanilla spaCy NER": {"extracted": 0, "tp": 0, "fp": 0, "fn": 0},
        "Proposed Model: Ontology NER": {"extracted": 0, "tp": 0, "fp": 0, "fn": 0}
    }

    for course in eval_courses:
        course_id = course["course_id"]
        synopsis = course["synopsis"]
        
        # Make the truth set case-insensitive for fair comparison
        truth_set = set([s.lower() for s in ground_truth[course_id]])
        
        # ---------------------------------------------------------
        # MODEL A: Baseline Keyword Matching (Regex/String search)
        # ---------------------------------------------------------
        model_a_extracted = set()
        for skill in flat_ontology_skills:
            if skill in synopsis.lower():
                model_a_extracted.add(skill)
                
        # ---------------------------------------------------------
        # MODEL B: Vanilla spaCy NER (Standard AI without your rules)
        # ---------------------------------------------------------
        doc = vanilla_nlp(synopsis)
        # Vanilla spaCy just grabs generic entities like ORG, DATE, PERSON
        model_b_extracted = set([ent.text.lower() for ent in doc.ents])

        # ---------------------------------------------------------
        # MODEL C: Your Proposed Ontology-Driven NER
        # ---------------------------------------------------------
        parsed_data = proposed_parser.extract_metadata(synopsis)
        model_c_extracted = set([s.lower() for s in parsed_data["extracted_skills"]])

        # --- SCORE THE MODELS ---
        models_to_score = [
            ("Baseline 1: Keyword Matching", model_a_extracted),
            ("Baseline 2: Vanilla spaCy NER", model_b_extracted),
            ("Proposed Model: Ontology NER", model_c_extracted)
        ]

        for model_name, extracted_set in models_to_score:
            results[model_name]["extracted"] += len(extracted_set)
            
            # True Positives: In both extraction and truth set
            tp = len(extracted_set.intersection(truth_set))
            # False Positives: Extracted, but NOT in truth set (AI hallucination/garbage)
            fp = len(extracted_set - truth_set)
            # False Negatives: In truth set, but NOT extracted (AI missed it)
            fn = len(truth_set - extracted_set)
            
            results[model_name]["tp"] += tp
            results[model_name]["fp"] += fp
            results[model_name]["fn"] += fn

    print("\n================ EVALUATION RESULTS ================")
    for model_name, data in results.items():
        calculate_metrics(model_name, data["extracted"], data["tp"], data["fp"], data["fn"])

if __name__ == "__main__":
    run_evaluation()