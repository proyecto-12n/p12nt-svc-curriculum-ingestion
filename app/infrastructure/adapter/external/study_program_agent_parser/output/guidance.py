from pydantic import Field

from infrastructure.adapter.external.study_program_agent_parser.output.curriculum_output_model import (
    CurriculumOutputModel,
)
from infrastructure.adapter.external.study_program_agent_parser.output.guidance_type import (
    GuidanceType,
)
from infrastructure.adapter.external.study_program_agent_parser.output.schema_examples import (
    schema_examples,
)
from infrastructure.adapter.external.study_program_agent_parser.output.source_reference import (
    SourceReference,
)


class Guidance(CurriculumOutputModel):
    model_config = schema_examples(
        {
            "title": "Observaciones al docente",
            "type": "observacion_docente",
            "description": "Promover un ambiente de respeto y empatia entre pares.",
            "objective_codes": ["OA 3"],
            "unit_code": "U1",
        }
    )

    title: str | None = Field(None, description="Guidance title.")
    type: GuidanceType | str | None = Field(
        None, description="Guidance type according to its curricular function."
    )
    description: str = Field(..., description="Guidance text.")
    objective_codes: list[str] = Field(
        default_factory=list, description="Related learning objectives."
    )
    unit_code: str | None = Field(None, description="Associated unit, when applicable.")
    source: SourceReference | None = Field(
        None, description="Source document reference."
    )
