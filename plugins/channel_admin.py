from pyrogram import Client, filters
from pyrogram.types import Message
from bot import Bot
from database.database import add_db_channel, remove_db_channel, get_db_channels
from config import OWNER_ID

@Bot.on_message(filters.private & filters.user(OWNER_ID) & filters.command("addgroup"))
async def add_channel(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply("Usage: /addgroup -100xxxxxxxxxx")
        return
    try:
        ch_id = int(message.command[1])
        ch = await client.get_chat(ch_id)
        await add_db_channel(ch_id)
        if not any(c.id == ch_id for c in getattr(client, 'db_channels', [])):
            client.db_channels.append(ch)
            client.db_channel = client.db_channels[0]
        await message.reply(f"✅ Added: {ch.title}\nTotal channels: {len(client.db_channels)}")
    except Exception as e:
        await message.reply(f"❌ Error: {e}")

@Bot.on_message(filters.private & filters.user(OWNER_ID) & filters.command("removegroup"))
async def remove_channel(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply("Usage: /removegroup -100xxxxxxxxxx")
        return
    try:
        ch_id = int(message.command[1])
        await remove_db_channel(ch_id)
        client.db_channels = [c for c in getattr(client, 'db_channels', []) if c.id != ch_id]
        if client.db_channels:
            client.db_channel = client.db_channels[0]
        await message.reply(f"✅ Removed. Total channels: {len(client.db_channels)}")
    except Exception as e:
        await message.reply(f"❌ Error: {e}")

@Bot.on_message(filters.private & filters.user(OWNER_ID) & filters.command("listgroup"))
async def list_channels(client: Client, message: Message):
    channels = getattr(client, 'db_channels', [])
    if not channels:
        await message.reply("No channels registered.")
        return
    text = "\n".join(f"• {ch.title} → <code>{ch.id}</code>" for ch in channels)
    await message.reply(f"<b>Registered channels ({len(channels)}):</b>\n{text}")
