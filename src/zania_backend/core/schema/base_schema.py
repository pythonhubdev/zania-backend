from typing import Any, Generic, TypeVar

import msgspec
from msgspec import Struct

from ..utils.enums import StatusEnum


class BaseSchema(Struct, rename="camel", omit_defaults=True):
	def to_dict(self, exclude_none: bool | None = None) -> dict[str, Any]:
		"""
		Convert the struct to a dictionary, excluding None and msgspec.UNSET values.

		Args:
		----
			exclude_none (bool): If True, exclude fields that are None.

		Returns:
		-------
			dict: A dictionary representation of the struct.

		"""
		if exclude_none is None:
			exclude_none = True

		return {
			f: getattr(self, f)
			for f in self.__struct_fields__
			if getattr(self, f, None) != msgspec.UNSET and (not exclude_none or getattr(self, f) is not None)
		}


T = TypeVar("T")


class BaseResponseSchema(BaseSchema, Generic[T]):
	status: StatusEnum
	message: str
	data: T | None = None


class BaseRequestSchema(BaseSchema): ...
