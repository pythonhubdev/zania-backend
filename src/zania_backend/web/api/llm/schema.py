
from pydantic import BaseModel, ConfigDict

from zania_backend.core.utils.case_converter import CaseConverter


class QAndASchema(BaseModel):
	questions: list[str] | None = None

	model_config = ConfigDict(
		alias_generator=CaseConverter.camelize,
		populate_by_name=True,
		arbitrary_types_allowed=True,
	)
