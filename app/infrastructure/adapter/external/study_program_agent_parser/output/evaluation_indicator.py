from pydantic import Field

from infrastructure.adapter.external.study_program_agent_parser.output.curriculum_item import (
    CurriculumItem,
)
from infrastructure.adapter.external.study_program_agent_parser.output.schema_examples import (
    schema_examples,
)


class EvaluationIndicator(CurriculumItem):
    model_config = schema_examples(
        {
            "objective_code": "OA 3",
            "description": "Describen riesgos de origen natural o provocados por la accion humana.",
            "criteria": ["Relaciona causas, efectos y medidas de prevencion."],
            "evidence": ["Explica riesgos locales usando modelos, tablas o diagramas."],
        }
    )

    objective_code: str | None = Field(
        None, description="Associated OA, OAG, OAT, or expected learning code."
    )
    achievement_level: str | None = Field(
        None, description="Expected level, range, or performance when present."
    )
    criteria: list[str] = Field(
        default_factory=list,
        description="Assessment criteria associated with the indicator.",
    )
    evidence: list[str] = Field(
        default_factory=list,
        description="Observable evidence suggested to verify learning.",
    )
