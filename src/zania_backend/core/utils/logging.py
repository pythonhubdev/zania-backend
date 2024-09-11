import logging
import sys
from typing import Any

from loguru import logger

from ..config.base import settings


class InterceptHandler(logging.Handler):
	def emit(self, record: logging.LogRecord) -> None:
		try:
			level: str | int = logger.level(record.levelname).name
		except ValueError:
			level = record.levelno

		frame, depth = logging.currentframe(), 2
		while frame.f_code.co_filename == logging.__file__:
			if frame.f_back:
				frame = frame.f_back
				depth -= 1

		logger.opt(depth=depth, exception=record.exc_info).log(
			level,
			record.getMessage(),
		)


LOG_PREFIX_MAPPING = {
	"STAGE": "[STAGE] ",
	"END STAGE": "[END STAGE] ",
	"GROUP": "[GROUP] ",
	"END GROUP": "[END GROUP] ",
}


class CustomFormatter:
	def __call__(self, record: dict[str, Any]) -> str:
		stage = record["extra"].get("stage", "")
		log_prefix = LOG_PREFIX_MAPPING.get(stage, "")

		log_format = f"<green>{{time:YYYY-MM-DD HH:mm:ss}}</green>" f"| <level>{log_prefix}{{level: <4}} </level> "
		if record["function"]:
			log_format += "| <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> "
		log_format += "- <level>{message}</level>\n"

		if record["exception"]:
			log_format += "{exception}\n"
		return log_format


def configure_logging() -> None:
	intercept_handler = InterceptHandler()
	intercept_handler.setFormatter(CustomFormatter())  # type: ignore
	logging.basicConfig(
		handlers=[intercept_handler],
		level=logging.NOTSET,
	)
	for logger_name in logging.root.manager.loggerDict:
		if logger_name.startswith("granian."):
			logging.getLogger(logger_name).handlers = []

	if not settings.server.USE_HYPERCORN:
		# Stop logs from RUST
		granian_internal_logger = logging.getLogger("_granian.asgi.serve")
		granian_internal_logger.setLevel(logging.CRITICAL)
		# Stop logs from Granian internal logger
		granian_private_logger = logging.getLogger("_granian")
		granian_private_logger.setLevel(logging.CRITICAL)
		granian_private_logger.handlers = [intercept_handler]
		granian_private_logger.propagate = False

		# Set config for granian access logger
		granian_access_logger = logging.getLogger("granian.access")
		granian_access_logger.handlers = [intercept_handler]
		granian_access_logger.propagate = False
	else:
		# Set config for hypercorn access logger
		hypercorn_access_logger = logging.getLogger("hypercorn.access")
		hypercorn_access_logger.handlers = [intercept_handler]
		hypercorn_access_logger.propagate = False

		# Set config for hypercorn internal logger
		hypercorn_internal_logger = logging.getLogger("hypercorn")
		hypercorn_internal_logger.handlers = [intercept_handler]
		hypercorn_access_logger.propagate = False

	logger.configure(
		handlers=[
			{
				"sink": sys.stdout,
				"level": settings.log.LEVEL,
				"format": CustomFormatter(),
			},
		],
	)


logger = logger.bind(name="Zania")
stage_logger = logger.bind(stage="STAGE")
end_stage_logger = logger.bind(stage="END STAGE")
