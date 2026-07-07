from pydantic import Field

from infrastructure.adapter.external.study_program_agent_parser.output.curriculum_output_model import (
    CurriculumOutputModel,
)
from infrastructure.adapter.external.study_program_agent_parser.output.evaluation_indicator import (
    EvaluationIndicator,
)
from infrastructure.adapter.external.study_program_agent_parser.output.schema_examples import (
    schema_examples,
)
from infrastructure.adapter.external.study_program_agent_parser.output.source_reference import (
    SourceReference,
)


class Assessment(CurriculumOutputModel):
    model_config = schema_examples(
        {
            "title": "Actividad de Evaluacion",
            "description": "Ejemplo de evaluacion asociado a una unidad o actividad.",
            "type": "formativa",
            "objective_codes": ["OA 3", "OA a"],
            "criteria": ["Usa evidencia para fundamentar sus respuestas."],
            "instruments": ["rubrica", "lista de cotejo"],
        }
    )

    title: str | None = Field(None, description="Assessment title or name.")
    description: str | None = Field(None, description="Assessment activity, instrument, or suggestion description.")
    type: str | None = Field(None, description="Assessment type indicated by the source.")
    objective_codes: list[str] = Field(default_factory=list, description="Assessed objective codes.")
    indicators: list[EvaluationIndicator] = Field(default_factory=list, description="Assessment indicators used.")
    criteria: list[str] = Field(default_factory=list, description="Assessment criteria, rubrics, or guidelines.")
    instruments: list[str] = Field(
        default_factory=list,
        description="Mentioned instruments, such as rubrics, checklists, or tests.",
    )
    source: SourceReference | None = Field(None, description="Source document reference.")
