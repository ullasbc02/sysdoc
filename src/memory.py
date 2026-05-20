import sqlite3
from datetime import datetime
from pathlib import Path

from src.config import load_config
from src.agent_state import AgentState


def get_db_path() -> Path:
    config = load_config()
    return Path(config["memory"]["sqlite_db"])


def init_memory_db() -> None:
    db_path = get_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS investigations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                user_query TEXT NOT NULL,
                final_answer TEXT,
                steps_count INTEGER NOT NULL
            )
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS investigation_steps (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                investigation_id INTEGER NOT NULL,
                iteration INTEGER NOT NULL,
                thought TEXT,
                action TEXT,
                command TEXT,
                observation TEXT,
                FOREIGN KEY (investigation_id)
                    REFERENCES investigations(id)
            )
            """
        )


def save_investigation(state: AgentState) -> int:
    init_memory_db()

    with sqlite3.connect(get_db_path()) as conn:
        cursor = conn.execute(
            """
            INSERT INTO investigations (
                timestamp,
                user_query,
                final_answer,
                steps_count
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                datetime.now().isoformat(),
                state.user_query,
                state.final_answer,
                len(state.steps),
            ),
        )

        investigation_id = cursor.lastrowid

        for step in state.steps:
            conn.execute(
                """
                INSERT INTO investigation_steps (
                    investigation_id,
                    iteration,
                    thought,
                    action,
                    command,
                    observation
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    investigation_id,
                    step.iteration,
                    step.thought,
                    step.action,
                    step.command,
                    step.observation,
                ),
            )

        return investigation_id


def list_recent_investigations(limit: int = 5) -> list[dict]:
    init_memory_db()

    with sqlite3.connect(get_db_path()) as conn:
        conn.row_factory = sqlite3.Row

        rows = conn.execute(
            """
            SELECT id, timestamp, user_query, final_answer, steps_count
            FROM investigations
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

        return [dict(row) for row in rows]


def search_similar_investigations(query: str, limit: int = 3) -> list[dict]:
    init_memory_db()

    keywords = [
        word.lower()
        for word in query.split()
        if len(word) > 3
    ]

    if not keywords:
        return []

    with sqlite3.connect(get_db_path()) as conn:
        conn.row_factory = sqlite3.Row

        rows = conn.execute(
            """
            SELECT id, timestamp, user_query, final_answer, steps_count
            FROM investigations
            ORDER BY id DESC
            LIMIT 25
            """
        ).fetchall()

        scored = []

        for row in rows:
            text = f"{row['user_query']} {row['final_answer']}".lower()

            score = sum(1 for keyword in keywords if keyword in text)

            if score > 0:
                item = dict(row)
                item["score"] = score
                scored.append(item)

        scored.sort(key=lambda x: x["score"], reverse=True)

        return scored[:limit]
