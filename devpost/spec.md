---
doc: spec
status: approved
---

# MemoriaGraph Lite — Technical Spec

## How This Works, In Plain Language
MemoriaGraph Lite is a lightweight, zero-dependency cognitive memory engine designed to keep AI coding agents from repeating mistakes and losing problem-solving context.

When an AI agent or a developer solves a bug or makes an architectural decision, the experience is distilled into a structured triad: **`Problem -> Mitigation -> Solution`** with domain tags. 
- The **Python FastAPI backend** receives this triad via REST API or the **Model Context Protocol (MCP)** server and writes it into a local SQLite database (`memoria.db`).
- The database stores both the raw episodes and the derived graph relationships (problems linked to their mitigations, solutions, and shared domain tags).
- An interactive **Web Visualizer** running in the browser polls or streams graph updates and renders a glowing, physics-based 2D network graph.
- When an AI agent (Claude Code, Cursor, Codex, Antigravity) encounters a future roadblock, it queries `memoria_recall` via MCP to retrieve the proven mitigation and verified fix.

Why this shape? Traditional agent setups either dump thousands of tokens of noisy chat logs into context or rely on heavy external graph databases (like Neo4j clusters) that are cumbersome to install. MemoriaGraph Lite uses a single embedded SQLite database and a zero-build HTML/JS interface so anyone—including hackathon judges—can clone and run it with one command in seconds.

## The Core Journey Through the System
1. **Startup & Web Access:** The user starts the server (`python3 server.py`) and navigates to `http://localhost:8000`. The browser loads `static/index.html`, fetching assets directly from FastAPI.  
   *(PRD ref: `prd.md > The Core Journey`, Step 1)*
2. **Empty State & Seeding:** The frontend issues a `GET /api/graph`. If nodes count is 0, the UI renders the empty state welcome banner. Clicking "Load Sample Cases" calls `POST /api/seed`, which inserts 3 generic developer troubleshooting episodes and their relational edges into SQLite.  
   *(PRD ref: `prd.md > The Core Journey`, Steps 2 & 3)*
3. **Graph Rendering:** `static/app.js` initializes Vis-Network with custom physics and dark-mode styling. Nodes represent Problems (amber), Mitigations (cyan), Solutions (emerald), and Tags (slate). Edges represent `MITIGATED_BY`, `SOLVED_BY`, and `TAGGED_WITH`.  
   *(PRD ref: `prd.md > Screens and Layout` & `prd.md > Interactive Graph Visualizer`)*
4. **Node Inspection:** Clicking a node triggers `onSelectNode` in `app.js`, opening the right-hand inspection drawer populated with the full markdown content of the cognitive triad.  
   *(PRD ref: `prd.md > Screens and Layout`)*
5. **Search & Filter:** As the user types in the search bar, the UI sends `GET /api/search?q={query}` (or filters in-memory), highlighting matching nodes and dimming non-matches.  
   *(PRD ref: `prd.md > Features and Behavior > 2. Search & Filter Bar`)*
6. **Manual Knowledge Ingestion:** Clicking "+ Teach Memory" opens a modal. The user fills out Problem, Mitigation, Solution, and Tags, then submits via `POST /api/episodes`. The backend saves to SQLite and returns the new node/edge payload, which the frontend appends to the graph without a page refresh.  
   *(PRD ref: `prd.md > Features and Behavior > 3. Manual "Teach Memory" Form`)*
7. **Agent MCP Recall & Record:** An AI coding agent connected via `mcp_server.py` executes:
   - `memoria_record(problem, mitigation, solution, tags)`: writes directly to SQLite and notifies the API.
   - `memoria_recall(query)`: runs a keyword/tag hybrid search across problems and mitigations, returning formatted solution prompts.  
   *(PRD ref: `prd.md > Features and Behavior > 5. Model Context Protocol (MCP) Server Interface`)*

## Stack
- **Language & Runtime:** Python 3.10+ (tested on Python 3.12).
- **Backend API:** FastAPI (`fastapi>=0.110.0`) & Uvicorn (`uvicorn[standard]>=0.28.0`).
  - *Rationale:* High performance, native async support, automated OpenAPI docs, zero boilerplate.
  - *Docs:* [FastAPI Documentation](https://fastapi.tiangolo.com/)
- **Data Storage:** SQLite 3 (Python built-in `sqlite3`).
  - *Rationale:* 100% portable, embedded, zero server setup, single-file durability (`memoria.db`).
- **MCP Server Protocol:** Model Context Protocol Python SDK or lightweight JSON-RPC 2.0 stdio runner.
  - *Rationale:* Native standard for Claude Code, Cursor, Antigravity, and modern AI coding harnesses.
  - *Docs:* [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- **Frontend Framework:** Vanilla HTML5 / Modern ES6 JavaScript / CSS3.
- **Graph Visualization Engine:** Vis-Network (loaded via unpkg CDN, fallback included).
  - *Rationale:* Zero build step (no `npm run build`, no node_modules required to run the server), responsive canvas physics, interactive node drag/zoom.
  - *Docs:* [Vis-Network Documentation](https://visjs.github.io/vis-network/docs/network/)

## Where It Runs and How Someone Tries It
- **Runtime Environment:** Any standard Linux, macOS, or Windows machine with Python 3.10+.
- **Setup & Run in 2 Commands:**
  ```bash
  pip install -r requirements.txt
  python3 server.py
  ```
- **Web Interface:** Open `http://localhost:8000` in any modern web browser.
- **MCP Integration:** Add to Claude Code or Cursor config:
  ```json
  {
    "mcpServers": {
      "memoriagraph": {
        "command": "python3",
        "args": ["/path/to/memoriagraph-lite/mcp_server.py"]
      }
    }
  }
  ```
- **Demo Recording Plan:**
  A 90-second video demo showing:
  1. Starting the server in terminal and launching the clean web UI.
  2. Clicking "Load Sample Cases" to show the instant graph physics visualization.
  3. Clicking "+ Teach Memory" to demonstrate the manual second-brain training form.
  4. Running a mock agent MCP query in terminal (`memoria_recall`) to show how an AI agent uses the memory to avoid an amnesia trap.

## Look and Feel
Carried forward from `prd.md > Look and Feel` and `scope.md > Inspiration & Identity`:
- **Palette:** Dark Cyber-Cockpit:
  - Canvas Background: Deep obsidian (`#0a0d14`)
  - Cards & Sidebar: Dark slate navy (`#121826`) with 1px border (`#1e293b`)
  - Problem Nodes: Amber / Crimson glow (`#f59e0b` / `#ef4444`)
  - Mitigation Nodes: Cyan electric glow (`#06b6d4`)
  - Solution Nodes: Emerald green glow (`#10b981`)
  - Tag Nodes: Slate blue (`#64748b`)
- **Typography:** Inter / system-ui for UI chrome; Fira Code / monospace for code snippets and technical solutions.
- **Energy:** Tactical, responsive, developer-centric, dark mode by default.

## Components

### 1. Web Application Server (`server.py`)
Serves the REST API endpoints and static frontend assets:
- `GET /`: Serves `static/index.html`.
- `GET /api/graph`: Returns all nodes and edges in Vis-Network format.
- `GET /api/search?q={query}`: Searches episodes and returns matching subgraph.
- `POST /api/episodes`: Creates a new cognitive episode and updates graph edges.
- `POST /api/seed`: Preloads the 3 sanitized generic developer cases.
- `DELETE /api/episodes/{id}`: Removes an episode and orphan tags.
*(Implements `prd.md > Screens and Layout` & `prd.md > Features and Behavior`)*

### 2. Graph & Database Layer (`database.py`)
Manages SQLite operations, schema creation, and relationship extraction:
- Creates tables `episodes` and `edges`.
- Handles full-text keyword indexing and tag node synthesis.
- Exposes clean CRUD methods: `add_episode()`, `get_graph()`, `search_episodes()`, `seed_sample_data()`.
*(Implements `prd.md > States and Boundaries > Persistence`)*

### 3. Model Context Protocol Server (`mcp_server.py`)
Stdio-based JSON-RPC server implementing the MCP specification:
- Exposes `memoria_record` tool.
- Exposes `memoria_recall` tool.
- Connects directly to SQLite so it can run independently or alongside `server.py`.
*(Implements `prd.md > Features and Behavior > 5. Model Context Protocol (MCP) Server Interface`)*

### 4. Frontend Cockpit Visualizer (`static/index.html`, `static/style.css`, `static/app.js`)
Zero-build single-page web app:
- Canvas container hosting Vis-Network force-directed graph.
- Top control header with live search and action triggers.
- Sliding side drawer for node inspection.
- Modal dialog for "+ Teach Memory".
*(Implements `prd.md > Screens and Layout` & `prd.md > Look and Feel`)*

## Data Model

### SQLite Table: `episodes`
| Column | Type | Description |
| :--- | :--- | :--- |
| `id` | `TEXT PRIMARY KEY` | Unique episode identifier (e.g., `ep_1792052023`) |
| `title` | `TEXT NOT NULL` | Concise name of the incident/decision |
| `problem` | `TEXT NOT NULL` | Detailed description of the roadblock/bug |
| `mitigation` | `TEXT NOT NULL` | Step-by-step heuristic or troubleshooting actions taken |
| `solution` | `TEXT NOT NULL` | Verified code fix or permanent configuration |
| `tags` | `TEXT` | Comma-separated domain tags (e.g. `jwt,api,auth`) |
| `created_at` | `TIMESTAMP` | ISO-8601 creation timestamp |

### SQLite Table: `edges`
| Column | Type | Description |
| :--- | :--- | :--- |
| `id` | `INTEGER PRIMARY KEY AUTOINCREMENT` | Edge ID |
| `source` | `TEXT NOT NULL` | Source node ID |
| `target` | `TEXT NOT NULL` | Target node ID |
| `relation` | `TEXT NOT NULL` | Relationship label (`MITIGATED_BY`, `SOLVED_BY`, `TAGGED_WITH`) |

## File Structure
```text
memoriagraph-lite/
├── devpost/                       # Official Devpost Hackathon documentation
│   ├── learner-profile.md         # Learner context & background (gitignored)
│   ├── scope.md                   # Approved project scope
│   ├── prd.md                     # Approved product requirements
│   └── spec.md                    # Approved technical specification
├── static/                        # Frontend Visualizer (Zero-build)
│   ├── index.html                 # Single-screen cockpit layout
│   ├── style.css                  # Cyber-minimalist dark styling
│   └── app.js                     # Vis-Network graph controller & API client
├── server.py                      # FastAPI application & REST endpoints
├── database.py                    # SQLite schema, graph generation, queries
├── mcp_server.py                  # Model Context Protocol stdio runner
├── sample_data.py                 # Sanitized open-source developer scenarios
├── requirements.txt               # Lightweight Python dependencies
├── README.md                      # Quickstart guide, architecture, demo link
└── .gitignore                     # Git ignore rules (learner profile, env, db)
```

## External Services and Dependencies
- **FastAPI (`>=0.110.0`):** Web framework. Docs: https://fastapi.tiangolo.com/
- **Uvicorn (`>=0.28.0`):** ASGI web server. Docs: https://www.uvicorn.org/
- **Pydantic (`>=2.6.0`):** Data validation. Docs: https://docs.pydantic.dev/
- **Vis-Network (`>=9.1.2`):** Graph visualization via CDN (`https://unpkg.com/vis-network/standalone/umd/vis-network.min.js`).

Cost: **$0.00** (100% free and open-source).  
API Keys Required: **None** (zero cloud dependencies).

## Important Failure Modes
1. **Network Disconnected while loading CDN:**  
   *Fallback:* Include an inline graceful fallback alert informing the user, and vendor a minimal standalone copy or simple SVG/Canvas fallback if CDN is unreachable.
2. **Corrupted or Locked SQLite file:**  
   *Fallback:* `database.py` wraps database writes in context managers with timeout protection and returns HTTP 500 with user-friendly error messages rather than crashing the server.
3. **Empty Search Query:**  
   *Fallback:* Resets the graph camera without errors or state anomalies.

## What Was Simplified and Why
- **SQLite instead of Neo4j:** Simplified from full Neo4j graph cluster to embedded SQLite + derived in-memory graph. *Reason:* Enables anyone (especially hackathon judges) to run the project in 5 seconds with zero external database setup.
- **Zero-Build Vanilla JS instead of React/Next.js/Vite:** *Reason:* Avoids npm dependency hell, node version mismatches, and build wait times. The entire frontend runs directly from FastAPI static mount.
- **Synthesized Graph Edges instead of complex manual graph algebra:** *Reason:* Triads (`Problem -> Mitigation -> Solution`) automatically generate directional edges without forcing users to manually map vertexes and edges.

## Decisions and Open Issues
- **Decision:** Use standard stdio for the MCP server so any developer using Claude Code or Cursor can add it as a local CLI tool with zero configuration.
- **Decision:** Sample cases are strictly sanitized generic developer scenarios (zero private internal data).
- **Verification Plan:** Every endpoint and MCP tool will be verified via direct HTTP tests and automated verification scripts in `5-build`.
