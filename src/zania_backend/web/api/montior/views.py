from fastapi import APIRouter

from zania_backend.core.schema.api_response import APIResponse, ResponseUtils

monitor_router = APIRouter(
	prefix="/health",
	tags=["Monitor"],
)


@monitor_router.get("", description="Health check", response_class=APIResponse)
def health() -> APIResponse:
	return ResponseUtils.create_success_response(message="Zania Backend is running")
