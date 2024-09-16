import logging
from dotenv import load_dotenv
from attr import dataclass
from pydantic import Field
from pydantic_settings import BaseSettings


load_dotenv()


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(module)s - %(funcName)s: %(message)s",
)


class Settings(BaseSettings):
    class Config:
        env_file = ".env"

    bot_token: str = Field(..., alias="BOT_TOKEN")
    git_token: str = Field(..., alias="GITLAB_TOKEN")
    git_url: str = Field(..., alias="GITLAB_URL")
    admin_users: set = Field(..., alias="ADMIN_USERS")
    approved_users: set = Field(..., alias="APPROVED_USERS")
    extensions: set = Field(..., alias="EXTENSIONS")


settings = Settings()
