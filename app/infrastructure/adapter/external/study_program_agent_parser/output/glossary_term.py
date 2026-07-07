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


class GlossaryTerm(CurriculumOutputModel):
    model_config = schema_examples(
        {
            "term": "Objetivo de Aprendizaje",
            "acronym": "OA",
            "definition": "Desempeno que se espera que los estudiantes logren en una asignatura, modulo o nivel.",
            "normalized_term": "LearningObjective",
        }
    )

    term: str = Field(..., description="Curricular or technical term used in the source.")
    acronym: str | None = Field(None, description="Associated acronym, when present.")
    definition: str | None = Field(None, description="Definition provided by the glossary or study program.")
    normalized_term: str | None = Field(None, description="Homologated name used by the model.")
    source: SourceReference | None = Field(None, description="Place where the term was defined.")
