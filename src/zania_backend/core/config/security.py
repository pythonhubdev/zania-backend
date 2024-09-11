from dataclasses import dataclass

from zania_backend.core.config.base import settings


@dataclass(frozen=True)
class CSRFConfig:
	secret_key: str = settings.app.SECRET_KEY
	cookies_samesite: str = "none"
