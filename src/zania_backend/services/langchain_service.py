import json
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING

import aiofiles  # type: ignore
from fastapi import UploadFile
from langchain.chains.question_answering import load_qa_chain
from langchain_community.document_loaders import JSONLoader, PyMuPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAI, OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter

from zania_backend.core import ErrorMessages
from zania_backend.core.utils.logging import logger
from zania_backend.repository import ServiceRepository

if TYPE_CHECKING:
	from langchain.chains.combine_documents.base import BaseCombineDocumentsChain
	from langchain_core.vectorstores import VST


class LangchainService(ServiceRepository):
	def __init__(self) -> None:
		self.document_store: VST | None = None  # type: ignore
		self.qa_chain: BaseCombineDocumentsChain | None = None

	async def query(self, question: str) -> dict[str, str]:
		if not self.document_store or not self.qa_chain:
			raise ValueError(ErrorMessages.DOCUMENT_NOT_LOADED)

		docs = self.document_store.similarity_search(question)

		return await self.qa_chain.arun(input_documents=docs, question=question)

	async def load(self, resource: UploadFile):
		assert resource.filename is not None
		with tempfile.NamedTemporaryFile(delete=False) as temp_file:
			content = await resource.read()
			temp_file.write(content)
			temp_file_path = temp_file.name
		try:
			loader: JSONLoader | PyMuPDFLoader
			if resource.filename.endswith(".pdf"):
				loader = PyMuPDFLoader(temp_file_path)
				documents = loader.load()
			elif resource.filename.endswith(".json"):
				loader = JSONLoader(temp_file_path, jq_schema=".[]")
				documents = loader.load()
			else:
				raise ValueError(ErrorMessages.UNSUPPORTED_FILE_TYPES)

			text_splitter = CharacterTextSplitter(chunk_size=10000, chunk_overlap=0)
			texts = text_splitter.split_documents(documents)

			embeddings = OpenAIEmbeddings()
			self.document_store = FAISS.from_documents(texts, embeddings)

			self.qa_chain = load_qa_chain(OpenAI(), chain_type="stuff")

		except Exception as exception:
			logger.error(f"Exception occurred while loading document: {exception}", exc_info=True)
			raise exception
		finally:
			Path.unlink(Path(temp_file_path))

	@staticmethod
	async def process_questions(questions_file: UploadFile) -> list[str]:
		with tempfile.NamedTemporaryFile(delete=False) as temp_file:
			content = await questions_file.read()
			temp_file.write(content)
			temp_file_path = temp_file.name

		try:
			assert questions_file.filename is not None
			if questions_file.filename.endswith(".json"):
				with aiofiles.open(temp_file_path) as file:
					questions = json.load(file)
			else:
				raise ValueError(ErrorMessages.UNSUPPORTED_FILE_TYPES_JSON)

			return questions

		finally:
			Path.unlink(Path(temp_file_path))
