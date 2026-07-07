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


class LearningResource(CurriculumOutputModel):
    model_config = schema_examples(
        {
            "title": "Sobreviviendo y evolucionando - Desastres naturales en Chile",
            "type": "video",
            "url": "https://www.youtube.com/watch?v=7JNzVZ6j3ik",
            "description": "Recurso sugerido para abordar riesgos socionaturales.",
        }
    )

    title: str | None = Field(None, description="Suggested resource title or name.")
    type: str | None = Field(None, description="Resource type: website, text, video, image, material, or other.")
    url: str | None = Field(None, description="Resource URL, when present.")
    description: str | None = Field(None, description="Suggested resource description or use.")
    source: SourceReference | None = Field(None, description="Source document reference.")
