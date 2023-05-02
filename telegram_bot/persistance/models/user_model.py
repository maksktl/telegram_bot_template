from sqlalchemy import sql, Column, String, BIGINT

from telegram_bot.persistance.models.timed_base_model import TimedBaseModel
from telegram_bot.services.dto.user_dto import UserDto


class UserModel(TimedBaseModel):
    __tablename__ = 'user'
    query: sql.Select

    firstname = Column(String(256), nullable=False, index=True)
    lastname = Column(String(256))
    telegram_id = Column(BIGINT, unique=True, index=True)
    telegram_username = Column(String(256), index=True)

    def fill(self, user_dto: UserDto):
        self.firstname = user_dto.firstname
        self.lastname = user_dto.lastname
        self.telegram_id = user_dto.telegram_id
        self.telegram_username = user_dto.telegram_username
