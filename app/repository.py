from app.config import DEFAULT_EMBED_COLOR
from app.database import get_connection


def add_role(guild_id, channel_id, emoji, role_id, description):
    with get_connection() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO reaction_roles VALUES (?, ?, ?, ?, ?)",
            (guild_id, channel_id, emoji, role_id, description),
        )
        conn.commit()


def delete_role(guild_id, channel_id, role_id):
    with get_connection() as conn:
        conn.execute(
            "DELETE FROM reaction_roles WHERE guild_id=? AND channel_id=? AND role_id=?",
            (guild_id, channel_id, role_id),
        )
        conn.commit()


def delete_role_by_emoji(guild_id, channel_id, emoji):
    with get_connection() as conn:
        conn.execute(
            "DELETE FROM reaction_roles WHERE guild_id=? AND channel_id=? AND emoji=?",
            (guild_id, channel_id, emoji),
        )
        conn.commit()


def get_roles(guild_id, channel_id):
    with get_connection() as conn:
        return conn.execute(
            """
            SELECT emoji, role_id, description
            FROM reaction_roles
            WHERE guild_id=? AND channel_id=?
            """,
            (guild_id, channel_id),
        ).fetchall()


def get_role_by_emoji(guild_id, channel_id, emoji):
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT role_id
            FROM reaction_roles
            WHERE guild_id=? AND channel_id=? AND emoji=?
            """,
            (guild_id, channel_id, emoji),
        ).fetchone()
        return row[0] if row else None


def save_panel(guild_id, channel_id, message_id):
    with get_connection() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO reaction_panels VALUES (?, ?, ?)",
            (guild_id, channel_id, message_id),
        )
        conn.commit()


def get_panel_by_channel(guild_id, channel_id):
    with get_connection() as conn:
        return conn.execute(
            """
            SELECT message_id
            FROM reaction_panels
            WHERE guild_id=? AND channel_id=?
            """,
            (guild_id, channel_id),
        ).fetchone()


def get_panel_channel(guild_id, message_id):
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT channel_id
            FROM reaction_panels
            WHERE guild_id=? AND message_id=?
            """,
            (guild_id, message_id),
        ).fetchone()
        return row[0] if row else None


def delete_panel_by_channel(guild_id, channel_id):
    with get_connection() as conn:
        conn.execute(
            """
            DELETE FROM reaction_panels
            WHERE guild_id=? AND channel_id=?
            """,
            (guild_id, channel_id),
        )
        conn.commit()


def get_embed_color(guild_id, channel_id):
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT embed_color
            FROM channel_settings
            WHERE guild_id=? AND channel_id=?
            """,
            (guild_id, channel_id),
        ).fetchone()

        if row:
            return row[0]

        row = conn.execute(
            "SELECT embed_color FROM guild_settings WHERE guild_id=?",
            (guild_id,),
        ).fetchone()
        return row[0] if row else DEFAULT_EMBED_COLOR


def set_embed_color(guild_id, channel_id, color):
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO channel_settings (guild_id, channel_id, embed_color)
            VALUES (?, ?, ?)
            ON CONFLICT(guild_id, channel_id) DO UPDATE SET embed_color=excluded.embed_color
            """,
            (guild_id, channel_id, color),
        )
        conn.commit()
