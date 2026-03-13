# Run the PDF Extraction
extract:
	python extractor.py

# Run the NLP AI Pipeline
nlp:
	python nlp_pipeline.py

# Start the FastAPI Server
api:
	uvicorn main:app --reload

# Install all dependencies at once
install:
	pip install pdfplumber spacy transformers torch keybert fastapi uvicorn
	python -m spacy download en_core_web_sm