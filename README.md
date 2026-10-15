# 🧠 MemoriaGraph Lite

> **Autonomous Cognitive Memory & Decision Hub for AI Coding Agents**  
> *Built for Devpost Learn: "Build With AI: Basics" Hackathon*

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![MCP Ready](https://img.shields.io/badge/MCP-Compatible-8b5cf6.svg)](https://modelcontextprotocol.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-emerald.svg)](LICENSE)

---

## 💡 The Core Idea: Solving AI Agent Amnesia

Most AI coding agents suffer from severe **session amnesia**. When you start a new conversation or switch tasks, the agent forgets hard-won architectural decisions and repeats the exact same debugging mistakes. 

Dumping raw conversation history is noisy, wastes context tokens, and distracts the agent.

**MemoriaGraph Lite** solves this by distilling every solved technical roadblock into a structured cognitive triad:

```
[ Problem Roadblock ] ──(MITIGATED_BY)──> [ Mitigation Heuristic ] ──(SOLVED_BY)──> [ Verified Solution ]
         │                                                                                    │
         └───────────────────────────(TAGGED_WITH)────────────────────────────────────────────┘
                                            ▼
                                  [ Shared Domain Tags ]
```

When an agent encounters a similar error in the future, it queries MemoriaGraph Lite via the **Model Context Protocol (MCP)** to immediately recall verified mitigation steps and tested code fixes—avoiding the trap on the very first attempt.

---

## ✨ Features at a Glance

1. **Interactive 2D Physics Visualizer:** Modern single-screen cockpit with glowing dark-cyber aesthetic (`#0a0d14`). Pan, zoom, and drag nodes to explore relationships.
2. **Cognitive Triad Inspection Drawer:** Click any incident to inspect its Problem, Mitigation Heuristic, and Verified Code Solution in a sliding right drawer.
3. **Dual-Tool Model Context Protocol (MCP) Server:** Stdio JSON-RPC server (`mcp_server.py`) with `memoria_record` and `memoria_recall` for seamless integration into Claude Code, Cursor, Codex, and Antigravity.
4. **Manual Second-Brain Training Form:** Non-technical users and beginners can train the agent's memory directly via the "+ Teach Memory" modal without touching the terminal.
5. **Zero-Friction Sample Cases Loader:** Preload 3 realistic, sanitized open-source developer scenarios (JWT 401 Expiration, React SSR Hydration Mismatch, Docker OOMKilled 137) with a single click.
6. **Zero-Build Portability:** Single embedded SQLite database (`memoria.db`) + zero-compile HTML5/JS. Runs anywhere with zero external database dependencies.

---

## 🚀 Quickstart (Run in 30 Seconds)

### 1. Clone & Install
```bash
git clone https://github.com/lhermawan/memoriagraph-lite.git
cd memoriagraph-lite
pip install -r requirements.txt
```

### 2. Start the Cockpit

**Linux / macOS:**
```bash
python3 server.py
```

**Windows (PowerShell / Command Prompt):**
```cmd
py server.py
# or: python server.py
```

Open **[http://localhost:8000](http://localhost:8000)** in your browser!

---

## 🔌 Model Context Protocol (MCP) Integration

MemoriaGraph Lite ships with a native stdio MCP server in `mcp_server.py`.

### Configuration (Google Antigravity, Claude Code, Cursor, Claude Desktop)

**Linux / macOS:**
```json
{
  "mcpServers": {
    "memoriagraph": {
      "command": "python3",
      "args": ["/ABSOLUTE/PATH/TO/memoriagraph-lite/mcp_server.py"]
    }
  }
}
```

**Windows:**
```json
{
  "mcpServers": {
    "memoriagraph": {
      "command": "py",
      "args": ["C:\\path\\to\\memoriagraph-lite\\mcp_server.py"]
    }
  }
}
```
*(Tip on Windows: If `py` is not in your global PATH, use `"command": "python"` or the full path to `python.exe`)*

### Available MCP Tools
* `memoria_record(title, problem, mitigation, solution, tags)`: Saves a new cognitive triad into the graph database.
* `memoria_recall(query)`: Searches memory and returns ranked problem/mitigation/solution prompts.

---

## 📋 Devpost Learn Hackathon Artifacts

This project was built following the official **Devpost Learn: Build With AI: Basics** plan-first curriculum:

* 📄 **[`devpost/scope.md`](devpost/scope.md):** Project boundary, kernel definition, and what was explicitly cut.
* 📄 **[`devpost/prd.md`](devpost/prd.md):** Complete product requirements, core user journey, and acceptance criteria.
* 📄 **[`devpost/spec.md`](devpost/spec.md):** Technical specification, data models, and stack rationale.
* 📄 **[`devpost/checklist.md`](devpost/checklist.md):** Ordered verifiable build slices and hands-on checkpoint logs.

---

## 🎬 90-Second Demo Script

1. **Launch:** Run `python3 server.py` and open `http://localhost:8000`. Show the clean initial empty state.
2. **Seed:** Click **"Load Sample Cases"** to watch the Vis-Network physics engine animate and form the interconnected knowledge graph.
3. **Inspect:** Click the *JWT 401 Unauthorized* problem node. Notice the right sidebar slide out displaying the exact mitigation strategy and Axios interceptor solution.
4. **Teach:** Click **"+ Teach Memory"** to demonstrate how a developer manually enters a new troubleshooting case (`Problem -> Mitigation -> Solution`).
5. **Agent Recall:** Demonstrate MCP terminal query:
   ```bash
   echo '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"memoria_recall","arguments":{"query":"jwt"}}}' | python3 mcp_server.py
   ```
   Show how the agent autonomously receives the verified solution to fix the bug on the first try!

---

## 🛡️ License

MIT License © 2026 Lucky Hermawan Roza (`lhermawan`)
