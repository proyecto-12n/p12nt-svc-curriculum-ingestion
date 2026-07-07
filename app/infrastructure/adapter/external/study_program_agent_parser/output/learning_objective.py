from pydantic import Field

from infrastructure.adapter.external.study_program_agent_parser.output.curriculum_item import (
    CurriculumItem,
)
from infrastructure.adapter.external.study_program_agent_parser.output.evaluation_indicator import (
    EvaluationIndicator,
)
from infrastructure.adapter.external.study_program_agent_parser.output.learning_objective_type import (
    LearningObjectiveType,
)
from infrastructure.adapter.external.study_program_agent_parser.output.schema_examples import (
    schema_examples,
)


class LearningObjective(CurriculumItem):
    model_config = schema_examples(
        {
            "code": "OA 3",
            "type": "OA",
            "subtype": "conocimiento",
            "description": (
                "Analizar, a partir de modelos, riesgos de origen natural o "
                "provocados por la accion humana en su contexto local."
            ),
            "module_code": "seguridad-prevencion-autocuidado",
            "unit_codes": ["U1"],
            "skill_codes": ["OA a", "OA b", "OA c"],
            "attitude_codes": ["A1"],
        },
        {
            "code": "OA a",
            "type": "OA",
            "subtype": "habilidad",
            "description": "Formular preguntas y problemas sobre topicos cientificos de interes.",
        },
    )

    type: LearningObjectiveType = Field(
        ...,
        description="Curricular objective type: OA, OAG, OAT, or expected learning.",
    )
    subtype: str | None = Field(
        None,
        description="Declared subtype, for example knowledge, skill, attitude, or axis.",
    )
    axis_code: str | None = Field(None, description="Associated axis code or name.")
    module_code: str | None = Field(
        None, description="Associated curriculum module, when applicable."
    )
    semester: str | None = Field(
        None, description="Semester or period when the objective is addressed."
    )
    priority: str | None = Field(
        None, description="Curricular prioritization category, when present."
    )
    unit_codes: list[str] = Field(
        default_factory=list, description="Units where this objective is covered."
    )
    skill_codes: list[str] = Field(
        default_factory=list, description="Skills associated with the objective."
    )
    knowledge_codes: list[str] = Field(
        default_factory=list,
        description="Knowledge items associated with the objective.",
    )
    attitude_codes: list[str] = Field(
        default_factory=list, description="Attitudes associated with the objective."
    )
    indicators: list[EvaluationIndicator] = Field(
        default_factory=list,
        description="Suggested assessment indicators for the objective.",
    )
    activity_codes: list[str] = Field(
        default_factory=list,
        description="Activities or examples associated with the objective.",
    )
    related_objectives: list[str] = Field(
        default_factory=list, description="Linked or integrated objective codes."
    )
