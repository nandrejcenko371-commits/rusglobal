from __future__ import annotations

import aiosqlite
from datetime import datetime, timezone
from config import DB_PATH


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id     INTEGER PRIMARY KEY,
                username    TEXT,
                first_name  TEXT,
                last_name   TEXT,
                started_at  TEXT NOT NULL,
                is_active   INTEGER DEFAULT 1
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS warmup_log (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id  INTEGER NOT NULL,
                day_num  INTEGER NOT NULL,
                sent_at  TEXT NOT NULL,
                UNIQUE(user_id, day_num),
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS kev_registrations (
                user_id        INTEGER PRIMARY KEY,
                name           TEXT NOT NULL,
                phone          TEXT,
                registered_at  TEXT NOT NULL,
                reminder_sent  INTEGER DEFAULT 0,
                zoom_sent      INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                user_id                 INTEGER PRIMARY KEY,
                inv_id                  INTEGER UNIQUE,
                amount                  REAL,
                status                  TEXT DEFAULT 'pending',
                edvibe_login            TEXT,
                edvibe_password         TEXT,
                paid_at                 TEXT,
                marathon_reminder_sent  INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        await db.commit()


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


# ── Users ──────────────────────────────────────────────────────────────────

async def add_user(user_id: int, username: str, first_name: str, last_name: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (user_id, username, first_name, last_name, started_at) VALUES (?, ?, ?, ?, ?)",
            (user_id, username, first_name, last_name, _now()),
        )
        await db.commit()


async def get_user(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)) as cur:
            row = await cur.fetchone()
            return dict(row) if row else None


async def get_all_active_users():
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM users WHERE is_active = 1") as cur:
            return [dict(r) for r in await cur.fetchall()]


# ── Warm-up ────────────────────────────────────────────────────────────────

async def warmup_sent(user_id: int, day_num: int) -> bool:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT 1 FROM warmup_log WHERE user_id = ? AND day_num = ?", (user_id, day_num)
        ) as cur:
            return await cur.fetchone() is not None


async def mark_warmup_sent(user_id: int, day_num: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO warmup_log (user_id, day_num, sent_at) VALUES (?, ?, ?)",
            (user_id, day_num, _now()),
        )
        await db.commit()


# ── KEV ───────────────────────────────────────────────────────────────────

async def register_kev(user_id: int, name: str, phone: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR REPLACE INTO kev_registrations (user_id, name, phone, registered_at) VALUES (?, ?, ?, ?)",
            (user_id, name, phone, _now()),
        )
        await db.commit()


async def is_kev_registered(user_id: int) -> bool:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT 1 FROM kev_registrations WHERE user_id = ?", (user_id,)) as cur:
            return await cur.fetchone() is not None


async def get_kev_users_pending(field: str) -> list[int]:
    """field: 'reminder_sent' or 'zoom_sent'"""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(f"SELECT user_id FROM kev_registrations WHERE {field} = 0") as cur:
            return [r[0] for r in await cur.fetchall()]


async def mark_kev_flag(user_id: int, field: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(f"UPDATE kev_registrations SET {field} = 1 WHERE user_id = ?", (user_id,))
        await db.commit()


# ── Payments ──────────────────────────────────────────────────────────────

async def create_payment(user_id: int, inv_id: int, amount: float):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR REPLACE INTO payments (user_id, inv_id, amount, status) VALUES (?, ?, ?, 'pending')",
            (user_id, inv_id, amount),
        )
        await db.commit()


async def get_payment_by_inv(inv_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM payments WHERE inv_id = ?", (inv_id,)) as cur:
            row = await cur.fetchone()
            return dict(row) if row else None


async def mark_payment_paid_pending_access(inv_id: int):
    """Robokassa confirmed — money received, waiting for admin to issue Edvibe access."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE payments SET status='paid_pending', paid_at=? WHERE inv_id=?",
            (_now(), inv_id),
        )
        await db.commit()


async def confirm_payment(user_id: int, login: str, password: str):
    """Admin issued Edvibe credentials — mark fully complete."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE payments SET status='paid', edvibe_login=?, edvibe_password=? WHERE user_id=?",
            (login, password, user_id),
        )
        await db.commit()


async def get_user_payment(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM payments WHERE user_id = ?", (user_id,)) as cur:
            row = await cur.fetchone()
            return dict(row) if row else None


async def get_paid_users_pending_reminder() -> list[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM payments WHERE status='paid' AND marathon_reminder_sent=0"
        ) as cur:
            return [dict(r) for r in await cur.fetchall()]


async def mark_marathon_reminder_sent(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE payments SET marathon_reminder_sent=1 WHERE user_id=?", (user_id,))
        await db.commit()
