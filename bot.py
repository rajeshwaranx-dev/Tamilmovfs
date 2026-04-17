# ────────────────────────────────────────────────────────────────
# ✅ THIS PROJECT IS DEVELOPED AND MAINTAINED BY @trinityXmods (TELEGRAM)
# 🚫 DO NOT REMOVE OR ALTER THIS CREDIT LINE UNDER ANY CIRCUMSTANCES.
# ⭐ FOR MORE HIGH-QUALITY OPEN-SOURCE BOTS, FOLLOW US ON GITHUB.
# 🔗 OFFICIAL GITHUB: https://github.com/Trinity-Mods
# 📩 NEED HELP OR HAVE QUESTIONS? REACH OUT VIA TELEGRAM: @velvetexams
# ────────────────────────────────────────────────────────────────

from aiohttp import web
from database.database import full_adminbase, get_db_channels, add_db_channel
from plugins import web_server
from pyrogram import Client
from pyrogram.enums import ParseMode
from pyrogram.raw import functions
import sys
from pyromod import listen
from pyromod.listen import ListenerTypes
from datetime import datetime

from config import ADMINS, API_HASH, APP_ID, LOGGER, TG_BOT_TOKEN, TG_BOT_WORKERS, FORCE_SUB_CHANNEL, FORCE_SUB_CHANNEL2, FORCE_SUB_CHANNEL3, FORCE_SUB_CHANNEL4, CHANNEL_ID, PORT, OWNER_ID

from pyrogram import utils

def get_peer_type_new(peer_id: int) -> str:
    peer_id_str = str(peer_id)
    if not peer_id_str.startswith("-"):
        return "user"
    elif peer_id_str.startswith("-100"):
        return "channel"
    else:
        return "chat"
utils.get_peer_type = get_peer_type_new


class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Bot",
            api_hash=API_HASH,
            api_id=APP_ID,
            plugins={"root": "plugins"},
            workers=TG_BOT_WORKERS,
            bot_token=TG_BOT_TOKEN
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()

        # Fix pyromod KeyError bug
        for lt in ListenerTypes:
            if lt not in self.listeners:
                self.listeners[lt] = []

        await self.invoke(functions.updates.GetState())

        usr_bot_me = await self.get_me()
        self.uptime = datetime.now()
        print(ADMINS)

        if FORCE_SUB_CHANNEL:
            try:
                link = (await self.get_chat(FORCE_SUB_CHANNEL)).invite_link
                if not link:
                    await self.export_chat_invite_link(FORCE_SUB_CHANNEL)
                    link = (await self.get_chat(FORCE_SUB_CHANNEL)).invite_link
                self.invitelink = link
            except Exception as a:
                self.LOGGER(__name__).warning(a)
                self.LOGGER(__name__).warning(f"FORCE_SUB_CHANNEL error: {FORCE_SUB_CHANNEL}")
                sys.exit()

        if FORCE_SUB_CHANNEL2:
            try:
                link = (await self.get_chat(FORCE_SUB_CHANNEL2)).invite_link
                if not link:
                    await self.export_chat_invite_link(FORCE_SUB_CHANNEL2)
                    link = (await self.get_chat(FORCE_SUB_CHANNEL2)).invite_link
                self.invitelink2 = link
            except Exception as a:
                self.LOGGER(__name__).warning(a)
                self.LOGGER(__name__).warning(f"FORCE_SUB_CHANNEL2 error: {FORCE_SUB_CHANNEL2}")
                sys.exit()

        if FORCE_SUB_CHANNEL3:
            try:
                link = (await self.get_chat(FORCE_SUB_CHANNEL3)).invite_link
                if not link:
                    await self.export_chat_invite_link(FORCE_SUB_CHANNEL3)
                    link = (await self.get_chat(FORCE_SUB_CHANNEL3)).invite_link
                self.invitelink3 = link
            except Exception as a:
                self.LOGGER(__name__).warning(a)
                self.LOGGER(__name__).warning(f"FORCE_SUB_CHANNEL3 error: {FORCE_SUB_CHANNEL3}")
                sys.exit()

        if FORCE_SUB_CHANNEL4:
            try:
                link = (await self.get_chat(FORCE_SUB_CHANNEL4)).invite_link
                if not link:
                    await self.export_chat_invite_link(FORCE_SUB_CHANNEL4)
                    link = (await self.get_chat(FORCE_SUB_CHANNEL4)).invite_link
                self.invitelink4 = link
            except Exception as a:
                self.LOGGER(__name__).warning(a)
                self.LOGGER(__name__).warning(f"FORCE_SUB_CHANNEL4 error: {FORCE_SUB_CHANNEL4}")
                sys.exit()

        try:
            saved_channels = await get_db_channels()
            if not saved_channels:
                await add_db_channel(CHANNEL_ID)
                saved_channels = [CHANNEL_ID]
            self.db_channels = []
            for ch_id in saved_channels:
                ch = await self.get_chat(ch_id)
                self.db_channels.append(ch)
                test = await self.send_message(chat_id=ch.id, text="Test Message")
                await test.delete()
            self.db_channel = self.db_channels[0]
        except Exception as e:
            self.LOGGER(__name__).warning(e)
            self.LOGGER(__name__).warning(f"DB Channel error: {e}")
            sys.exit()

        initadmin = await full_adminbase()
        for x in initadmin:
            if x in ADMINS:
                continue
            ADMINS.append(x)

        await self.send_message(chat_id=OWNER_ID, text="Bot has started! 😉")
        self.set_parse_mode(ParseMode.HTML)
        self.LOGGER(__name__).info(f"Bot made by @the_universal_being!")
        self.username = usr_bot_me.username

        app = web.AppRunner(await web_server())
        await app.setup()
        await web.TCPSite(app, "0.0.0.0", PORT).start()

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped. contact @the_universal_being")
