from typing import Any

from starlette.responses import JSONResponse

from ..utils.enums import StatusEnum
from .base_schema import BaseResponseSchema


class APIResponse(JSONResponse):
	def __init__(
		self,
		status: StatusEnum,
		message: str,
		data: dict[str, Any] | None = None,
		status_code: int = 200,
		headers: dict[str, Any] | None = None,
	):
		content = BaseResponseSchema(
			status=status,
			message=message,
			data=data,
		).to_dict(exclude_none=True)
		super().__init__(content=content, status_code=status_code, headers=headers)


class ResponseUtils:
	@staticmethod
	def create_error_response(status_code: int, message: str) -> APIResponse:
		return APIResponse(status=StatusEnum.ERROR, message=message, status_code=status_code)
