---
doc: checklist
status: approved
---

# Build Checklist

Build mode: fast

## Slices

- [x] **1. Core SQLite Graph Engine and Generic Sample Seeder**
  Becomes usable: A runnable database engine (`database.py` and `sample_data.py`) that initializes SQLite tables, extracts relational graph nodes and edges (`Problem -> Mitigation -> Solution`), and seeds 3 generic developer incidents.
  Why now: Proves the core data model and graph derivation first, providing the persistence layer needed by the web UI and MCP server.
  PRD ref: `prd.md > The Core Journey` (steps 2-3), `prd.md > Features and Behavior > 4. Zero-Friction Sample Cases Loader`
  Spec ref: `spec.md > Components > 2. Graph & Database Layer`, `spec.md > Data Model`
  Build: Create `requirements.txt`, `database.py`, and `sample_data.py` with episode CRUD, graph edge derivation, keyword search, and sanitized sample seeder.
  Verify (mechanical): Run automated test verifying SQLite schema initialization, sample data seeding of 3 episodes, and extraction of nodes and edges.
  Learner check: Run Python one-liner to print graph nodes and confirm structured `Problem -> Mitigation -> Solution` entities exist.
  Commit: `feat: add core sqlite graph database engine and sample seeder`

- [x] **2. Web Cockpit Visualizer, Interactive Graph, and Manual Entry Form**
  Becomes usable: A running web interface at `http://localhost:8000` with dark-mode cyber styling, Vis-Network physics canvas, search bar, node inspection drawer, and manual "+ Teach Memory" modal form.
  Why now: Delivers the entire human-facing visual experience and manual second-brain training workflow.
  PRD ref: `prd.md > Screens and Layout`, `prd.md > Look and Feel`, `prd.md > Features and Behavior > 1, 2, 3`
  Spec ref: `spec.md > Components > 1. Web Application Server`, `spec.md > Components > 4. Frontend Cockpit Visualizer`
  Build: Create `server.py` (FastAPI) and `static/index.html`, `static/style.css`, and `static/app.js` with responsive graph layout, live search, and modal form.
  Verify (mechanical): Start FastAPI server, curl endpoints (`GET /api/graph`, `POST /api/episodes`, `GET /api/search`), and verify HTTP 200/201 responses with valid JSON payloads.
  Learner check: Open `http://localhost:8000` in browser, click "Load Sample Cases", inspect a node, and submit a new memory via the modal.
  Commit: `feat: implement web visualizer cockpit, graph canvas, and manual entry modal`

- [ ] **3. Dual-Tool Model Context Protocol (MCP) Server for AI Coding Agents**
  Becomes usable: Stdio JSON-RPC server (`mcp_server.py`) exposing `memoria_record` and `memoria_recall` so external AI agents (Claude Code, Cursor, Antigravity) can autonomously store and retrieve solutions.
  Why now: Completes the unique kernel and autonomous agent interoperability loop for the hackathon demo.
  PRD ref: `prd.md > Features and Behavior > 5. Model Context Protocol (MCP) Server Interface`
  Spec ref: `spec.md > Components > 3. Model Context Protocol Server`
  Build: Create `mcp_server.py` implementing MCP stdio JSON-RPC protocol with tool discovery and execution handlers for `memoria_record` and `memoria_recall`.
  Verify (mechanical): Pipe test JSON-RPC payloads into `mcp_server.py` stdio, assert tool listing returns both tools, and verify `memoria_record` and `memoria_recall` execute successfully.
  Learner check: Send mock JSON-RPC query in terminal and verify formatted mitigation and solution output is returned.
  Commit: `feat: implement dual-tool mcp server for ai coding agents`

- [ ] **4. Quickstart Documentation, Demo Script, and Project Polish**
  Becomes usable: Complete `README.md` with 1-command startup instructions, architecture diagrams, MCP configuration examples for Claude/Cursor, and demo video script.
  Why now: Prepares everything required for `6-ship` and project handoff.
  PRD ref: `prd.md > What We're Building`
  Spec ref: `spec.md > Where It Runs and How Someone Tries It`
  Build: Create `README.md` documenting quickstart, MCP setup, API endpoints, and clean startup script.
  Verify (mechanical): Run clean startup check, verify all links and endpoints.
  Learner check: Review `README.md` and test running the full stack with 1 command.
  Commit: `docs: add comprehensive readme with mcp setup and demo guide`

## Hands-on Checkpoints

- [ ] Early usable behavior explored — Slice 2 (Web Visualizer cockpit and graph canvas live in browser)
- [ ] Final kick-the-tires exploration and feedback completed — Slice 4 (Complete end-to-end app and MCP integration)

## Final Review

- [ ] Final review complete — feedback resolved and learner confirms ready to ship

## Code Tour and App Map

- [ ] Learning activity complete — guided route, focused alternative, prior practice connected, or brief recap
- [ ] Optional edit and transfer reflection addressed — offered/declined/already covered/not applicable as appropriate
- [ ] `devpost/app-map.html` generated from finished code, checked, and shown, including a project-grounded practice to reuse

Activity and evidence: [to be recorded upon completion]
Route and stops: [to be recorded upon completion]
Edit outcome: [to be recorded upon completion]
Reflection: [to be recorded upon completion]
Activity mode: [to be recorded upon completion]

## Revisions

