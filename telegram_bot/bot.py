import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from telegram_bot.config import Config
from telegram_bot.handlers.error_handler import ErrorHandler
from telegram_bot.handlers.user_handler import UserHandler
from telegram_bot.middlewares.acl_middleware import ACLMiddleware
from telegram_bot.middlewares.environment_middleware import EnvironmentMiddleware
from telegram_bot.persistance.db import setup

logger = logging.getLogger(__name__)
handlers = []


class Main:

    @staticmethod
    def register_all_middlewares(dp, config):
        dp.setup_middleware(EnvironmentMiddleware(config=config))
        dp.setup_middleware(ACLMiddleware())

    @staticmethod
    def register_all_filters(dp):
        # dp.filters_factory.bind(IsAdminFilter)
        # dp.filters_factory.bind(BotAccessFilter)
        pass

    @staticmethod
    def register_all_handlers(dp):
        handlers.append(UserHandler(dp))
        handlers.append(ErrorHandler(dp))

    @staticmethod
    async def main():
        logging.basicConfig(
            level=logging.INFO,
            format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
            # filename='tgbot.log'
        )
        logger.info("Starting bot")
        config = Config.get_instance(".env")

        storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
        bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
        dp = Dispatcher(bot, storage=storage)

        bot['config'] = config

        Main.register_all_middlewares(dp, config)
        Main.register_all_filters(dp)
        Main.register_all_handlers(dp)

        await setup(
            f'postgresql+asyncpg://{config.db.user}:{config.db.password}@{config.db.host}/{config.db.database}?client_encoding=utf8')
        try:
            await dp.start_polling()
        finally:
            await dp.storage.close()
            await dp.storage.wait_closed()
            await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(Main.main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
