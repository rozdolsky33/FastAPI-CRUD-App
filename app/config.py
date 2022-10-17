from pydantic import BaseSettings, PostgresDsn


class Config(BaseSettings):
    postgres_host: PostgresDsn

    class Config():
        env_prefix = "db_"
