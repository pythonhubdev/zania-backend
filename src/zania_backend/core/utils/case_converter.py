import re
from collections.abc import Mapping
from functools import lru_cache
from typing import Any


class CaseConverter:
	UNDERSCORE_RE = re.compile(r"(?<=[^\-_])[\-_]+[^\-_]")

	@classmethod
	@lru_cache(maxsize=1024)
	def _camelize_string(cls, s: str) -> str:
		"""Camelizes a single string."""
		if s.isupper() or s.isnumeric():
			return s
		s = s[0].lower() + s[1:] if s and not s[:2].isupper() else s
		return cls.UNDERSCORE_RE.sub(lambda m: m.group(0)[-1].upper(), s)

	@classmethod
	def camelize(
		cls, data: str | list[Any] | tuple[Any] | Mapping[str, Any]
	) -> str | list[Any] | tuple[Any] | Mapping[str, Any]:
		"""
		Convert a string, dict, or list of dicts to camel case.

		Args:
		----
		data: A string, dictionary, or list of dictionaries.

		Returns:
		-------
		Camelized string, dictionary, or list of dictionaries.

		"""
		if isinstance(data, str):
			return cls._camelize_string(data)
		elif isinstance(data, (list | tuple)):
			return type(data)(cls.camelize(item) for item in data)
		elif isinstance(data, Mapping):
			return {cls._camelize_string(k) if isinstance(k, str) else k: cls.camelize(v) for k, v in data.items()}
		else:
			return data

	@classmethod
	@lru_cache(maxsize=1024)
	def _decamelize_string(cls, s: str) -> str:
		"""Decamelizes a single string."""
		return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s).lower()

	@classmethod
	def decamelize(
		cls, data: str | list[Any] | tuple[Any] | Mapping[str, Any]
	) -> str | list[Any] | tuple[Any] | Mapping[str, Any]:
		"""
		Convert a camelCase string, dict, or list of dicts to snake_case.

		Args:
		----
		data: A string, dictionary, or list of dictionaries in camelCase.

		Returns:
		-------
		snake_case string, dictionary, or list of dictionaries.

		"""
		if isinstance(data, str):
			return cls._decamelize_string(data)
		elif isinstance(data, (list | tuple)):
			return type(data)(cls.decamelize(item) for item in data)
		elif isinstance(data, Mapping):
			return {cls._decamelize_string(k) if isinstance(k, str) else k: cls.decamelize(v) for k, v in data.items()}
		else:
			return data
