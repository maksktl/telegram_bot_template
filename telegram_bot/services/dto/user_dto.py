from dataclasses import dataclass
from uuid import UUID


@dataclass
class UserDto:
    id: UUID = None
    firstname: str = None
    lastname: str = None
    telegram_id: int = None
    telegram_username: int = None

    def fill_from_user(self, user):
        self.telegram_id = user.id
        self.firstname = user.first_name
        self.lastname = user.last_name
        self.telegram_username = user.username
