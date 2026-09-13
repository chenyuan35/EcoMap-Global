import os
import sqlite3
from pathlib import Path

DB_PATH = Path(os.getenv("ECOMAP_DB_PATH", "data/ecomap.db"))

SAMPLE_ROWS = [
    ("Tokyo", "Japan", 35.6762, 139.6503, "temperature", 26.4, "°C", "demo"),
    ("Tokyo", "Japan", 35.6762, 139.6503, "pm25", 12.0, "µg/m³", "demo"),
    ("Singapore", "Singapore", 1.3521, 103.8198, "temperature", 30.1, "°C", "demo"),
    ("Singapore", "Singapore", 1.3521, 103.8198, "pm25", 18.0, "µg/m³", "demo"),
    ("London", "United Kingdom", 51.5072, -0.1276, "temperature", 18.7, "°C", "demo"),
    ("London", "United Kingdom", 51.5072, -0.1276, "pm25", 9.0, "µg/m³", "demo"),
    ("New York", "United States", 40.7128, -74.0060, "temperature", 23.9, "°C", "demo"),
    ("New York", "United States", 40.7128, -74.0060, "pm25", 11.0, "µg/m³", "demo"),
    ("Sydney", "Australia", -33.8688, 151.2093, "temperature", 20.2, "°C", "demo"),
    ("Sydney", "Australia", -33.8688, 151.2093, "pm25", 7.0, "µg/m³", "demo"),
    ("Nairobi", "Kenya", -1.2921, 36.8219, "temperature", 22.5, "°C", "demo"),
    ("Nairobi", "Kenya", -1.2921, 36.8219, "pm25", 16.0, "µg/m³", "demo"),
]


def connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS observations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city TEXT NOT NULL,
                country TEXT NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                metric TEXT NOT NULL,
                value REAL NOT NULL,
                unit TEXT NOT NULL,
                source TEXT NOT NULL,
                observed_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        count = conn.execute("SELECT COUNT(*) FROM observations").fetchone()[0]
        if count == 0:
            conn.executemany(
                """
                INSERT INTO observations
                (city, country, latitude, longitude, metric, value, unit, source)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                SAMPLE_ROWS,
            )
        conn.commit()


def get_observations(metric: str | None = None, limit: int = 500) -> list[dict]:
    sql = "SELECT * FROM observations"
    params: list[object] = []
    if metric:
        sql += " WHERE metric = ?"
        params.append(metric)
    sql += " ORDER BY city, metric LIMIT ?"
    params.append(limit)
    with connect() as conn:
        return [dict(row) for row in conn.execute(sql, params).fetchall()]


def get_summary() -> list[dict]:
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT metric, ROUND(AVG(value), 2) AS average_value,
                   MIN(value) AS min_value, MAX(value) AS max_value,
                   COUNT(*) AS samples, unit
            FROM observations
            GROUP BY metric, unit
            ORDER BY metric
            """
        ).fetchall()
        return [dict(row) for row in rows]
