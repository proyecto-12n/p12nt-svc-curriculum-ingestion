"""
NextProject 2026

This file is part of the NP Collector Curriculum project.
Unauthorized copying of this file, via any medium is strictly prohibited.
"""

from typing import Dict

from infrastructure.adapter.external.study_program_agent_parser.pydantic_ai_study_program_agent_parser import (
    PydanticAiStudyProgramAgentParser,
)
from infrastructure.adapter.external.study_program_agent_parser import (
    LLMModelFactory,
    OllamaModelFactory,
    GeminiModelFactory,
)
from app.config import Settings


class StudyProgramAgentParserProvider:
    """
    Provider for resolving the appropriate StudyProgramAgentParser implementation.
    """

    def __init__(self, settings: Settings):
        self.settings = settings
        self._factories: Dict[str, LLMModelFactory] = {
            "ollama": OllamaModelFactory(),
            "gemini": GeminiModelFactory(),
        }
        self._registry: Dict[str, PydanticAiStudyProgramAgentParser] = {}

    def get_parser(self, name: str | None = None) -> PydanticAiStudyProgramAgentParser:
        """
        Get an instance of a StudyProgramAgentParser.
        If name is None, falls back to the setting from the configuration.
        """
        parser_name = name or self.settings.llm_agent_parser

        if parser_name not in self._registry:
            factory = self._factories.get(parser_name)
            if not factory:
                raise ValueError(f"Unknown LLM model type: {parser_name}")

            model = factory.create_model(self.settings)
            self._registry[parser_name] = PydanticAiStudyProgramAgentParser(model=model)

        return self._registry[parser_name]
