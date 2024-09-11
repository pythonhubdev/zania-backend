from .open_api_config import open_api_config
from .security import CSRFConfig


class Config:
	OPEN_API_CONFIG = open_api_config
	CSRF_CONFIG = CSRFConfig
