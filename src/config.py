from functools import lru_cache
from pathlib import Path
from typing import Tuple

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent
DOTENV_PATH = BASE_DIR / ".env"


class Settings(BaseSettings):
    app_name: str = "SafraMonitor - API"
    debug: bool = False
    database_url: str

    temperature_interval: Tuple[float, float] = (25.0, 40.0)
    moisture_interval: Tuple[float, float] = (25.0, 80.0)
    gas_level_interval: Tuple[float, float] = (3.2, 10.0)

    telegram_bot_token: str
    telegram_chat_id: str = "984362796"

    dashboard_link: str = "https://ryanfaustinocarvalho.grafana.net/public-dashboards/d8b0214e85dc48b88877a4b98259a2d0"

    model_config = SettingsConfigDict(
        env_file=str(DOTENV_PATH),
        env_file_encoding="utf-8",
    )


@lru_cache
def get_settings():
    return Settings()
