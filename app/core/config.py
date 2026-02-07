"""Application configuration."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "tgbot-vpn"
    database_url: str = Field(
        default="postgresql+psycopg2://postgres:postgres@db:5432/tgbot", alias="DATABASE_URL"
    )
    jwt_secret: str = Field(default="change-me", alias="JWT_SECRET")
    jwt_algorithm: str = "HS256"
    jwt_exp_minutes: int = 60

    bot_token: str = Field(default="", alias="BOT_TOKEN")

    three_x_ui_base_url: str = Field(default="http://3x-ui:2053", alias="THREE_X_UI_BASE_URL")
    three_x_ui_username: str = Field(default="admin", alias="THREE_X_UI_USERNAME")
    three_x_ui_password: str = Field(default="admin", alias="THREE_X_UI_PASSWORD")

    rate_limit_devices_per_hour: int = 3


settings = Settings()
