from fastapi.openapi.models import Server

server_config: list[Server] = [
	Server(
		url="http://127.0.0.1:8000",
		description="Development server",
	),
	Server(
		url="https://api.zania.com",
		description="Production server",
	),
]
