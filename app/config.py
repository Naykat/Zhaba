import os

from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
DB_FILE = "reaction_roles.db"

DEFAULT_EMBED_COLOR = 0x5865F2
SUCCESS_EMBED_COLOR = 0x57F287
ERROR_EMBED_COLOR = 0xED4245
