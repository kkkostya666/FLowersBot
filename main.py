import asyncio
import logging

from aiogram.utils.chat_action import ChatActionMiddleware
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config.token import BOT_TOKEN
from handlers.start.start import StartHandler
from handlers.profile.profile import ProfileHandler
from handlers.main_menu.menu import MenuHandler
from handlers.admin.admin_handlers import AdminHandler
from handlers.support.support import SupportHandler
from handlers.catalog.catalog import CatalogHandler
from handlers.admin.newsletter_handlers import NewSletterHandler
from db.db import Db


class MainBot:
    def __init__(self, bot_token: str):
        self.bot = Bot(token=bot_token)
        self.dp = Dispatcher(storage=MemoryStorage())
        self.db = Db(db_name="freelance.db")
        self.start_handler = StartHandler(db=self.db, chat_id=-1002393331487, bot_token=BOT_TOKEN)
        self.profile_handler = ProfileHandler(db=self.db)
        self.main_menu = MenuHandler(db=self.db)
        self.support = SupportHandler(db=self.db, chat_id=-1002393331487, bot_token=BOT_TOKEN)
        self.admin = AdminHandler(db=self.db, chat_id=-1002393331487, bot_token=BOT_TOKEN)
        self.catalog = CatalogHandler(db=self.db, bot_token=BOT_TOKEN, chat_id=-1002393331487)
        self.newsletter = NewSletterHandler(db=self.db, bot_token=BOT_TOKEN, chat_id=-1002393331487)
        self.setup()

    def setup(self):
        self.dp.include_routers(*[self.start_handler.router,
                                  self.profile_handler.router,
                                  self.main_menu.router,
                                  self.admin.router,
                                  self.support.router,
                                  self.catalog.router,
                                  self.newsletter.router])
        self.dp.message.middleware(ChatActionMiddleware())

    async def start(self):
        await self.bot.delete_webhook(drop_pending_updates=True)
        await self.dp.start_polling(self.bot, allowed_updates=self.dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main_bot = MainBot(BOT_TOKEN)
    asyncio.run(main_bot.start())

