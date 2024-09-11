from typing import Annotated

from fastapi import APIRouter, File, UploadFile

from zania_backend.core.schema.api_response import APIResponse
from zania_backend.web.api.llm.controller import LLMController
from zania_backend.web.api.llm.schema import QAndASchema

llm_router = APIRouter(prefix="/llm", tags=["LLM"])


@llm_router.post("/query", response_class=APIResponse)
async def query(
	document: Annotated[UploadFile, File()],
	data: QAndASchema,
	questions_document: Annotated[UploadFile, File()] | None = None,
) -> APIResponse:
	return await LLMController.query(
		data=data,
		document=document,
		questions_document=questions_document,
	)
