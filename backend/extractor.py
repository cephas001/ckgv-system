import pdfplumber
import re
import json
import os

# Path to curriculum handbook
PDF_PATH = os.path.join("data", "Mock_CS_Handbook.pdf")

def extract_curriculum(pdf_path):
    extracted_courses = []
    
    # 1. THE REGEX TARGETS (Hunting for specific NUC/School formats)
    course_pattern = re.compile(r"Course Module:\s*([A-Z]{3}\s\d{3}):\s*(.*?)\s*\(")
    prereq_pattern = re.compile(r"Prerequisite:\s*(None|[A-Z]{3}\s\d{3})")
    credit_pattern = re.compile(r"Credit Units:\s*(\d+)")
    synopsis_header_pattern = re.compile(r"Course Synopsis")
    
    # Extract all raw text from the PDF
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"
                
    # 2. STATEFUL PARSING LOGIC
    current_course = None
    capturing_synopsis = False
    synopsis_text = []

    for line in full_text.split('\n'):
        line = line.strip()
        if not line:
            continue
            
        # Check if we hit a new course
        course_match = course_pattern.search(line)
        if course_match:
            # If we were already tracking a course, save it before starting the new one!
            if current_course:
                current_course['synopsis'] = " ".join(synopsis_text).strip()
                extracted_courses.append(current_course)
            
            # Start tracking the new course
            current_course = {
                "course_id": course_match.group(1).strip(),
                "title": course_match.group(2).strip(),
                "prerequisites": [],
                "credits": 0,
                "synopsis": ""
            }
            capturing_synopsis = False
            synopsis_text = []
            continue
        
        # If we are currently inside a course block, look for its metadata
        if current_course and not capturing_synopsis:
            prereq_match = prereq_pattern.search(line)
            if prereq_match:
                prereq = prereq_match.group(1).strip()
                if prereq.lower() != "none":
                    current_course["prerequisites"].append(prereq)
                continue
            
            credit_match = credit_pattern.search(line)
            if credit_match:
                current_course["credits"] = int(credit_match.group(1))
                continue
                
            # Detect the start of the summary paragraph so we can switch states
            if synopsis_header_pattern.search(line):
                capturing_synopsis = True
                continue
        
        # Capture the paragraph text (The BERT Target)
        if current_course and capturing_synopsis:
            # Trap to ignore page headers that interrupt the text
            if "McPherson University" in line or "Department of Computer Science" in line or line.startswith("Level:") or line.startswith("Semester:") or line.startswith("Course Type:"):
                continue
            synopsis_text.append(line)

    # Don't forget to append the very last course in the document!
    if current_course:
        current_course['synopsis'] = " ".join(synopsis_text).strip()
        extracted_courses.append(current_course)

    return extracted_courses

if __name__ == "__main__":
    print(f"Scanning {PDF_PATH}...\n")
    try:
        courses = extract_curriculum(PDF_PATH)
        
        # NEW: Save to a JSON file for the AI to read
        output_path = os.path.join("data", "raw_courses.json")
        with open(output_path, "w") as f:
            json.dump(courses, f, indent=4)
            
        print(f"✅ SYSTEM SUCCESS: Extracted {len(courses)} courses and saved to {output_path}!")
    except FileNotFoundError:
        print(f"❌ ERROR: Could not find the PDF. Make sure it is saved exactly at: {PDF_PATH}")