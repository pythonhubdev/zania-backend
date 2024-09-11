from scalar_fastapi import get_scalar_api_reference  # type: ignore

from .base import settings

open_api_config = get_scalar_api_reference(
	openapi_url="/api/openapi.json",
	title=settings.app.NAME,
	scalar_js_url="/static/docs/scalar.js",
	scalar_theme="/static/docs/scalar.css",
	servers=[
		{
			"url": "http://0.0.0.0:8000",
			"description": "Local server",
		},
		{
			"url": "https://api.zania.com",
			"description": "Zania server",
		},
	],
)
