from pydantic import Field

from infrastructure.adapter.external.study_program_agent_parser.output.curriculum_output_model import (
    CurriculumOutputModel,
)
from infrastructure.adapter.external.study_program_agent_parser.output.schema_examples import (
    schema_examples,
)
from infrastructure.adapter.external.study_program_agent_parser.output.source_reference import (
    SourceReference,
)


class CurriculumItem(CurriculumOutputModel):
    model_config = schema_examples(
        {
            "code": "Eje 1",
            "name": "Escuchar y apreciar",
            "description": "Eje curricular que organiza objetivos relacionados con la apreciacion musical.",
            "normalized_term": "ThematicAxis",
        }
    )

    code: str | None = Field(None, description="Official code or identifier.")
    name: str | None = Field(None, description="Item name, title, or label.")
    description: str | None = Field(None, description="Item textual description.")
    original_text: str | None = Field(
        None, description="Literal text when it differs from the normalized version."
    )
    normalized_term: str | None = Field(
        None, description="Concept homologated through the glossary."
    )
    source: SourceReference | None = Field(
        None, description="Source PDF and page reference."
    )
