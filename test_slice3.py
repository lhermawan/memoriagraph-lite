import json
import subprocess
import sys

def test_slice3_mcp():
    print("[1/3] Testing MCP initialize & tools/list via stdio...")
    
    init_payload = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
    tools_payload = json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
    
    record_payload = json.dumps({
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "memoria_record",
            "arguments": {
                "title": "PostgreSQL Connection Pool Exhaustion under Load",
                "problem": "Backend services throw 'FATAL: remaining connection slots are reserved' during traffic spikes.",
                "mitigation": "Enable PgBouncer connection pooling in transaction mode and configure client-side pool size limits.",
                "solution": "Deployed PgBouncer sidecar with max_client_conn=1000 and default_pool_size=25.",
                "tags": "postgres, database, pgbouncer, performance"
            }
        }
    })
    
    recall_payload = json.dumps({
        "jsonrpc": "2.0",
        "id": 4,
        "method": "tools/call",
        "params": {
            "name": "memoria_recall",
            "arguments": {
                "query": "pgbouncer"
            }
        }
    })
    
    input_data = f"{init_payload}\n{tools_payload}\n{record_payload}\n{recall_payload}\n"
    
    process = subprocess.Popen(
        [sys.executable, "mcp_server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    
    stdout, stderr = process.communicate(input=input_data, timeout=5)
    assert process.returncode == 0, f"Process failed with return code {process.returncode}. Stderr: {stderr}"
    
    lines = [line.strip() for line in stdout.splitlines() if line.strip()]
    assert len(lines) == 4, f"Expected 4 responses, got {len(lines)}: {lines}"
    
    res1 = json.loads(lines[0])
    assert res1["id"] == 1
    assert res1["result"]["serverInfo"]["name"] == "memoriagraph-lite"
    
    res2 = json.loads(lines[1])
    assert res2["id"] == 2
    tools = [t["name"] for t in res2["result"]["tools"]]
    assert "memoria_record" in tools
    assert "memoria_recall" in tools
    print(f"      Discovered Tools: {tools}")
    
    res3 = json.loads(lines[2])
    assert res3["id"] == 3
    assert not res3["result"]["isError"]
    assert "Successfully stored memory episode" in res3["result"]["content"][0]["text"]
    print("      memoria_record execution verified.")
    
    res4 = json.loads(lines[3])
    assert res4["id"] == 4
    assert not res4["result"]["isError"]
    recall_text = res4["result"]["content"][0]["text"]
    assert "PostgreSQL Connection Pool Exhaustion" in recall_text
    assert "PgBouncer" in recall_text
    print("      memoria_recall execution verified.")
    
    print("✓ Slice 3 Mechanical Verification Passed Flawlessly!")

if __name__ == "__main__":
    test_slice3_mcp()
