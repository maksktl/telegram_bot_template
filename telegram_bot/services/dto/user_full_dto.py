from dataclasses import dataclass
from uuid import UUID


@dataclass
class UserFullDto:
    id: UUID
    firstname: str
    lastname: str
    telegram_id: int
    telegram_username: str

    def __init__(self, model):
        self.id = model.id
        self.telegram_id = model.telegram_id
        self.telegram_username = model.telegram_username
        self.firstname = model.firstname
        self.lastname = model.lastname
