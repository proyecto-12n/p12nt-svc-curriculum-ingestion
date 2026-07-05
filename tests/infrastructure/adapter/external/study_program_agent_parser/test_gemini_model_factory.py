from unittest.mock import MagicMock, patch

import pytest

from app.config import Settings
from infrastructure.adapter.external.study_program_agent_parser.gemini_model_factory import (
    GeminiModelFactory,
)


class TestGeminiModelFactory:
    def test_given_api_key_when_create_model_then_uses_google_provider_and_model(self):
        with (
            patch(
                "infrastructure.adapter.external.study_program_agent_parser.gemini_model_factory.GoogleProvider"
            ) as provider_class,
            patch(
                "infrastructure.adapter.external.study_program_agent_parser.gemini_model_factory.GoogleModel"
            ) as model_class,
        ):
            provider = MagicMock()
            model = MagicMock()
            provider_class.return_value = provider
            model_class.return_value = model
            settings = Settings(gemini_api_key="secret", gemini_llm_model_name="gemini")

            result = GeminiModelFactory().create_model(settings)

        assert result == model
        provider_class.assert_called_once_with(api_key="secret")
        model_class.assert_called_once_with("gemini", provider=provider)

    def test_given_missing_api_key_when_create_model_then_raises_value_error(self):
        with pytest.raises(ValueError, match="GEMINI_API_KEY is not set"):
            GeminiModelFactory().create_model(Settings(gemini_api_key=None))
