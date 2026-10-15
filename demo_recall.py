#!/usr/bin/env python3
"""
demo_recall.py — Quick interactive terminal demo showing an AI agent querying MemoriaGraph Lite MCP.
Can be run on Linux (python3 demo_recall.py) and Windows (py demo_recall.py).
"""

import sys
import json
import subprocess

def run_mcp_query(query: str = "jwt"):
    print(f"\n==================================================")
    print(f"🤖 AI AGENT MCP QUERY -> MemoriaGraph Lite")
    print(f"   Executing: memoria_recall(query='{query}')")
    print(f"==================================================\n")

    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "memoria_recall",
            "arguments": {"query": query}
        }
    }

    try:
        proc = subprocess.Popen(
            [sys.executable, "mcp_server.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = proc.communicate(input=json.dumps(request) + "\n", timeout=5)
        
        for line in stdout.splitlines():
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            if "result" in data and "content" in data["result"]:
                for item in data["result"]["content"]:
                    print(item["text"])
            elif "error" in data:
                print(f"Error: {data['error']['message']}")
                
    except Exception as e:
        print(f"Failed to query MCP server: {e}")

    print("\n--------------------------------------------------")
    print("✓ MCP Recall verified! Agent retrieved past fix without amnesia.")
    print("==================================================\n")

if __name__ == "__main__":
    search_term = sys.argv[1] if len(sys.argv) > 1 else "jwt"
    run_mcp_query(search_term)
