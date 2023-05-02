import datetime

from telegram_bot.persistance.db import db
from telegram_bot.persistance.models.base_model import BaseModel


class TimedBaseModel(BaseModel):
    __abstract__ = True

    created_at = db.Column(db.DateTime(True), server_default=db.func.now(), default=datetime.datetime.utcnow)
    updated_at = db.Column(
        db.DateTime(True),
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        server_default=db.func.now(),
        index=True
    )
