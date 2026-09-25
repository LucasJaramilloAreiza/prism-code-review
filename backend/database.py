import json
from typing import Optional
import aiosqlite

DB_PATH = "prism.db"

async def init_db() -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                id TEXT PRIMARY KEY,
                pr_url TEXT NOT NULL,
                pr_title TEXT,
                mode TEXT NOT NULL,
                critical_count INTEGER DEFAULT 0,
                medium_count INTEGER DEFAULT 0,
                low_count INTEGER DEFAULT 0,
                report_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        await db.commit()

async def save_report(report) -> None:
    counts = {"critical": 0, "medium": 0, "low": 0}
    for agent in report.agents:
        for f in agent.findings:
            counts[f.severity.value] += 1
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR REPLACE INTO reviews (id, pr_url, pr_title, mode, critical_count, medium_count, low_count, report_json, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (report.id, report.pr_url, report.pr_title, report.mode,
             counts["critical"], counts["medium"], counts["low"],
             report.model_dump_json(), report.created_at.isoformat())
        )
        await db.commit()

async def get_history(limit: int = 20, offset: int = 0) -> list[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT id, pr_url, pr_title, mode, critical_count, medium_count, low_count, created_at FROM reviews ORDER BY created_at DESC LIMIT ? OFFSET ?",
            (limit, offset)
        ) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
