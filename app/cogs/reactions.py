import discord
from discord.ext import commands

from app.repository import get_panel_channel, get_role_by_emoji


class ReactionsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.guild_id is None:
            return

        if self.bot.user and payload.user_id == self.bot.user.id:
            return

        channel_id = get_panel_channel(payload.guild_id, payload.message_id)
        if channel_id is None:
            return

        guild = self.bot.get_guild(payload.guild_id)
        if guild is None:
            return

        role_id = get_role_by_emoji(guild.id, channel_id, str(payload.emoji))
        if role_id is None:
            return

        role = guild.get_role(role_id)
        if role is None:
            return

        member = guild.get_member(payload.user_id) or await guild.fetch_member(payload.user_id)
        await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        if payload.guild_id is None:
            return

        channel_id = get_panel_channel(payload.guild_id, payload.message_id)
        if channel_id is None:
            return

        guild = self.bot.get_guild(payload.guild_id)
        if guild is None:
            return

        role_id = get_role_by_emoji(guild.id, channel_id, str(payload.emoji))
        if role_id is None:
            return

        role = guild.get_role(role_id)
        if role is None:
            return

        member = guild.get_member(payload.user_id) or await guild.fetch_member(payload.user_id)
        await member.remove_roles(role)
