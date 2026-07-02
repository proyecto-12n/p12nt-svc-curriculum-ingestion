"""
NextProject 2026

This file is part of the NP Collector Curriculum project.
Unauthorized copying of this file, via any medium is strictly prohibited.
"""

from pydantic_ai.models import Model
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider

from app.infrastructure.adapter.external.study_program_agent_parser.llm_model_factory import (
    LLMModelFactory,
)
from app.config import Settings


class GeminiModelFactory(LLMModelFactory):
    """
    Concrete factory for Gemini models.
    """

    def create_model(self, settings: Settings) -> Model:
        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is not set or provided.")
        google_provider = GoogleProvider(api_key=settings.gemini_api_key)
        return GoogleModel(settings.gemini_llm_model_name, provider=google_provider)
