from fastapi import UploadFile
from starlette import status

from zania_backend.core.schema.api_response import APIResponse, ResponseUtils
from zania_backend.services.langchain_service import LangchainService
from zania_backend.web.api.llm.schema import QAndASchema


class LLMController:
	@staticmethod
	async def query(
		document: UploadFile,
		questions_document: UploadFile | None,
		data: QAndASchema | None,
	) -> APIResponse:
		try:
			service = LangchainService()
			await service.load(document)
			questions = []
			if questions_document:
				questions = await service.process_questions(questions_document)
			elif data and data.questions:
				questions = data.questions

			results = {}
			for question in questions:
				answer = await service.query(question)
				results[question] = answer.strip()

			return ResponseUtils.create_success_response(
				message="Successfully queried LLM model",
				data=results,
			)
		except ValueError as value_error:
			if "Either 'questions_document' or 'questions' must be provided." in str(value_error):
				return ResponseUtils.create_error_response(
					status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
					message="Either 'questions_document' or 'questions' must be provided.",
				)
			if "Did not find openai_api_key" in str(value_error):
				return ResponseUtils.create_error_response(
					status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
					message="Did not find openai_api_key! Please provide the API key manually or set in the env with "
					"`OPENAI_API_KEY`.",
				)
			return ResponseUtils.create_error_response(
				status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
				message=str(value_error),
			)
