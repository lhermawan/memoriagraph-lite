---
doc: prd
status: approved
---

# MemoriaGraph Lite — Product Requirements

Lightweight cognitive memory and decision hub for AI coding agents that turns troubleshooting episodes into reusable `Problem -> Mitigation -> Solution` knowledge graphs.  
Source: `scope.md > The Unique Kernel` and `scope.md > The POC Boundary`.

## The Core Journey
1. **Launch & Landing:** The user opens the local web visualizer in their browser (e.g., `http://localhost:8000`).
2. **First-Time Orientation:** On first load (with no data yet), the user sees an inviting empty state with an explanation and a **"Load Sample Cases"** button alongside a **"+ Teach Memory"** button.
3. **Seeding (Optional):** The user clicks "Load Sample Cases" to instantly populate generic developer scenarios (e.g., *JWT Expiration Refresh*, *React Hydration Mismatch*, *Docker OOMKilled 137*), rendering a connected 2D graph.
4. **Visual Exploration:** The user clicks any node on the graph; an inspection sidebar slides open, displaying the full cognitive triad: **Problem Description**, **Mitigation Strategy**, **Verified Solution**, and **Tags**.
5. **Fast Retrieval:** The user searches via the top search bar (e.g., "hydration" or "jwt"); matching nodes and their relationship clusters highlight instantly.
6. **Agent Memory Formation:** An external AI coding agent (via MCP) or a human user (via the web modal) submits a new episode. The graph updates in real time without refreshing the page.
7. **Agent Recall:** A coding agent connects via MCP tool `memoria_recall("jwt token invalid")` and receives structured mitigation guidance to solve an issue autonomously.

## Screens and Layout
A unified single-screen responsive cockpit:
- **Top Header Bar:**
  - Branding: *MemoriaGraph Lite* with live connection status indicator (Active / Listening).
  - Search Input: Real-time keyword filter across problems, mitigations, solutions, and tags.
  - Action Bar: Quick action buttons: **"+ Teach Memory"** and **"Load Sample Cases"** (hidden once data is loaded).
- **Central Canvas (70% viewport width):**
  - Interactive force-directed 2D graph view with zoom, pan, and node drag.
  - Color-coded node system:
    - 🔴/🟠 **Problem Node** (Amber/Red glow)
    - 🔵 **Mitigation Node** (Cyan glow)
    - 🟢 **Solution Node** (Emerald Green glow)
    - ⚪ **Tag/Domain Node** (Muted Slate)
- **Detail Inspector (30% right sidebar, collapsible):**
  - Displays selected node details: Title, Category, Triad breakdown (`Problem -> Mitigation -> Solution`), Timestamp, and Related Cases.
  - Action to delete or copy knowledge snippet for pasting into prompts.
- **"Teach Memory" Modal (Overlay):**
  - Clean input form for beginners to manually feed knowledge:
    - *Problem* (textarea, required)
    - *Mitigation* (textarea, required)
    - *Solution* (textarea, required)
    - *Tags/Domain* (text input, comma-separated)

## Look and Feel
- **Theme:** Cyber-minimalist dark theme (`#0a0d14` background, `#121826` surface cards).
- **Typography:** Modern clean sans-serif (Inter/Geist) paired with monospace (Fira Code) for technical solutions and code snippets.
- **Accents:** High-contrast tactical neon: Cyan (`#06b6d4`), Emerald (`#10b981`), Amber (`#f59e0b`).
- **Graph Motion:** Smooth physics simulation with dampening; glowing edges indicating directional relationships (`SOLVED_BY`, `MITIGATED_BY`).

## Features and Behavior

### 1. Interactive Graph Visualizer
- The user can zoom, pan, and drag nodes to explore relationships.
- Clicking a node highlights its immediate neighborhood (Problem $\to$ Mitigation $\to$ Solution) and dims unrelated nodes.
- Responsive canvas resizing to full window height.

### 2. Search & Filter Bar
- Typing in the search bar dynamically filters visible nodes.
- Highlights matched keywords in the detail sidebar.
- Clear search button resets the camera focus.

### 3. Manual "Teach Memory" Form
- Allows human developers and beginners to manually add cognitive episodes without writing code or configuring an agent.
- Validates that Problem, Mitigation, and Solution are not empty.
- Submitting appends the node to the graph and SQLite store immediately.

### 4. Zero-Friction Sample Cases Loader
- One-click button on the empty state to preload 3 completely generic developer troubleshooting examples:
  - *Example 1:* JWT Expired Token Handling (API Gateway 401).
  - *Example 2:* React SSR Hydration Mismatch (Server vs Client render differences).
  - *Example 3:* Docker Container Exit Code 137 (Out of Memory / OOMKilled limits).
- **Security Rule:** Strictly NO real internal or sensitive operational data included.

### 5. Model Context Protocol (MCP) Server Interface
- Dual tools exposed over stdio/HTTP:
  - `memoria_record`: Accepts `problem`, `mitigation`, `solution`, `tags`.
  - `memoria_recall`: Accepts `query`, returns ranked matching triads.

## States and Boundaries
- **Empty State:** Displayed when database has 0 records. Shows an informational card: *"Your Second Brain is Ready. Teach your first memory or load sample cases."*
- **Active State:** Graph displays all interconnected triads with total count metrics.
- **Search Not Found:** If query yields no matches, canvas shows a subtle *"No matching memories found"* toast without clearing the existing graph.
- **Persistence:** All memories persist locally in a single SQLite database file (`memoria.db`).
- **Privacy Boundary:** 100% local execution. Zero telemetry or external cloud egress.

## Product Decisions
- **Manual Input Form Included:** Decided to include a manual web form so non-agent users or beginners can treat MemoriaGraph Lite as a personal second-brain trainer.
- **Generic-Only Sample Data:** Strictly sanitized, realistic but synthetic open-source developer scenarios to ensure zero leak of private operational knowledge.
- **Single-Screen Cockpit:** All interactions (Search, Graph, Inspector, Modal) happen on one unified screen to avoid multi-page navigation friction.

## What We're Building
1. Web interface (HTML5 + CSS + Canvas/Vis.js) with Search, Graph, Detail Drawer, and Modal.
2. Lightweight REST API backend (Python FastAPI) serving graph data and handling CRUD.
3. Dual-tool MCP server (`memoria_record` and `memoria_recall`).
4. Sample case seeder (`/api/seed`).

## Deferred From the POC
- Multi-user authentication & role permissions.
- Automatic background conversation transcript scrapers.
- Cloud graph database hosting (Neo4j Aura / Cloud DBs).

## Possible Later Enhancements
- Export memory graph to Markdown / Obsidian vault format.
- Visual timeline replay slider showing how agent knowledge evolved over time.

## Non-Goals
- We are NOT building a general-purpose chat interface (this is a memory engine and visualizer, not a ChatGPT clone).
- We are NOT building an unconstrained vector dump of raw conversational logs.

## Open Questions
- None. Requirements are clear, bounded, and testable within the hackathon timeline.
