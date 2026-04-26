import sqlite3

from app.config import DB_FILE


def get_connection():
    return sqlite3.connect(DB_FILE)


def init_db():
    with get_connection() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS reaction_roles (
            guild_id INTEGER,
            channel_id INTEGER,
            emoji TEXT,
            role_id INTEGER,
            description TEXT,
            PRIMARY KEY (guild_id, channel_id, emoji)
        )
        """)

        conn.execute("""
        CREATE TABLE IF NOT EXISTS reaction_panels (
            guild_id INTEGER,
            channel_id INTEGER,
            message_id INTEGER,
            PRIMARY KEY (guild_id, channel_id)
        )
        """)

        conn.execute("""
        CREATE TABLE IF NOT EXISTS guild_settings (
            guild_id INTEGER PRIMARY KEY,
            embed_color INTEGER DEFAULT 5793266
        )
        """)

        conn.execute("""
        CREATE TABLE IF NOT EXISTS channel_settings (
            guild_id INTEGER,
            channel_id INTEGER,
            embed_color INTEGER DEFAULT 5793266,
            PRIMARY KEY (guild_id, channel_id)
        )
        """)

        conn.commit()

