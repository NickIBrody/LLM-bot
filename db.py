import sqlite3, time
from pathlib import Path

DB = Path("/root/pybot/users.db")

def conn():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    return c

def init():
    with conn() as c:
        c.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id          INTEGER PRIMARY KEY,
                name        TEXT,
                username    TEXT,
                access      INTEGER DEFAULT 0,
                is_admin    INTEGER DEFAULT 0,
                paid_at     INTEGER,
                granted_at  INTEGER,
                granted_by  TEXT,
                first_seen  INTEGER,
                stars       INTEGER DEFAULT 0
            )
        """)

def get(uid: int):
    with conn() as c:
        return c.execute("SELECT * FROM users WHERE id=?", (uid,)).fetchone()

def upsert(uid: int, **kw):
    with conn() as c:
        exists = c.execute("SELECT 1 FROM users WHERE id=?", (uid,)).fetchone()
        if exists:
            sets = ", ".join(f"{k}=?" for k in kw)
            c.execute(f"UPDATE users SET {sets} WHERE id=?", (*kw.values(), uid))
        else:
            kw.setdefault("first_seen", int(time.time()))
            kw["id"] = uid
            cols = ", ".join(kw.keys())
            vals = ", ".join("?" * len(kw))
            c.execute(f"INSERT INTO users ({cols}) VALUES ({vals})", tuple(kw.values()))

def grant(uid: int, by: str):
    upsert(uid, access=1, granted_at=int(time.time()), granted_by=str(by))

def revoke(uid: int):
    upsert(uid, access=0)

def has_access(uid: int) -> bool:
    row = get(uid)
    return bool(row and row["access"])

def all_users():
    with conn() as c:
        return c.execute("SELECT * FROM users ORDER BY first_seen DESC").fetchall()

def stats():
    with conn() as c:
        total = c.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        active = c.execute("SELECT COUNT(*) FROM users WHERE access=1").fetchone()[0]
        paid = c.execute("SELECT COUNT(*) FROM users WHERE paid_at IS NOT NULL").fetchone()[0]
        return {"total": total, "active": active, "paid": paid}

init()
