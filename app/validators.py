import discord

from app.responses import err, temp_response


def is_valid_emoji(emoji: str, guild: discord.Guild) -> bool:
    emoji = emoji.strip()
    parsed = discord.PartialEmoji.from_str(emoji)

    if parsed.id is not None:
        return discord.utils.get(guild.emojis, id=parsed.id) is not None

    if len(emoji) == 1:
        return not emoji.isalnum()

    if len(emoji) <= 4:
        return not emoji.replace("\ufe0f", "").isalnum()

    return False


async def require_guild(interaction: discord.Interaction):
    if interaction.guild is None:
        await temp_response(interaction, err("This command only works in a server."))
        return None
    return interaction.guild


async def require_text_channel(interaction: discord.Interaction):
    channel = interaction.channel
    if not isinstance(channel, discord.TextChannel):
        await temp_response(interaction, err("This command only works in a text channel."))
        return None
    return channel
