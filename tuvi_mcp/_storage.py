# -*- coding: utf-8 -*-
"""
(c) 2026 nmhaaa3218 <manh.ha.3218@gmail.com>
"""

import os
import sqlite3

# Determine database directory:
# Priority 1: Environment variable TUVI_DB_PATH
# Priority 2: User home directory ~/.tuvi_mcp/tuvi_horoscopes.db
# Priority 3: Fallback/Default path inside package directory

DB_PATH_ENV = os.environ.get("TUVI_DB_PATH")
if DB_PATH_ENV:
    DB_FILE = DB_PATH_ENV
else:
    try:
        home_dir = os.path.expanduser("~")
        db_dir = os.path.join(home_dir, ".tuvi_mcp")
        os.makedirs(db_dir, exist_ok=True)
        DB_FILE = os.path.join(db_dir, "tuvi_horoscopes.db")
    except Exception:
        # Fallback to package directory if home directory is read-only
        DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tuvi_horoscopes.db")


def get_connection():
    """Get connection to the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database and create tables if they do not exist."""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS horoscopes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                day INTEGER NOT NULL,
                month INTEGER NOT NULL,
                year INTEGER NOT NULL,
                hour INTEGER NOT NULL,
                gender TEXT NOT NULL,
                is_solar BOOLEAN NOT NULL DEFAULT 1,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()


# Run initialization automatically when module is loaded
init_db()


def save_horoscope(
    name: str, day: int, month: int, year: int, hour: int, gender: str, is_solar: bool, notes: str = None
) -> int:
    """Save a horoscope details to the database, returning its id."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO horoscopes (name, day, month, year, hour, gender, is_solar, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (name, day, month, year, hour, gender, 1 if is_solar else 0, notes),
        )
        conn.commit()
        return cursor.lastrowid


def list_saved_horoscopes() -> list:
    """Retrieve all saved horoscopes."""
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT id, name, day, month, year, hour, gender, is_solar, notes, created_at
            FROM horoscopes
            ORDER BY created_at DESC
        """).fetchall()
        return [dict(row) for row in rows]


def _enrich_with_cach_cuc(record: dict) -> dict:
    """Attach evaluated 51-Cách-Cục list to a saved horoscope record.

    The DB row stores birth inputs only; we rebuild the chart from those inputs
    and run the declarative evaluator so the persisted record surfaces the same
    pattern-recognition surface as `generate_horoscope`. Lazy import avoids
    pulling tuvi_calculator when no read occurs.
    """
    if not record:
        return record
    from .tuvi_calculator import get_horoscope_chart

    chart = get_horoscope_chart(
        name=record["name"],
        day=record["day"],
        month=record["month"],
        year=record["year"],
        hour_val=record["hour"],
        gender_val=record["gender"],
        is_solar=bool(record["is_solar"]),
    )
    if isinstance(chart, dict) and "error" not in chart:
        record["cach_cuc"] = chart.get("cach_cuc", [])
    else:
        record["cach_cuc"] = []
    return record


def get_saved_horoscope_by_id(horoscope_id: int) -> dict:
    """Retrieve a saved horoscope by its unique id, with evaluated cách cục list."""
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT id, name, day, month, year, hour, gender, is_solar, notes, created_at
            FROM horoscopes
            WHERE id = ?
        """,
            (horoscope_id,),
        ).fetchone()
        return _enrich_with_cach_cuc(dict(row)) if row else None


def get_saved_horoscope_by_name(name: str) -> dict:
    """Retrieve the latest saved horoscope matching a name, with evaluated cách cục list."""
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT id, name, day, month, year, hour, gender, is_solar, notes, created_at
            FROM horoscopes
            WHERE name = ?
            ORDER BY created_at DESC
            LIMIT 1
        """,
            (name,),
        ).fetchone()
        return _enrich_with_cach_cuc(dict(row)) if row else None


def delete_saved_horoscope_by_id(horoscope_id: int) -> bool:
    """Delete a saved horoscope by id, returns True if deleted."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM horoscopes WHERE id = ?", (horoscope_id,))
        conn.commit()
        return cursor.rowcount > 0
