---
doc: scope
status: approved
---

# MemoriaGraph Lite

Lightweight cognitive memory and decision hub for AI coding agents that turns raw troubleshooting into reusable `Problem -> Mitigation -> Solution` knowledge graphs.

## The Unique Kernel
Unlike generic chat-history dumpers or raw vector stores that drown in conversation noise, MemoriaGraph Lite distills problem-solving episodes into structured cognitive decision triads: **`Problem -> Mitigation -> Solution`**. When an AI agent encounters a bug, roadblock, or architectural choice, it doesn't pull unstructured text; it retrieves proven heuristics and verified solutions established in past sessions.

## Who It's For
Software engineers and AI agent power-users (working with Claude Code, Cursor, Codex, Antigravity) who are frustrated by agents repeating the same debugging mistakes, re-asking already answered questions, and suffering from session amnesia.

## The Core Loop
1. During a development or debugging task, a problem is resolved.
2. The user or agent triggers `memoria_record`: saving the episode as `Problem -> Mitigation -> Solution` with domain tags.
3. The lightweight backend stores the node and relationship, and the interactive Web Visualizer renders the new connection in real time.
4. In future sessions, when an agent encounters a related challenge, it queries `memoria_recall` via MCP and immediately receives the exact past mitigation and solution.

## Inspiration & Identity
- **Aesthetic:** Dark-mode cyber-minimalist cockpit (inspired by developer HUDs, Vercel/Linear dark themes).
- **Feel:** Fast, tactical, zero-clutter, instant responsiveness.
- **Visualization:** Interactive 2D graph with glowing nodes (Problem = amber/red, Mitigation = cyan, Solution = emerald green) interconnected by directional edges.

## Why This Matters to the Learner
The learner orchestrates autonomous AI agents daily across multi-server environments and cybersecurity workflows. Repetitive mistakes and context loss waste tokens and developer attention. Having a lightweight, portable memory engine ensures hard-won architectural decisions and bug fixes persist permanently across agent sessions.

## What "Working" Looks Like
A crisp 90-second demo:
1. An AI agent in terminal solves an issue (e.g. rate limit / CORS / auth configuration).
2. Agent calls `memoria_record` via MCP to persist the triad: Problem $\rightarrow$ Mitigation $\rightarrow$ Solution.
3. The Web Visualizer running in the browser instantly displays the new node and its graph connections live without page refresh.
4. The agent starts a brand-new, clean conversation context, queries `memoria_recall("auth throttle")`, immediately retrieves the past insight, and avoids the trap on the first try.

## The POC Boundary
- **Lightweight Backend:** Single-process Python (FastAPI + SQLite / in-memory graph index) for zero-dependency local startup.
- **Dual MCP Facade:** Model Context Protocol stdio/HTTP server exposing:
  - `memoria_record`: Store a structured `Problem -> Mitigation -> Solution` episode.
  - `memoria_recall`: Search and retrieve past solutions by query or semantic tags.
- **Interactive Web Visualizer:** Zero-build-step modern web interface (HTML5 + Canvas / Vis.js / Cytoscape) showing real-time nodes and relational links.
- **REST API:** Standard endpoints for UI communication and third-party integration.

## Later
- Deep Neo4j graph database clustering with 4-Way BM25 + Vector RRF scoring.
- Multi-agent shared team synchronization over cloud sync.
- Automated background transcript harvesting (zero-token passive ingestion).

## Explicitly Cut
- **User Authentication / Accounts:** Unnecessary bloat for a local developer tool PoC.
- **Heavy Database Clusters (Neo4j / Pinecone):** Cut in favor of self-contained SQLite / JSON graph to allow instant 1-command startup for any judge.
- **Complex Multi-Step Cognitive Reflection Daemons:** Cut so the agent interacts cleanly via standard MCP tools.
