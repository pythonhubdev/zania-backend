from importlib import metadata

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.models import Server
from fastapi.staticfiles import StaticFiles
from fastapi_msgspec.responses import MsgSpecJSONResponse  # type: ignore

from zania_backend.core import Helper, configure_logging
from zania_backend.core.schema.api_response import APIResponse, ResponseUtils
from zania_backend.middlewares import LoggingMiddleware
from zania_backend.web.api.router import api_router


def construct_app() -> FastAPI:
	_app = FastAPI(
		title="Zania Backend",
		version=metadata.version("zania-backend"),
		docs_url=None,
		redoc_url=None,
		openapi_url="/api/openapi.json",
		default_response_class=MsgSpecJSONResponse,
		servers=[
			Server(
				url="http://0.0.0.0:8000",
				description="Local server",
			).model_dump(),
			Server(
				url="https://api.zania.com",
				description="Zania server",
			).model_dump(),
		],
	)

	_app.add_middleware(
		CORSMiddleware,  # type: ignore
		allow_origins=["*"],
		allow_credentials=True,
		allow_methods=["*"],
		allow_headers=["*"],
	)
	_app.add_middleware(LoggingMiddleware)  # type: ignore

	_app.include_router(router=api_router, prefix="/api")

	_app.mount(
		"/static",
		StaticFiles(directory=Helper.module_to_os_path("zania_backend") / "static"),
		name="static",
	)

	configure_logging()

	@_app.get("/", response_class=APIResponse)
	def index() -> APIResponse:
		return ResponseUtils.create_success_response(
			message="Welcome to Zania Backend API",
		)

	return _app


app: FastAPI = construct_app()
