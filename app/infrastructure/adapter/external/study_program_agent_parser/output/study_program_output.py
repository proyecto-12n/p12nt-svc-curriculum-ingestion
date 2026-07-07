from typing import Any

from pydantic import Field

from infrastructure.adapter.external.study_program_agent_parser.output.activity import Activity
from infrastructure.adapter.external.study_program_agent_parser.output.assessment import Assessment
from infrastructure.adapter.external.study_program_agent_parser.output.curriculum_item import (
    CurriculumItem,
)
from infrastructure.adapter.external.study_program_agent_parser.output.curriculum_module import (
    CurriculumModule,
)
from infrastructure.adapter.external.study_program_agent_parser.output.curriculum_output_model import (
    CurriculumOutputModel,
)
from infrastructure.adapter.external.study_program_agent_parser.output.glossary_term import GlossaryTerm
from infrastructure.adapter.external.study_program_agent_parser.output.guidance import Guidance
from infrastructure.adapter.external.study_program_agent_parser.output.learning_objective import (
    LearningObjective,
)
from infrastructure.adapter.external.study_program_agent_parser.output.schema_examples import (
    schema_examples,
)
from infrastructure.adapter.external.study_program_agent_parser.output.source_reference import (
    SourceReference,
)
from infrastructure.adapter.external.study_program_agent_parser.output.unit import Unit


class StudyProgramOutput(CurriculumOutputModel):
    model_config = schema_examples(
        {
            "title": "Programa de Estudio Ciencias para la Ciudadania 3 o 4 medio",
            "ministry": "Ministerio de Educacion",
            "responsible_unit": "Unidad de Curriculum y Evaluacion",
            "education_level": "Educacion Media",
            "modality": "Humanistico-Cientifica",
            "formation": "Formacion General",
            "grade": "3 o 4 medio",
            "subject": "Ciencias para la Ciudadania",
            "module": "Seguridad, Prevencion y Autocuidado",
            "publication_year": 2021,
            "learning_objectives": [
                {
                    "code": "OA 3",
                    "type": "OA",
                    "description": (
                        "Analizar riesgos de origen natural o provocados por "
                        "la accion humana en su contexto local."
                    ),
                    "unit_codes": ["U1"],
                }
            ],
            "units": [
                {
                    "code": "U1",
                    "number": 1,
                    "title": "Riesgos socionaturales en nuestros territorios",
                    "estimated_time": "9 semanas",
                    "objective_codes": ["OA 3"],
                }
            ],
        }
    )

    title: str | None = Field(None, description="Study program title.")
    ministry: str | None = Field(None, description="Ministry responsible for the document.")
    responsible_unit: str | None = Field(None, description="Responsible unit, division, or service.")
    education_level: str | None = Field(
        None,
        description="Education level, for example primary or secondary education.",
    )
    modality: str | None = Field(None, description="Educational modality, formation, or curriculum differentiation.")
    formation: str | None = Field(
        None,
        description="Curriculum formation type, for example general, differentiated, or technical-professional.",
    )
    grade: str | None = Field(None, description="School grade or year.")
    subject: str | None = Field(None, description="Subject, sector, module, or study program area.")
    module: str | None = Field(None, description="Module name when the PDF corresponds to a specific module.")
    decree: str | None = Field(None, description="Approval decree, resolution, or regulation indicated.")
    publication_year: int | None = Field(None, description="Document publication or edition year.")
    isbn: str | None = Field(None, description="Document ISBN, when present.")
    sources: list[SourceReference] = Field(
        default_factory=list,
        description="PDFs, pages, or sections used as sources.",
    )
    glossary: list[GlossaryTerm] = Field(
        default_factory=list,
        description="Glossary terms used to interpret the study program.",
    )
    formative_purposes: list[str] = Field(default_factory=list, description="Declared general formative purposes.")
    approaches: list[str] = Field(
        default_factory=list,
        description="Declared disciplinary, pedagogical, or curricular approaches.",
    )
    axes: list[CurriculumItem] = Field(default_factory=list, description="Curricular or thematic axes.")
    dimensions: list[CurriculumItem] = Field(
        default_factory=list,
        description="Curricular dimensions or scopes when present.",
    )
    skills: list[CurriculumItem] = Field(default_factory=list, description="Skills declared at study program level.")
    knowledge: list[CurriculumItem] = Field(
        default_factory=list,
        description="Knowledge declared at study program level.",
    )
    attitudes: list[CurriculumItem] = Field(
        default_factory=list,
        description="Attitudes declared at study program level.",
    )
    learning_objectives: list[LearningObjective] = Field(default_factory=list, description="Learning Objectives, OA.")
    general_learning_objectives: list[LearningObjective] = Field(
        default_factory=list,
        description="General Learning Objectives, OAG.",
    )
    transversal_learning_objectives: list[LearningObjective] = Field(
        default_factory=list,
        description="Transversal Learning Objectives, OAT.",
    )
    expected_learning: list[LearningObjective] = Field(
        default_factory=list,
        description="Expected learning when the document uses that category.",
    )
    annual_overview: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Annual organization, sequencing, or overview.",
    )
    modules: list[CurriculumModule] = Field(
        default_factory=list,
        description="Curriculum modules included in the study program.",
    )
    units: list[Unit] = Field(default_factory=list, description="Study program curriculum units.")
    general_guidance: list[Guidance] = Field(
        default_factory=list,
        description="General implementation, planning, didactic, or assessment guidance.",
    )
    general_activities: list[Activity] = Field(
        default_factory=list,
        description="Activities not associated with a specific unit.",
    )
    general_assessments: list[Assessment] = Field(
        default_factory=list,
        description="General assessments, instruments, or suggestions.",
    )
    bibliography: list[str] = Field(default_factory=list, description="Recommended bibliography or resources.")
    appendices: list[CurriculumItem] = Field(
        default_factory=list,
        description="Appendices or other complementary document elements.",
    )
