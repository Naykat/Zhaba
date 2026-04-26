import discord

from app.repository import delete_panel_by_channel, get_panel_by_channel


async def delete_old_panel_in_channel(guild: discord.Guild, channel: discord.TextChannel):
    row = get_panel_by_channel(guild.id, channel.id)
    if row is None:
        return

    try:
        message = await channel.fetch_message(row[0])
        await message.delete()
    except Exception:
        pass

    delete_panel_by_channel(guild.id, channel.id)
