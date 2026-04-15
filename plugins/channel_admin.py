from pyrogram import Client, filters
from pyrogram.types import ChatMemberUpdated
from bot import Bot
from database.database import add_db_channel, remove_db_channel

@Bot.on_chat_member_updated(filters.channel)
async def bot_promoted_or_demoted(client: Client, update: ChatMemberUpdated):
    bot_id = (await client.get_me()).id

    if not update.new_chat_member or update.new_chat_member.user.id != bot_id:
        return

    ch_id = update.chat.id
    status = str(update.new_chat_member.status)

    if "administrator" in status:
        await add_db_channel(ch_id)
        if not any(ch.id == ch_id for ch in getattr(client, 'db_channels', [])):
            ch = await client.get_chat(ch_id)
            client.db_channels.append(ch)
        client.db_channel = client.db_channels[0]
    elif any(s in status for s in ("left", "banned", "member")):
        await remove_db_channel(ch_id)
        client.db_channels = [ch for ch in getattr(client, 'db_channels', []) if ch.id != ch_id]
        if client.db_channels:
            client.db_channel = client.db_channels[0]
