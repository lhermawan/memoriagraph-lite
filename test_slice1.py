import os
import database

TEST_DB = "test_memoria.db"

def test_slice1():
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    
    print("[1/4] Initializing SQLite schema...")
    database.init_db(TEST_DB)
    
    print("[2/4] Seeding sample developer cases...")
    seeded = database.seed_sample_data(TEST_DB)
    assert seeded == 3, f"Expected 3 seeded episodes, got {seeded}"
    
    print("[3/4] Testing graph derivation...")
    graph = database.get_graph(TEST_DB)
    nodes = graph["nodes"]
    edges = graph["edges"]
    
    # 3 episodes * 4 core nodes (Hub, Prob, Mit, Sol) + tag nodes
    hub_nodes = [n for n in nodes if n["group"] == "episode"]
    prob_nodes = [n for n in nodes if n["group"] == "problem"]
    mit_nodes = [n for n in nodes if n["group"] == "mitigation"]
    sol_nodes = [n for n in nodes if n["group"] == "solution"]
    tag_nodes = [n for n in nodes if n["group"] == "tag"]
    
    assert len(hub_nodes) == 3, f"Expected 3 hub nodes, got {len(hub_nodes)}"
    assert len(prob_nodes) == 3, f"Expected 3 problem nodes, got {len(prob_nodes)}"
    assert len(mit_nodes) == 3, f"Expected 3 mitigation nodes, got {len(mit_nodes)}"
    assert len(sol_nodes) == 3, f"Expected 3 solution nodes, got {len(sol_nodes)}"
    assert len(tag_nodes) > 0, "Expected shared tag nodes"
    assert len(edges) > 0, "Expected relational edges"
    
    print(f"      Total Nodes: {len(nodes)} (Hubs: {len(hub_nodes)}, Problems: {len(prob_nodes)}, Mitigations: {len(mit_nodes)}, Solutions: {len(sol_nodes)}, Tags: {len(tag_nodes)})")
    print(f"      Total Edges: {len(edges)}")
    
    print("[4/4] Testing keyword search...")
    jwt_results = database.search_episodes("jwt", TEST_DB)
    assert len(jwt_results) == 1
    assert "JWT" in jwt_results[0]["title"]
    
    oom_results = database.search_episodes("oom", TEST_DB)
    assert len(oom_results) == 1
    assert "Docker" in oom_results[0]["title"]
    
    # Cleanup test db
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
        
    print("✓ Slice 1 Mechanical Verification Passed Flawlessly!")

if __name__ == "__main__":
    test_slice1()
