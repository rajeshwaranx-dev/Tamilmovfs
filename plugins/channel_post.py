# ────────────────────────────────────────────────────────────────
# ✅ THIS PROJECT IS DEVELOPED AND MAINTAINED BY @trinityXmods (TELEGRAM)
# 🚫 DO NOT REMOVE OR ALTER THIS CREDIT LINE UNDER ANY CIRCUMSTANCES.
# ⭐ FOR MORE HIGH-QUALITY OPEN-SOURCE BOTS, FOLLOW US ON GITHUB.
# 🔗 OFFICIAL GITHUB: https://github.com/Trinity-Mods
# 📩 NEED HELP OR HAVE QUESTIONS? REACH OUT VIA TELEGRAM: @velvetexams
# ────────────────────────────────────────────────────────────────
# 🔒 PRIVATE BOT — Creates links only. Does NOT send files to users.
# ────────────────────────────────────────────────────────────────
import asyncio
import base64
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
from bot import Bot
from config import ADMINS, DISABLE_CHANNEL_BUTTON, USER_REPLY_TEXT


def is_media(message: Message) -> bool:
    return bool(
        message.document or message.video or message.audio or
        message.photo or message.animation or message.voice or
        message.video_note or message.sticker
    )


async def is_db_channel(_, client, message):
    return message.chat.id in [ch.id for ch in getattr(client, 'db_channels', [])]

dynamic_channel_filter = filters.create(is_db_channel)


@Bot.on_message(filters.private & ~filters.user(ADMINS) & ~filters.command(['start']))
async def user_reply(client: Client, message: Message):
    await message.reply_text(USER_REPLY_TEXT, quote=True, disable_web_page_preview=True)


@Bot.on_message(filters.private & filters.user(ADMINS) & ~filters.command(['start','users','broadcast','batch','genlink','stats','auth_secret','deauth_secret', 'auth', 'sbatch', 'exit', 'add_admin', 'del_admin', 'admins', 'add_prem', 'ping', 'restart', 'ch2l', 'cancel']))
async def channel_post(client: Client, message: Message):
    if not is_media(message):
        await message.reply_text("❌ Only files/media can be stored.\nPlain text messages are ignored.", quote=True)
        return

    reply_text = await message.reply_text("Please Wait...! 🫷", quote=True)

    db_channels = getattr(client, 'db_channels', [client.db_channel])
    links = []

    for db_ch in db_channels:
        try:
            post_message = await message.copy(chat_id=db_ch.id, disable_notification=True)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            post_message = await message.copy(chat_id=db_ch.id, disable_notification=True)
        except Exception as e:
            print(e)
            continue

        fs_param = "fs_" + base64.b64encode(str(post_message.id).encode()).decode()
        link = f"https://t.me/{client.username}?start={fs_param}"
        links.append((db_ch.title or str(db_ch.id), link))

        if not DISABLE_CHANNEL_BUTTON:
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Get File", url=link)]])
            try:
                await post_message.edit_reply_markup(reply_markup)
            except FloodWait as e:
                await asyncio.sleep(e.value)
                await post_message.edit_reply_markup(reply_markup)
            except Exception:
                pass

    if not links:
        await reply_text.edit_text("Something went Wrong..!")
        return

    buttons = [[InlineKeyboardButton(f"📁 {title}", url=lnk)] for title, lnk in links]
    text = "<b>Here are your links:</b>\n\n" + "\n".join(f"• <a href='{lnk}'>{title}</a>" for title, lnk in links)
    await reply_text.edit(text, reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)


@Bot.on_message(filters.channel & filters.incoming & dynamic_channel_filter)
async def new_post(client: Client, message: Message):
    if DISABLE_CHANNEL_BUTTON:
        return
    if not is_media(message):
        return

    await asyncio.sleep(4)

    fs_param = "fs_" + base64.b64encode(str(message.id).encode()).decode()
    link = f"https://t.me/{client.username}?start={fs_param}"

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Get File", url=link)]])
    try:
        await message.edit_reply_markup(reply_markup)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        await message.edit_reply_markup(reply_markup)
    except Exception:
        pass

# ────────────────────────────────────────────────────────────────
# ✅ THIS PROJECT IS DEVELOPED AND MAINTAINED BY @trinityXmods (TELEGRAM)
# 🚫 DO NOT REMOVE OR ALTER THIS CREDIT LINE UNDER ANY CIRCUMSTANCES.
# ⭐ FOR MORE HIGH-QUALITY OPEN-SOURCE BOTS, FOLLOW US ON GITHUB.
# 🔗 OFFICIAL GITHUB: https://github.com/Trinity-Mods
# 📩 NEED HELP OR HAVE QUESTIONS? REACH OUT VIA TELEGRAM: @velvetexams
# ────────────────────────────────
