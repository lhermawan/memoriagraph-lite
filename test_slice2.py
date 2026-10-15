import os
from fastapi.testclient import TestClient
from server import app
import database

client = TestClient(app)

def test_slice2_api():
    print("[1/5] Testing GET /api/health...")
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"
    
    print("[2/5] Testing POST /api/seed (preloading generic developer cases)...")
    res = client.post("/api/seed")
    assert res.status_code == 200
    assert res.json()["status"] == "seeded"
    assert res.json()["count"] == 3
    
    print("[3/5] Testing GET /api/graph...")
    res = client.get("/api/graph")
    assert res.status_code == 200
    graph = res.json()
    assert len(graph["nodes"]) > 0
    assert len(graph["edges"]) > 0
    print(f"      Graph nodes: {len(graph['nodes'])}, edges: {len(graph['edges'])}")
    
    print("[4/5] Testing POST /api/episodes (Manual 'Teach Memory' Form)...")
    test_episode = {
        "title": "CORS Preflight Options 405 Method Not Allowed",
        "problem": "Browser OPTIONS request fails on API endpoint because handler only allows POST.",
        "mitigation": "Add CORSMiddleware with allowed_methods=['*'] before route definition.",
        "solution": "FastAPI CORSMiddleware properly registered at app root level.",
        "tags": "cors, fastapi, api"
    }
    res = client.post("/api/episodes", json=test_episode)
    assert res.status_code == 201
    created = res.json()["episode"]
    assert created["title"] == test_episode["title"]
    assert created["tags"] == "cors, fastapi, api"
    
    print("[5/5] Testing GET /api/search...")
    res = client.get("/api/search?q=cors")
    assert res.status_code == 200
    search_data = res.json()
    assert search_data["count"] >= 1
    assert any("CORS" in r["title"] for r in search_data["results"])
    
    # Test index.html static serving
    res = client.get("/")
    assert res.status_code == 200
    assert "MemoriaGraph Lite" in res.text
    
    print("✓ Slice 2 Mechanical Verification Passed Flawlessly!")

if __name__ == "__main__":
    test_slice2_api()
