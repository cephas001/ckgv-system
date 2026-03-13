from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI()

# CRITICAL: Allows the Frontend (Nuxt) to talk to the Backend (FastAPI)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, specify the Nuxt URL
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_PATH = os.path.join("data", "final_graph_data.json")

@app.get("/")
def read_root():
    return {"status": "CKGV API is running"}

@app.get("/api/graph")
def get_graph_data():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r") as f:
            return json.load(f)
    return {"error": "Data file not found"}