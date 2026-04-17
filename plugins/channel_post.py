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
