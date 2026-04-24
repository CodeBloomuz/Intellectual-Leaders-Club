import aiosqlite
from config import DB_PATH


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER UNIQUE,
                username TEXT,
                full_name TEXT,
                fakultet TEXT,
                yonalish TEXT,
                guruh TEXT,
                phone TEXT,
                interest TEXT,
                motivation TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS interviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                time TEXT,
                location TEXT,
                sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()


async def add_user(telegram_id, username, full_name, fakultet, yonalish, guruh, phone, interest, motivation):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT OR REPLACE INTO users
            (telegram_id, username, full_name, fakultet, yonalish, guruh, phone, interest, motivation, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending')
        """, (telegram_id, username, full_name, fakultet, yonalish, guruh, phone, interest, motivation))
        await db.commit()


async def get_user(telegram_id):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,)) as cursor:
            return await cursor.fetchone()


async def get_all_users(status=None):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        if status:
            async with db.execute("SELECT * FROM users WHERE status = ? ORDER BY created_at DESC", (status,)) as cursor:
                return await cursor.fetchall()
        else:
            async with db.execute("SELECT * FROM users ORDER BY created_at DESC") as cursor:
                return await cursor.fetchall()


async def update_status(telegram_id, status):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE users SET status = ? WHERE telegram_id = ?", (status, telegram_id))
        await db.commit()


async def get_stats():
    async with aiosqlite.connect(DB_PATH) as db:
        stats = {}
        for s in ['pending', 'invited', 'accepted', 'rejected', 'probation']:
            async with db.execute("SELECT COUNT(*) FROM users WHERE status = ?", (s,)) as cursor:
                row = await cursor.fetchone()
                stats[s] = row[0]
        async with db.execute("SELECT COUNT(*) FROM users") as cursor:
            row = await cursor.fetchone()
            stats['total'] = row[0]
        return stats


async def save_interview(date, time, location):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO interviews (date, time, location) VALUES (?, ?, ?)",
            (date, time, location)
        )
        await db.commit()


async def user_exists(telegram_id):
    user = await get_user(telegram_id)
    return user is not None
