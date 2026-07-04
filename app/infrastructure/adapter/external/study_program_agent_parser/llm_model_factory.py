"""
NextProject 2026

This file is part of the NP Collector Curriculum project.
Unauthorized copying of this file, via any medium is strictly prohibited.
"""

from abc import ABC, abstractmethod
from typing import Protocol

from pydantic_ai.models import Model

from app.config import Settings


class LLMModelFactory(Protocol):
    """
    Abstract Factory for creating PydanticAI Model instances (Factory Method Pattern).
    """

    @abstractmethod
    def create_model(self, settings: Settings) -> Model:
        """
        Creates and returns a PydanticAI Model.
        """
        ...
