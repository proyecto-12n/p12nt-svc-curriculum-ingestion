from pydantic import Field

from infrastructure.adapter.external.study_program_agent_parser.output.curriculum_output_model import (
    CurriculumOutputModel,
)
from infrastructure.adapter.external.study_program_agent_parser.output.glossary_term import GlossaryTerm
from infrastructure.adapter.external.study_program_agent_parser.output.schema_examples import (
    schema_examples,
)
from infrastructure.adapter.external.study_program_agent_parser.output.source_reference import (
    SourceReference,
)
from infrastructure.adapter.external.study_program_agent_parser.output.study_program_output import (
    StudyProgramOutput,
)


class NativeOutput(CurriculumOutputModel):
    model_config = schema_examples(
        {
            "study_programs": [
                {
                    "title": "Programa de Estudio Musica Quinto Ano Basico",
                    "ministry": "Ministerio de Educacion",
                    "education_level": "Educacion Basica",
                    "grade": "5 basico",
                    "subject": "Musica",
                    "units": [{"code": "U1", "number": 1, "title": "Unidad 1"}],
                }
            ],
            "global_glossary": [
                {
                    "term": "Objetivo de Aprendizaje",
                    "acronym": "OA",
                    "normalized_term": "LearningObjective",
                }
            ],
        }
    )

    study_programs: list[StudyProgramOutput] = Field(
        default_factory=list,
        description="Curriculum study programs extracted from PDFs.",
    )
    global_glossary: list[GlossaryTerm] = Field(
        default_factory=list,
        description="Consolidated glossary for curriculum term interpretation.",
    )
    sources: list[SourceReference] = Field(default_factory=list, description="Analyzed PDF source set.")
