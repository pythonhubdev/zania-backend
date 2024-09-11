from zania_backend.core.config.base import settings
from zania_backend.web.application import construct_app
from zania_backend.web.granian_app import GranianApplication
from zania_backend.web.hypercorn_app import HypercornApplication


def main() -> None:
	"""Entrypoint of the application."""
	if settings.server.USE_HYPERCORN:
		app = construct_app()
		hypercorn_app = HypercornApplication(app)
		hypercorn_app.run()
	else:
		GranianApplication.run()


if __name__ == "__main__":
	main()
