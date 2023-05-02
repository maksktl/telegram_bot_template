from dataclasses import dataclass

from environs import Env


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str


@dataclass
class TgBot:
    token: str
    use_redis: bool


@dataclass
class Config:
    _instance = None
    tg_bot: TgBot
    db: DbConfig

    @classmethod
    def get_instance(cls, path=None):
        if cls._instance is None:
            env = Env()
            env.read_env(path)
            return Config(
                tg_bot=TgBot(
                    token=env.str("BOT_TOKEN"),
                    use_redis=env.bool("USE_REDIS"),
                ),
                db=DbConfig(
                    host=env.str('DB_HOST'),
                    password=env.str('DB_PASS'),
                    user=env.str('DB_USER'),
                    database=env.str('DB_NAME')
                ),
            )
        return cls._instance
