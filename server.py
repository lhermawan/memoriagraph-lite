"""
server.py — FastAPI Application Server for MemoriaGraph Lite.
Serves REST API endpoints and static Web Visualizer cockpit.
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

import database

# Pydantic Schemas
database.init_db()

class EpisodeCreate(BaseModel):
    title: str = Field(..., min_length=3, description="Incident or decision title")
    problem: str = Field(..., min_length=5, description="What went wrong or was needed")
    mitigation: str = Field(..., min_length=5, description="Immediate troubleshooting or heuristic")
    solution: str = Field(..., min_length=5, description="Verified code fix or permanent configuration")
    tags: Optional[str] = Field("", description="Comma-separated domain tags")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: ensure SQLite database schema is initialized
    database.init_db()
    yield


app = FastAPI(
    title="MemoriaGraph Lite",
    description="Autonomous Cognitive Memory Engine & Graph Visualizer for AI Coding Agents",
    version="1.0.0",
    lifespan=lifespan,
)

# Enable CORS for local dev / MCP consumers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure static directory exists
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(STATIC_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", response_class=FileResponse)
async def serve_index():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "MemoriaGraph Lite API is running. Add static/index.html to view visualizer."}


@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "MemoriaGraph Lite",
        "version": "1.0.0",
    }


@app.get("/api/graph")
async def get_graph_data():
    """Returns nodes and edges formatted for Vis-Network graph visualization."""
    return database.get_graph()


@app.get("/api/episodes")
async def list_episodes():
    """Returns all recorded cognitive episodes."""
    return database.get_episodes()


@app.get("/api/episodes/{episode_id}")
async def get_single_episode(episode_id: str):
    """Retrieves full details of a single episode."""
    ep = database.get_episode(episode_id)
    if not ep:
        raise HTTPException(status_code=404, detail="Episode not found")
    return ep


@app.post("/api/episodes", status_code=status.HTTP_201_CREATED)
async def create_episode(payload: EpisodeCreate):
    """Creates a new cognitive episode and automatically derives relational graph edges."""
    episode = database.add_episode(
        title=payload.title,
        problem=payload.problem,
        mitigation=payload.mitigation,
        solution=payload.solution,
        tags=payload.tags or "",
    )
    return {
        "status": "created",
        "episode": episode,
        "graph": database.get_graph(),
    }


@app.delete("/api/episodes/{episode_id}")
async def delete_episode_endpoint(episode_id: str):
    """Removes an episode and cleans up associated graph edges."""
    deleted = database.delete_episode(episode_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Episode not found")
    return {"status": "deleted", "id": episode_id}


@app.get("/api/search")
async def search_endpoint(q: str = Query("", description="Keyword search across memories")):
    """Searches memory episodes by keyword or tag."""
    matches = database.search_episodes(q)
    return {
        "query": q,
        "count": len(matches),
        "results": matches,
    }


@app.post("/api/seed")
async def seed_endpoint():
    """Preloads the 3 sanitized generic developer cases."""
    count = database.seed_sample_data()
    return {
        "status": "seeded",
        "count": count,
        "message": f"Successfully loaded {count} generic developer cases.",
        "graph": database.get_graph(),
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
