"""
database.py — SQLite Graph Engine & Memory Storage for MemoriaGraph Lite.
Derives nodes, cognitive triads, and interconnected tag clusters.
"""

import sqlite3
import datetime
import uuid
import re
from typing import List, Dict, Any, Optional
from sample_data import SAMPLE_EPISODES

DB_PATH = "memoria.db"


def get_connection(db_path: str = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: str = DB_PATH):
    """Initializes SQLite tables for episodes and relational graph edges."""
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS episodes (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                problem TEXT NOT NULL,
                mitigation TEXT NOT NULL,
                solution TEXT NOT NULL,
                tags TEXT,
                created_at TEXT NOT NULL
            )
        """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS edges (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT NOT NULL,
                target TEXT NOT NULL,
                relation TEXT NOT NULL
            )
        """
        )
        conn.commit()


def clean_tags(tags_str: str) -> List[str]:
    """Parses and sanitizes comma-separated tags."""
    if not tags_str:
        return []
    tags = [t.strip().lower() for t in tags_str.split(",") if t.strip()]
    return list(dict.fromkeys(tags))  # Deduplicate while preserving order


def add_episode(
    title: str,
    problem: str,
    mitigation: str,
    solution: str,
    tags: str = "",
    ep_id: Optional[str] = None,
    db_path: str = DB_PATH,
) -> Dict[str, Any]:
    """Adds a cognitive episode and generates directional graph triad edges."""
    if not ep_id:
        ep_id = f"ep_{uuid.uuid4().hex[:8]}"
    
    created_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
    parsed_tags = clean_tags(tags)
    joined_tags = ", ".join(parsed_tags)

    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO episodes (id, title, problem, mitigation, solution, tags, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (ep_id, title.strip(), problem.strip(), mitigation.strip(), solution.strip(), joined_tags, created_at),
        )

        # Remove any existing edges for this episode before re-generating
        cursor.execute("DELETE FROM edges WHERE source LIKE ? OR target LIKE ?", (f"{ep_id}%", f"{ep_id}%"))

        # Generate Triad Edges:
        # Episode Hub -> Problem
        prob_id = f"{ep_id}_prob"
        mit_id = f"{ep_id}_mit"
        sol_id = f"{ep_id}_sol"

        edges_to_insert = [
            (ep_id, prob_id, "HAS_PROBLEM"),
            (prob_id, mit_id, "MITIGATED_BY"),
            (mit_id, sol_id, "SOLVED_BY"),
        ]

        # Connect to shared tag nodes
        for tag in parsed_tags:
            tag_id = f"tag_{re.sub(r'[^a-zA-Z0-9_]', '', tag)}"
            edges_to_insert.append((ep_id, tag_id, "TAGGED_WITH"))

        cursor.executemany(
            """
            INSERT INTO edges (source, target, relation)
            VALUES (?, ?, ?)
        """,
            edges_to_insert,
        )
        conn.commit()

    return {
        "id": ep_id,
        "title": title,
        "problem": problem,
        "mitigation": mitigation,
        "solution": solution,
        "tags": joined_tags,
        "created_at": created_at,
    }


def get_episodes(db_path: str = DB_PATH) -> List[Dict[str, Any]]:
    """Returns all recorded episodes ordered by newest first."""
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM episodes ORDER BY created_at DESC")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def get_episode(ep_id: str, db_path: str = DB_PATH) -> Optional[Dict[str, Any]]:
    """Returns a single episode by ID."""
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM episodes WHERE id = ?", (ep_id,))
        row = cursor.fetchone()
        return dict(row) if row else None


def delete_episode(ep_id: str, db_path: str = DB_PATH) -> bool:
    """Deletes an episode and its associated graph edges."""
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM episodes WHERE id = ?", (ep_id,))
        deleted = cursor.rowcount > 0
        cursor.execute("DELETE FROM edges WHERE source LIKE ? OR target LIKE ?", (f"{ep_id}%", f"{ep_id}%"))
        conn.commit()
        return deleted


def get_graph(db_path: str = DB_PATH) -> Dict[str, Any]:
    """
    Builds the full graph topology formatted for Vis-Network.
    Color coding:
      - Episode Hub: Indigo/Blue
      - Problem: Amber/Red
      - Mitigation: Cyan
      - Solution: Emerald Green
      - Tag: Slate Blue
    """
    episodes = get_episodes(db_path)
    nodes = []
    edges = []
    seen_tags = set()

    for ep in episodes:
        ep_id = ep["id"]
        prob_id = f"{ep_id}_prob"
        mit_id = f"{ep_id}_mit"
        sol_id = f"{ep_id}_sol"

        # Hub Node
        nodes.append(
            {
                "id": ep_id,
                "label": ep["title"][:28] + ("..." if len(ep["title"]) > 28 else ""),
                "group": "episode",
                "title": f"<b>{ep['title']}</b><br>ID: {ep_id}",
                "episode_id": ep_id,
                "raw_data": ep,
            }
        )

        # Problem Node
        nodes.append(
            {
                "id": prob_id,
                "label": "Problem\n" + ep["problem"][:22] + "...",
                "group": "problem",
                "title": f"<b>Problem</b><br>{ep['problem']}",
                "episode_id": ep_id,
            }
        )

        # Mitigation Node
        nodes.append(
            {
                "id": mit_id,
                "label": "Mitigation\n" + ep["mitigation"][:22] + "...",
                "group": "mitigation",
                "title": f"<b>Mitigation Heuristic</b><br>{ep['mitigation']}",
                "episode_id": ep_id,
            }
        )

        # Solution Node
        nodes.append(
            {
                "id": sol_id,
                "label": "Solution\n" + ep["solution"][:22] + "...",
                "group": "solution",
                "title": f"<b>Verified Solution</b><br>{ep['solution']}",
                "episode_id": ep_id,
            }
        )

        # Direct Triad Edges
        edges.append({"from": ep_id, "to": prob_id, "label": "HAS_PROBLEM", "arrows": "to"})
        edges.append({"from": prob_id, "to": mit_id, "label": "MITIGATED_BY", "arrows": "to"})
        edges.append({"from": mit_id, "to": sol_id, "label": "SOLVED_BY", "arrows": "to"})

        # Tag Nodes & Edges
        for tag in clean_tags(ep.get("tags", "")):
            tag_id = f"tag_{re.sub(r'[^a-zA-Z0-9_]', '', tag)}"
            if tag_id not in seen_tags:
                seen_tags.add(tag_id)
                nodes.append(
                    {
                        "id": tag_id,
                        "label": f"#{tag}",
                        "group": "tag",
                        "title": f"Tag: #{tag}",
                    }
                )
            edges.append({"from": ep_id, "to": tag_id, "label": "TAGGED", "arrows": "to", "dashes": True})

    return {"nodes": nodes, "edges": edges, "total_episodes": len(episodes)}


def search_episodes(query: str, db_path: str = DB_PATH) -> List[Dict[str, Any]]:
    """Performs full-text keyword matching across titles, problems, mitigations, solutions, and tags."""
    if not query or not query.strip():
        return get_episodes(db_path)

    query_term = f"%{query.strip().lower()}%"
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * FROM episodes
            WHERE LOWER(title) LIKE ?
               OR LOWER(problem) LIKE ?
               OR LOWER(mitigation) LIKE ?
               OR LOWER(solution) LIKE ?
               OR LOWER(tags) LIKE ?
            ORDER BY created_at DESC
        """,
            (query_term, query_term, query_term, query_term, query_term),
        )
        return [dict(row) for row in cursor.fetchall()]


def seed_sample_data(db_path: str = DB_PATH) -> int:
    """Preloads the 3 generic developer troubleshooting episodes."""
    count = 0
    for item in SAMPLE_EPISODES:
        add_episode(
            title=item["title"],
            problem=item["problem"],
            mitigation=item["mitigation"],
            solution=item["solution"],
            tags=item["tags"],
            ep_id=item["id"],
            db_path=db_path,
        )
        count += 1
    return count
