from aiogram import Dispatcher
from aiogram.types import Message

from telegram_bot.config import Config
from telegram_bot.handlers.base import BaseHandler


class UserHandler(BaseHandler):
    def __init__(self, dp: Dispatcher):
        self._general_filters = {}
        super().__init__(dp)

    @staticmethod
    async def user_start(message: Message, config: Config):
        await message.answer(f"Приветствую, {message.chat.first_name}!")


    @staticmethod
    async def default_message(message: Message):
        await message.answer('Вы можете использовать следующие команды:\n\n'
                             '/start - стартовое сообщение бота\n'
                             'По остальным вопросам пишите <a href=\"https://t.me/Fulkerson\">Поддержке</a>')

    def register_methods(self):
        self.dp.register_message_handler(UserHandler.user_start, commands=["start"], state="*", **self._general_filters)
        self.dp.register_message_handler(UserHandler.default_message, **self._general_filters)
