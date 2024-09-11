import json
from typing import Annotated

from fastapi import APIRouter, File, Form, UploadFile

from zania_backend.core.schema.api_response import APIResponse

from .controller import LLMController
from .schema import QAndASchema

llm_router = APIRouter(prefix="/llm", tags=["LLM"])


@llm_router.post("/query", response_class=APIResponse)
async def query(
	document: Annotated[
		UploadFile,
		File(
			...,
			description="The actual document to query",
		),
	],
	questions: Annotated[
		str | None,
		Form(
			...,
			description="Pass the questions as a list of strings",
		),
	] = None,
	questions_document: Annotated[
		UploadFile | None,
		File(
			...,
			description="The document containing the questions",
		),
	] = None,
) -> APIResponse:
	assert document is not None
	data: QAndASchema | None = None
	if questions is not None:
		data = QAndASchema(questions=json.loads(questions))
	return await LLMController.query(
		data=data,
		document=document,
		questions_document=questions_document,
	)
