import discord
from discord import app_commands
from discord.ext import commands

from app.repository import (
    add_role,
    delete_role,
    delete_role_by_emoji,
    get_embed_color,
    get_role_by_emoji,
    get_roles,
    save_panel,
    set_embed_color,
)
from app.responses import err, ok, temp_followup, temp_response
from app.services import delete_old_panel_in_channel
from app.validators import is_valid_emoji, require_guild, require_text_channel


class AdminCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="add_role", description="Add a reaction role in the current channel")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(emoji="Emoji", role="Role", description="Description")
    async def add(
        self,
        interaction: discord.Interaction,
        emoji: str,
        role: discord.Role,
        description: str,
    ):
        guild = await require_guild(interaction)
        if guild is None:
            return

        channel = await require_text_channel(interaction)
        if channel is None:
            return

        if not is_valid_emoji(emoji, guild):
            return await temp_response(
                interaction,
                err("Invalid emoji. Use a standard emoji or one from this server."),
            )

        existing_role_id = get_role_by_emoji(guild.id, channel.id, emoji)
        if existing_role_id is not None and existing_role_id != role.id:
            existing_role = guild.get_role(existing_role_id)
            if existing_role:
                return await temp_response(
                    interaction,
                    err(f"This emoji is already used for {existing_role.mention} in this channel."),
                )

            return await temp_response(
                interaction,
                err("This emoji is already used for another role in this channel."),
            )

        if guild.me is None or role >= guild.me.top_role:
            return await temp_response(
                interaction,
                err("That role is higher than or equal to the bot's top role."),
            )

        add_role(guild.id, channel.id, emoji, role.id, description)
        await temp_response(interaction, ok(f"{emoji} — {description} added for this channel."))

    @app_commands.command(name="delete_role", description="Delete a reaction role from the current channel")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(role="Role to remove", emoji="Emoji to remove")
    async def delete(
        self,
        interaction: discord.Interaction,
        role: discord.Role | None = None,
        emoji: str | None = None,
    ):
        guild = await require_guild(interaction)
        if guild is None:
            return

        channel = await require_text_channel(interaction)
        if channel is None:
            return

        if role is None and emoji is None:
            return await temp_response(interaction, err("Provide either a role or an emoji to delete."))

        if role is not None and emoji is not None:
            return await temp_response(interaction, err("Provide only one value: either a role or an emoji."))

        if role is not None:
            delete_role(guild.id, channel.id, role.id)
            return await temp_response(interaction, ok(f"Role {role.mention} was removed from this channel."))

        if not is_valid_emoji(emoji, guild):
            return await temp_response(interaction, err("Invalid emoji."))

        role_id = get_role_by_emoji(guild.id, channel.id, emoji)
        if role_id is None:
            return await temp_response(
                interaction,
                err("That emoji was not found in this channel's reaction roles."),
            )

        delete_role_by_emoji(guild.id, channel.id, emoji)
        await temp_response(interaction, ok(f"Emoji {emoji} was removed from this channel."))

    @app_commands.command(name="color", description="Set the reaction panel embed color")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(hex_color="HEX color, for example #5865F2")
    async def color(self, interaction: discord.Interaction, hex_color: str):
        guild = await require_guild(interaction)
        if guild is None:
            return

        channel = await require_text_channel(interaction)
        if channel is None:
            return

        value = hex_color.strip().replace("#", "")
        if len(value) != 6:
            return await temp_response(interaction, err("Color must be in the format #5865F2."))

        try:
            color_value = int(value, 16)
        except ValueError:
            return await temp_response(interaction, err("Invalid HEX color."))

        set_embed_color(guild.id, channel.id, color_value)
        embed = discord.Embed(
            description=f"✅ Color updated: `#{value.upper()}`",
            color=color_value,
        )
        await temp_response(interaction, embed)

    @app_commands.command(name="roles", description="Create a reaction roles panel in the current channel")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(
        title="Embed title",
        description="Embed description",
    )
    async def roles(
        self,
        interaction: discord.Interaction,
        title: str = "Reaction Roles",
        description: str = "Click a reaction to get access to the related channels.",
    ):
        guild = await require_guild(interaction)
        if guild is None:
            return

        channel = await require_text_channel(interaction)
        if channel is None:
            return

        data = get_roles(guild.id, channel.id)
        if not data:
            return await temp_response(interaction, err("No reaction roles are configured in this channel."))

        await interaction.response.defer(ephemeral=True)
        await delete_old_panel_in_channel(guild, channel)

        embed = discord.Embed(
            title=title,
            description=description,
            color=get_embed_color(guild.id, channel.id),
        )

        emojis = []
        for emoji, role_id, role_description in data:
            role = guild.get_role(role_id)
            if role is None:
                continue

            embed.add_field(
                name=f"{emoji} — {role_description}",
                value="\u200b",
                inline=False,
            )
            emojis.append(emoji)

        if not emojis:
            return await temp_followup(
                interaction,
                err("Roles were found in the database for this channel, but they no longer exist on the server."),
            )

        message = await channel.send(embed=embed)
        for emoji in emojis:
            try:
                await message.add_reaction(emoji)
            except Exception:
                pass

        save_panel(guild.id, channel.id, message.id)
        await temp_followup(interaction, ok("Reaction roles panel created in this channel."))

    @app_commands.command(name="clear", description="Delete messages in the current channel")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(amount="Number of messages")
    async def clear(self, interaction: discord.Interaction, amount: int):
        guild = await require_guild(interaction)
        if guild is None:
            return

        if amount < 1 or amount > 100:
            return await temp_response(interaction, err("Provide a number from 1 to 100."))

        channel = await require_text_channel(interaction)
        if channel is None:
            return

        if guild.me is None:
            return await temp_response(interaction, err("Could not determine the bot's member data in this server."))

        permissions = channel.permissions_for(guild.me)
        if not permissions.manage_messages:
            return await temp_response(interaction, err("The bot does not have the Manage Messages permission."))

        if not permissions.read_message_history:
            return await temp_response(interaction, err("The bot does not have the Read Message History permission."))

        await interaction.response.defer(ephemeral=True)
        deleted = await channel.purge(limit=amount, bulk=False)
        await temp_followup(interaction, ok(f"Deleted messages: {len(deleted)}"))

    async def cog_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingPermissions):
            await temp_response(interaction, err("You do not have enough permissions."))
            return

        try:
            await temp_response(interaction, err("An error occurred while executing the command."))
        except Exception:
            pass
