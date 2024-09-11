from granian import Granian
from granian.constants import Interfaces

from zania_backend.core.config.base import settings


class GranianApplication:
	"""
	Custom Granian application.

	This class is used to start Hypercorn with the FastAPI application.
	"""

	@staticmethod
	def run() -> None:
		"""Run the FastAPI application with Hypercorn."""
		granian_app = Granian(
			target=settings.server.APP_LOC,
			interface=Interfaces.ASGI,
			address=settings.server.HOST,
			port=settings.server.PORT,
			workers=settings.server.HTTP_WORKERS,
			reload=settings.app.DEBUG,
		)
		granian_app.serve()
