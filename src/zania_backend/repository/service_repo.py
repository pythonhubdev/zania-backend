from abc import ABC, abstractmethod

from fastapi import UploadFile


class ServiceRepository(ABC):
	@abstractmethod
	async def load(self, resource: UploadFile):
		"""
		Lazy load the resource into the service. For example, a PDF file can be loaded into a PDF reader.

		:param resource:
		:return:
		"""

	@abstractmethod
	async def query(self, query: str):
		"""
		Query the service based on a specific resource that was loaded.

		:param query:
		:return:
		"""
