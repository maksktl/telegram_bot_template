import logging
from typing import Optional
from uuid import UUID

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from telegram_bot.services.dto.user_dto import UserDto
from telegram_bot.services.user_service import UserService

logger = logging.getLogger(__name__)


class ACLMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()
        self.__user_service = UserService.get_instance()

    async def on_pre_process_message(self, message: types.Message, data: dict, *args, **kwargs):
        try:
            user = await self.__user_service.get_user_by_tg_id(message.from_user.id)

        except Exception as err:
            logger.info(f'New user {message.from_user=}')
            user_dto = UserDto()
            user_dto.fill_from_user(message.from_user)
            user = await self.__user_service.create_user(user_dto)
        if user.firstname != message.from_user.first_name or user.firstname == 'Not Authorized':
            user_dto = UserDto()
            user_dto.fill_from_user(message.from_user)
            user = await self.__user_service.update_user(user_dto)
        data['user'] = user

    async def on_pre_process_callback_query(self, call: types.CallbackQuery, data: dict, *arg, **kwargs):
        try:
            user = await self.__user_service.get_user_by_tg_id(call.message.from_user.id)

        except Exception as err:
            logger.info(f'New user {call.message.from_user=}')
            user_dto = UserDto()
            user_dto.fill_from_user(call.message.from_user)
            user = await self.__user_service.create_user(user_dto)

        data['user'] = user
