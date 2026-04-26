import discord
from discord.ext import commands

from app.cogs.admin import AdminCog
from app.cogs.reactions import ReactionsCog
from app.database import init_db
from app.logging_config import logger


class RoleBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=discord.Intents.all(),
        )
        self._commands_synced = False

    async def setup_hook(self):
        init_db()
        logger.info("Database initialized.")

        await self.add_cog(AdminCog(self))
        logger.info("Admin cog loaded.")

        await self.add_cog(ReactionsCog(self))
        logger.info("Reactions cog loaded.")

    async def _force_reset_command_cache(self):
        commands_snapshot = list(self.tree.get_commands())
        logger.info("Resetting slash command cache.")

        self.tree.clear_commands(guild=None)
        await self.tree.sync()

        for guild in self.guilds:
            self.tree.clear_commands(guild=guild)
            await self.tree.sync(guild=guild)

        for command in commands_snapshot:
            self.tree.add_command(command)

        logger.info("Slash command cache reset completed.")

    async def on_ready(self):
        if self._commands_synced:
            logger.info("Bot is ready. Command sync was already completed earlier.")
            return

        try:
            await self._force_reset_command_cache()
            await self.tree.sync()
            logger.info("Global application commands synced.")

            for guild in self.guilds:
                self.tree.copy_global_to(guild=guild)
                await self.tree.sync(guild=guild)
                logger.info("Guild commands synced for guild_id=%s.", guild.id)
        except Exception:
            logger.exception("Failed during startup command synchronization.")

        self._commands_synced = True
        logger.info("Bot is ready as %s.", self.user)


def create_bot():
    return RoleBot()
