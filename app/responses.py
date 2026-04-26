import asyncio

import discord

from app.config import ERROR_EMBED_COLOR, SUCCESS_EMBED_COLOR


def ok(text):
    return discord.Embed(description=f"✅ {text}", color=SUCCESS_EMBED_COLOR)


def err(text):
    return discord.Embed(description=f"❌ {text}", color=ERROR_EMBED_COLOR)


async def temp_response(interaction: discord.Interaction, embed: discord.Embed):
    await interaction.response.send_message(embed=embed, ephemeral=True)
    await asyncio.sleep(3)

    try:
        await interaction.delete_original_response()
    except Exception:
        pass


async def temp_followup(interaction: discord.Interaction, embed: discord.Embed):
    msg = await interaction.followup.send(embed=embed, ephemeral=True, wait=True)
    await asyncio.sleep(3)

    try:
        await msg.delete()
    except Exception:
        pass
