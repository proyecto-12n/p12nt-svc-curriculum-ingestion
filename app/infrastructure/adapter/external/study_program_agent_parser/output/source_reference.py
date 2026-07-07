from pydantic import Field

from infrastructure.adapter.external.study_program_agent_parser.output.curriculum_output_model import (
    CurriculumOutputModel,
)
from infrastructure.adapter.external.study_program_agent_parser.output.schema_examples import (
    schema_examples,
)


class SourceReference(CurriculumOutputModel):
    model_config = schema_examples(
        {
            "document": "articles-20710_programa.pdf",
            "page": 56,
            "section": "Unidad 1",
            "original_text": "PROPOSITO",
        }
    )

    document: str | None = Field(
        None, description="Source PDF name, URL, or identifier."
    )
    page: int | None = Field(
        None, description="Document page where the information appears."
    )
    section: str | None = Field(None, description="Source section, title, or heading.")
    original_text: str | None = Field(
        None, description="Original extracted text without normalization."
    )
