"""
NextProject 2026

This file is part of the NP Collector Curriculum project.
Unauthorized copying of this file, via any medium is strictly prohibited.
"""

from pydantic_ai.models import Model
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.ollama import OllamaProvider

from infrastructure.adapter.external.study_program_agent_parser.llm_model_factory import (
    LLMModelFactory,
)
from app.config import Settings


class OllamaModelFactory(LLMModelFactory):
    """
    Concrete factory for Ollama models.
    """

    def create_model(self, settings: Settings) -> Model:
        provider = OllamaProvider(base_url=settings.ollama_llm_base_url)
        return OllamaModel(model_name=settings.ollama_llm_model_name, provider=provider)
