from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional


def _bool_from_env(value: Optional[str], default: bool = False) -> bool:
    if value is None or value == "":
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _float_from_env(value: Optional[str], default: float) -> float:
    if value is None or value == "":
        return default
    try:
        return float(value)
    except ValueError:
        return default


def _int_from_env(value: Optional[str], default: int) -> int:
    if value is None or value == "":
        return default
    try:
        return int(value)
    except ValueError:
        return default


@dataclass(frozen=True)
class Settings:
    app_name: str
    app_password: str
    secret_key: str
    database_url: str
    llm_enabled: bool
    llm_base_url: str
    llm_model: str
    llm_timeout_seconds: int
    weather_enabled: bool
    weather_latitude: float
    weather_longitude: float
    weather_timezone: str

    @property
    def auth_enabled(self) -> bool:
        return bool(self.app_password)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings(
        app_name=os.getenv("APP_NAME", "Command Center"),
        app_password=os.getenv("APP_PASSWORD", ""),
        secret_key=os.getenv("SECRET_KEY", "change-me"),
        database_url=os.getenv("DATABASE_URL", "sqlite:///./data/command_center.db"),
        llm_enabled=_bool_from_env(os.getenv("LLM_ENABLED"), False),
        llm_base_url=os.getenv("LLM_BASE_URL", "http://192.168.1.X:1234/v1"),
        llm_model=os.getenv("LLM_MODEL", "local-model"),
        llm_timeout_seconds=_int_from_env(os.getenv("LLM_TIMEOUT_SECONDS"), 8),
        weather_enabled=_bool_from_env(os.getenv("WEATHER_ENABLED"), True),
        weather_latitude=_float_from_env(os.getenv("WEATHER_LATITUDE"), 47.712),
        weather_longitude=_float_from_env(os.getenv("WEATHER_LONGITUDE"), -116.948),
        weather_timezone=os.getenv("WEATHER_TIMEZONE", "America/Los_Angeles"),
    )


def reset_settings_cache() -> None:
    get_settings.cache_clear()
