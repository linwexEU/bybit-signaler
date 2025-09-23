import os

from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings

current_dir = os.path.dirname(os.path.abspath(__file__))

os.chdir(current_dir)

dotenv_path = find_dotenv(".env")
load_dotenv(dotenv_path)


class Settings(BaseSettings):
    TESTNET: bool

    API_KEY: str
    API_SECRET: str

    THRESHOLD: int

    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    REDIS_HOST: str
    REDIS_PORT: int

    API_ID: int
    API_HASH: str

    GROUP_LINK: str

    SESSION_NAME: str
    SESSION_PATH: str

    COOKIES_PATH: str
    DOWNLOAD_DIR: str

    OPENAI_API_KEY: str

    @property
    def DATABASE_URL(self) -> str: 
        return f"postgresql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def REDIS_URL(self) -> str: 
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/"

    class ConfigDict: 
        env_file = dotenv_path


settings = Settings()
