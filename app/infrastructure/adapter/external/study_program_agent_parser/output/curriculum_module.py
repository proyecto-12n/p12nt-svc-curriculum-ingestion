from typing import Any

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
from infrastructure.adapter.external.study_program_agent_parser.output.unit import Unit


class CurriculumModule(CurriculumOutputModel):
    model_config = schema_examples(
        {
            "code": "seguridad-prevencion-autocuidado",
            "title": "Seguridad, Prevencion y Autocuidado",
            "description": "Modulo de Ciencias para la Ciudadania.",
            "estimated_time": "1 semestre",
            "objective_codes": ["OA 1", "OA 2", "OA 3"],
            "attitude_codes": ["A1", "A2"],
        }
    )

    code: str | None = Field(None, description="Module code or identifier.")
    title: str | None = Field(None, description="Curriculum module title.")
    description: str | None = Field(None, description="General module description.")
    purpose: str | None = Field(None, description="Module formative purpose.")
    estimated_time: str | None = Field(
        None, description="Module duration or estimated time."
    )
    overview: list[dict[str, Any]] = Field(
        default_factory=list, description="Semester, annual, or module overview."
    )
    objective_codes: list[str] = Field(
        default_factory=list,
        description="Learning objectives associated with the module.",
    )
    attitude_codes: list[str] = Field(
        default_factory=list, description="Attitudes associated with the module."
    )
    units: list[Unit] = Field(
        default_factory=list, description="Units that compose the module."
    )
    source: SourceReference | None = Field(
        None, description="Source document reference."
    )
