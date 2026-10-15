#!/usr/bin/env python3
"""
mcp_server.py — Dual-Tool Model Context Protocol (MCP) Stdio Server.
Exposes memoria_record and memoria_recall for Claude Code, Cursor, and Antigravity.
Protocol: JSON-RPC 2.0 over stdio.
"""

import sys
import json
import logging
from typing import Dict, Any, List

import database

# Configure logger to output exclusively to stderr so stdout remains pure JSON-RPC
logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [MCP] %(message)s",
)

SERVER_INFO = {
    "name": "memoriagraph-lite",
    "version": "1.0.0",
}

TOOLS = [
    {
        "name": "memoria_record",
        "description": "Store a solved debugging incident, technical roadblock, or architecture decision as a structured cognitive triad (Problem -> Mitigation -> Solution) into MemoriaGraph Lite.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Concise title of the incident, bug, or decision",
                },
                "problem": {
                    "type": "string",
                    "description": "Detailed description of the error, root cause, or roadblock",
                },
                "mitigation": {
                    "type": "string",
                    "description": "Step-by-step troubleshooting heuristic or immediate actions taken",
                },
                "solution": {
                    "type": "string",
                    "description": "Verified code fix, configuration change, or permanent resolution",
                },
                "tags": {
                    "type": "string",
                    "description": "Comma-separated domain tags (e.g. 'jwt, auth, api')",
                },
            },
            "required": ["title", "problem", "mitigation", "solution"],
        },
    },
    {
        "name": "memoria_recall",
        "description": "Recall past verified mitigations, heuristics, and code fixes from MemoriaGraph Lite when encountering similar bugs or architectural decisions.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Keyword, error message, or concept to search for in past memory",
                },
            },
            "required": ["query"],
        },
    },
]


def send_response(response_obj: Dict[str, Any]):
    """Sends a single JSON-RPC 2.0 response line to stdout."""
    payload = json.dumps(response_obj)
    sys.stdout.write(payload + "\n")
    sys.stdout.flush()


def handle_initialize(req_id: Any) -> Dict[str, Any]:
    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "result": {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {
                    "listChanged": False,
                },
            },
            "serverInfo": SERVER_INFO,
        },
    }


def handle_tools_list(req_id: Any) -> Dict[str, Any]:
    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "result": {
            "tools": TOOLS,
        },
    }


def handle_tools_call(req_id: Any, params: Dict[str, Any]) -> Dict[str, Any]:
    tool_name = params.get("name")
    args = params.get("arguments", {})

    if tool_name == "memoria_record":
        title = args.get("title", "").strip()
        problem = args.get("problem", "").strip()
        mitigation = args.get("mitigation", "").strip()
        solution = args.get("solution", "").strip()
        tags = args.get("tags", "").strip()

        if not all([title, problem, mitigation, solution]):
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {
                    "code": -32602,
                    "message": "Missing required fields: title, problem, mitigation, solution are mandatory.",
                },
            }

        ep = database.add_episode(
            title=title,
            problem=problem,
            mitigation=mitigation,
            solution=solution,
            tags=tags,
        )

        reply_text = (
            f"✓ Successfully stored memory episode into MemoriaGraph Lite:\n"
            f"- ID: {ep['id']}\n"
            f"- Title: {ep['title']}\n"
            f"- Triad: Problem -> Mitigation -> Solution created\n"
            f"- Tags: {ep['tags'] or 'none'}"
        )

        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "content": [{"type": "text", "text": reply_text}],
                "isError": False,
            },
        }

    elif tool_name == "memoria_recall":
        query = args.get("query", "").strip()
        episodes = database.search_episodes(query)

        if not episodes:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": f"No past memory episodes found matching '{query}'. Proceeding with standard reasoning.",
                        }
                    ],
                    "isError": False,
                },
            }

        output_lines = [f"Found {len(episodes)} relevant memory episode(s) in MemoriaGraph Lite:\n"]
        for idx, ep in enumerate(episodes[:5], 1):
            output_lines.append(f"### [{idx}] {ep['title']} (ID: {ep['id']})")
            output_lines.append(f"**Problem:**\n{ep['problem']}\n")
            output_lines.append(f"**Mitigation Heuristic:**\n{ep['mitigation']}\n")
            output_lines.append(f"**Verified Solution:**\n```\n{ep['solution']}\n```")
            if ep.get("tags"):
                output_lines.append(f"**Tags:** {ep['tags']}\n")
            output_lines.append("---\n")

        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "content": [{"type": "text", "text": "\n".join(output_lines)}],
                "isError": False,
            },
        }

    else:
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {
                "code": -32601,
                "message": f"Unknown tool: '{tool_name}'",
            },
        }


def run_stdio_server():
    """Main JSON-RPC stdio event loop."""
    database.init_db()
    logging.info("MemoriaGraph Lite MCP Stdio Server started.")

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        try:
            req = json.loads(line)
        except json.JSONDecodeError as e:
            logging.error(f"Malformed JSON: {e}")
            send_response({
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": "Parse error"},
            })
            continue

        method = req.get("method")
        req_id = req.get("id")

        if method == "initialize":
            send_response(handle_initialize(req_id))
        elif method in ("notifications/initialized", "initialized"):
            # Notifications do not return a response
            pass
        elif method == "tools/list":
            send_response(handle_tools_list(req_id))
        elif method == "tools/call":
            params = req.get("params", {})
            send_response(handle_tools_call(req_id, params))
        elif method == "ping":
            send_response({"jsonrpc": "2.0", "id": req_id, "result": {}})
        else:
            if req_id is not None:
                send_response({
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32601, "message": f"Method not found: '{method}'"},
                })


if __name__ == "__main__":
    run_stdio_server()
