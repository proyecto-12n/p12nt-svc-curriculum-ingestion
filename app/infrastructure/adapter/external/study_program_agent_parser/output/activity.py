from pydantic import Field

from infrastructure.adapter.external.study_program_agent_parser.output.activity_type import (
    ActivityType,
)
from infrastructure.adapter.external.study_program_agent_parser.output.assessment import (
    Assessment,
)
from infrastructure.adapter.external.study_program_agent_parser.output.curriculum_output_model import (
    CurriculumOutputModel,
)
from infrastructure.adapter.external.study_program_agent_parser.output.evaluation_indicator import (
    EvaluationIndicator,
)
from infrastructure.adapter.external.study_program_agent_parser.output.learning_resource import (
    LearningResource,
)
from infrastructure.adapter.external.study_program_agent_parser.output.schema_examples import (
    schema_examples,
)
from infrastructure.adapter.external.study_program_agent_parser.output.source_reference import (
    SourceReference,
)


class Activity(CurriculumOutputModel):
    model_config = schema_examples(
        {
            "number": "Actividad 1",
            "title": "Estoy realmente preparado para viajar dentro de Chile?",
            "type": "aprendizaje",
            "purpose": "Reflexionar sobre riesgos socionaturales presentes en Chile.",
            "steps": [
                "Sensibilizacion",
                "Exploracion sobre riesgos socionaturales",
                "Conversatorio",
            ],
            "questions": [
                "Que harias en una situacion de emergencia?",
                "Que factores considerarias para tomar decisiones?",
            ],
            "objective_codes": ["OA 3", "OA a", "OA b"],
            "attitude_codes": [
                "Pensar con apertura a distintas perspectivas y contextos."
            ],
            "estimated_time": "2 horas pedagogicas",
        }
    )

    number: str | None = Field(
        None, description="Activity number or identifier within the unit."
    )
    title: str | None = Field(None, description="Activity or example title.")
    type: ActivityType | str | None = Field(
        None, description="Activity type according to the source."
    )
    purpose: str | None = Field(None, description="Declared activity purpose.")
    description: str | None = Field(None, description="Complete activity description.")
    steps: list[str] = Field(
        default_factory=list, description="Activity moments, steps, or development."
    )
    questions: list[str] = Field(
        default_factory=list, description="Questions, challenges, or prompts."
    )
    teacher_instructions: list[str] = Field(
        default_factory=list,
        description="Instructions or suggestions addressed to teachers.",
    )
    student_instructions: list[str] = Field(
        default_factory=list, description="Instructions addressed to students."
    )
    objective_codes: list[str] = Field(
        default_factory=list,
        description="Objective codes associated with the activity.",
    )
    attitude_codes: list[str] = Field(
        default_factory=list, description="Associated attitude codes or texts."
    )
    indicator_codes: list[str] = Field(
        default_factory=list, description="Associated indicator codes or references."
    )
    indicators: list[EvaluationIndicator] = Field(
        default_factory=list,
        description="Assessment indicators mentioned in the activity.",
    )
    resources: list[LearningResource] = Field(
        default_factory=list,
        description="Materials, texts, ICT resources, websites, or suggested support.",
    )
    interdisciplinary_connections: list[str] = Field(
        default_factory=list,
        description="Subjects or areas connected to the activity.",
    )
    estimated_time: str | None = Field(
        None, description="Suggested duration when present."
    )
    assessment: Assessment | None = Field(
        None, description="Assessment associated with the activity, if any."
    )
    source: SourceReference | None = Field(
        None, description="Source document reference."
    )
