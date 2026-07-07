from pydantic import Field

from infrastructure.adapter.external.study_program_agent_parser.output.activity import (
    Activity,
)
from infrastructure.adapter.external.study_program_agent_parser.output.assessment import (
    Assessment,
)
from infrastructure.adapter.external.study_program_agent_parser.output.curriculum_item import (
    CurriculumItem,
)
from infrastructure.adapter.external.study_program_agent_parser.output.curriculum_output_model import (
    CurriculumOutputModel,
)
from infrastructure.adapter.external.study_program_agent_parser.output.evaluation_indicator import (
    EvaluationIndicator,
)
from infrastructure.adapter.external.study_program_agent_parser.output.guidance import (
    Guidance,
)
from infrastructure.adapter.external.study_program_agent_parser.output.learning_objective import (
    LearningObjective,
)
from infrastructure.adapter.external.study_program_agent_parser.output.schema_examples import (
    schema_examples,
)
from infrastructure.adapter.external.study_program_agent_parser.output.source_reference import (
    SourceReference,
)


class Unit(CurriculumOutputModel):
    model_config = schema_examples(
        {
            "code": "U1",
            "number": 1,
            "semester": "Semestre 1",
            "module_code": "seguridad-prevencion-autocuidado",
            "title": (
                "Riesgos socionaturales en nuestros territorios: Preparados "
                "para actuar en situacion de emergencia?"
            ),
            "purpose": (
                "Que los estudiantes reflexionen y adopten medidas de "
                "prevencion frente a riesgos socionaturales."
            ),
            "estimated_time": "9 semanas",
            "guiding_questions": [
                "Que entendemos por riesgos socionaturales?",
                "Que riesgos existen en mi contexto local?",
            ],
            "objective_codes": ["OA 3", "OA a", "OA b", "OA c"],
            "attitude_codes": ["A1"],
            "keywords": ["riesgo", "prevencion", "mitigacion", "adaptacion"],
        }
    )

    code: str | None = Field(None, description="Unit code or identifier.")
    number: int | None = Field(
        None, description="Unit number inside the study program."
    )
    semester: str | None = Field(
        None, description="Semester or school-year period associated with the unit."
    )
    module_code: str | None = Field(
        None, description="Curriculum module code when applicable."
    )
    title: str | None = Field(None, description="Official unit title.")
    purpose: str | None = Field(None, description="Unit purpose.")
    description: str | None = Field(
        None, description="General unit description or synthesis."
    )
    estimated_time: str | None = Field(
        None, description="Suggested time, duration, or pedagogical hours."
    )
    guiding_questions: list[str] = Field(
        default_factory=list, description="Guiding questions declared for the unit."
    )
    objective_codes: list[str] = Field(
        default_factory=list,
        description="OA, OAG, OAT, or expected learning codes covered.",
    )
    objectives: list[LearningObjective] = Field(
        default_factory=list,
        description="Full objectives declared inside the unit.",
    )
    knowledge_codes: list[str] = Field(
        default_factory=list, description="Knowledge items covered in the unit."
    )
    knowledge: list[CurriculumItem] = Field(
        default_factory=list,
        description="Knowledge items declared inside the unit.",
    )
    skill_codes: list[str] = Field(
        default_factory=list, description="Skills developed in the unit."
    )
    skills: list[CurriculumItem] = Field(
        default_factory=list, description="Skills declared inside the unit."
    )
    attitude_codes: list[str] = Field(
        default_factory=list, description="Attitudes promoted in the unit."
    )
    attitudes: list[CurriculumItem] = Field(
        default_factory=list, description="Attitudes declared inside the unit."
    )
    keywords: list[str] = Field(
        default_factory=list, description="Keywords declared for the unit."
    )
    prior_knowledge: list[str] = Field(
        default_factory=list, description="Required or suggested prior knowledge."
    )
    indicators: list[EvaluationIndicator] = Field(
        default_factory=list,
        description="Suggested assessment indicators in the unit.",
    )
    guidance: list[Guidance] = Field(
        default_factory=list,
        description="Didactic, assessment, or implementation guidance.",
    )
    activities: list[Activity] = Field(
        default_factory=list,
        description="Activities, activity examples, or learning experiences.",
    )
    assessments: list[Assessment] = Field(
        default_factory=list,
        description="Assessment examples, suggestions, or activities.",
    )
    contents: list[CurriculumItem] = Field(
        default_factory=list,
        description="Declared contents when the source uses this category.",
    )
    source: SourceReference | None = Field(
        None, description="Source document reference."
    )
