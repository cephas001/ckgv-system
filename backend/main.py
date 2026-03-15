from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Modular routers
from routers import admin, graph, extraction

# Initialize the main FastAPI application
app = FastAPI(
    title="CKGV System API",
    description="Backend services for the Interactive Curriculum Knowledge Graph Visualization."
)

# CRITICAL: Allows the Frontend (Nuxt) to talk to the Backend (FastAPI)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, change this to your specific URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect the routers to the main application
app.include_router(admin.router)
app.include_router(graph.router)
app.include_router(extraction.router)

@app.get("/")
def read_root():
    return {"status": "CKGV API is running securely and modularly!"}