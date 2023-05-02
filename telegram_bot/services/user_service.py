import logging

from telegram_bot.persistance.models.user_model import UserModel
from telegram_bot.persistance.repository.user_repository import UserRepository
from telegram_bot.services.dto.user_dto import UserDto
from telegram_bot.services.dto.user_full_dto import UserFullDto

logger = logging.getLogger(__name__)


class UserService:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = UserService()
        return cls._instance

    def __init__(self):
        self.__user_repository = UserRepository.get_instance()

    async def get_user(self, id) -> UserFullDto:
        user_model = await self.__user_repository.get_by_id(id)
        if not user_model:
            raise Exception("User not found")
        return UserFullDto(user_model)

    async def get_user_by_tg_id(self, tg_id) -> UserFullDto:
        user_model = await self.__user_repository.get_by_tg_id_and_deleted_false(tg_id)
        if not user_model:
            raise Exception("User not found")
        return UserFullDto(user_model)

    async def create_user(self, user_dto: UserDto) -> UserFullDto:
        if user_dto.telegram_id and await self.__user_repository.get_by_tg_id_and_deleted_false(
                user_dto.telegram_id):
            raise Exception("User already exists")
        user_model = UserModel()
        user_model.fill(user_dto)
        return UserFullDto(await self.__user_repository.create(user_model))

    async def update_user(self, user_dto: UserDto):
        user_model = await self.__user_repository.get_by_id(user_dto.id)
        if not user_model:
            user_model = await self.__user_repository.get_by_tg_id_and_deleted_false(user_dto.telegram_id)
        if not user_model:
            raise Exception("User not found")
        return UserFullDto(await self.__user_repository.update(user_model.update_by_dto(user_dto)))
