from hypercorn import Config

from .base import settings


class HypercornConfig(Config):
	def __init__(self):
		super().__init__()
		self._custom_bind = [f"{settings.server.HOST}:{settings.server.PORT}"]

	@property
	def bind(self) -> list[str]:
		return self._custom_bind

	@bind.setter
	def bind(self, value: list[str] | str) -> None:
		if isinstance(value, str):
			self._custom_bind = [value]
		else:
			self._custom_bind = value

	workers = settings.server.HTTP_WORKERS  # type: ignore
	use_reloader = settings.app.DEBUG
	accesslog = None
	errorlog = None
