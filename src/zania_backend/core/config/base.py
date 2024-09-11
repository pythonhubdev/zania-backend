from __future__ import annotations

import binascii
import json
import os
from dataclasses import dataclass, field
from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import Final

from loguru import logger

from zania_backend.core.utils.helper import Helper

DEFAULT_MODULE_NAME = "zania_backend"
BASE_DIR: Final[Path] = Helper.module_to_os_path(DEFAULT_MODULE_NAME)

TRUE_VALUES = {"True", "true", "1", "yes", "Y", "T"}


class Environment(str, Enum):
	"""Current working environment."""

	DEVELOPMENT = "development"
	PRODUCTION = "production"
	TESTING = "testing"


ENV_FILE_MAP = {
	Environment.DEVELOPMENT: ".env.development",
	Environment.TESTING: ".env.testing",
}


@dataclass
class LogSettings:
	"""Logger configuration."""

	LEVEL: int = field(default_factory=lambda: int(os.getenv("LOG_LEVEL", "10")))
	"""Stdlib log levels.

    Only emit logs at this level, or higher.
    """
	HYPERCORN_ACCESS_LEVEL: int = 20
	"""Level to log hypercorn access logs."""
	HYPERCORN_ERROR_LEVEL: int = 20
	"""Level to log hypercorn error logs."""
	GRANIAN_ACCESS_LEVEL: int = 30
	"""Level to log granian access logs."""
	GRANIAN_ERROR_LEVEL: int = 20
	"""Level to log granian error logs."""


@dataclass
class AppSettings:
	"""Application configuration."""

	DEBUG: bool = field(default_factory=lambda: os.getenv("DEBUG", "False") in TRUE_VALUES)
	"""Run server with `debug=True`."""
	SECRET_KEY: str = field(
		default_factory=lambda: os.getenv("SECRET_KEY", binascii.hexlify(os.urandom(32)).decode(encoding="utf-8")),
	)
	"""Application secret key."""
	NAME: str = field(default_factory=lambda: "app")
	"""Application name."""
	ALLOWED_CORS_ORIGINS: list[str] | str = field(default_factory=lambda: os.getenv("ALLOWED_CORS_ORIGINS", '["*"]'))
	"""Allowed CORS Origins"""
	CSRF_COOKIE_NAME: str = field(default_factory=lambda: "csrftoken")
	"""CSRF Cookie Name"""
	CSRF_COOKIE_SECURE: bool = field(default_factory=lambda: False)
	"""CSRF Secure Cookie"""
	JWT_ENCRYPTION_ALGORITHM: str = field(default_factory=lambda: "HS256")
	"""JWT Encryption Algorithm"""

	OPEN_API_KEY: str = field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
	"""OpenAI API Key"""

	def __post_init__(self) -> None:
		if isinstance(self.ALLOWED_CORS_ORIGINS, str):
			if self.ALLOWED_CORS_ORIGINS.startswith("[") and self.ALLOWED_CORS_ORIGINS.endswith("]"):
				try:
					# Safely evaluate the string as a Python list.
					self.ALLOWED_CORS_ORIGINS = json.loads(self.ALLOWED_CORS_ORIGINS)
				except (SyntaxError, ValueError):
					# Handle potential errors if the string is not a valid Python literal.
					msg = "ALLOWED_CORS_ORIGINS is not a valid list representation."
					raise ValueError(msg) from None
			else:
				# Split the string by commas into a list if it is not meant to be a list representation.
				self.ALLOWED_CORS_ORIGINS = [host.strip() for host in self.ALLOWED_CORS_ORIGINS.split(",")]


@dataclass
class ServerSettings:
	"""Server configurations."""

	APP_LOC: str = field(default_factory=lambda: os.getenv("APP_LOC", "app:app"))
	"""Path to app executable, or factory."""
	HOST: str = field(default_factory=lambda: os.getenv("HOST", "0.0.0.0"))
	"""Server network host."""
	PORT: int = field(default_factory=lambda: int(os.getenv("PORT", "8000")))
	"""Server port."""

	HTTP_WORKERS: int = field(
		default_factory=lambda: int(os.getenv("WEB_CONCURRENCY"))  # type: ignore[arg-type]
		if os.getenv("WEB_CONCURRENCY") is not None
		else 1,
	)
	"""Number of HTTP Worker processes to be spawned by Hypercorn / Granian."""
	USE_HYPERCORN: bool = field(default_factory=lambda: os.getenv("USE_HYPERCORN", "True") in TRUE_VALUES)

	"""Current working environment."""
	ENVIRONMENT: Environment = field(default_factory=lambda: Environment(os.getenv("ENVIRONMENT", "development")))


@dataclass
class Settings:
	app: AppSettings = field(default_factory=AppSettings)
	server: ServerSettings = field(default_factory=ServerSettings)
	log: LogSettings = field(default_factory=LogSettings)

	@classmethod
	def from_env(cls) -> Settings:
		environment = os.getenv("ENVIRONMENT", "development")
		dotenv_filename = f".env.{environment}"
		if environment != "production":
			env_file = Path(f"{os.curdir}/{dotenv_filename}")
			if env_file.is_file():
				from dotenv import load_dotenv

				logger.info(f"Loading environment variables from {env_file}")
				load_dotenv(env_file)
			else:
				logger.warning(f"No environment file found for {environment}")

		return cls()


@lru_cache(maxsize=1, typed=True)
def get_settings() -> Settings:
	return Settings.from_env()


settings: Settings = get_settings()
