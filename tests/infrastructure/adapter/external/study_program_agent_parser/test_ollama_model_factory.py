from unittest.mock import MagicMock, patch

from app.config import Settings
from infrastructure.adapter.external.study_program_agent_parser.ollama_model_factory import (
    OllamaModelFactory,
)


class TestOllamaModelFactory:
    def test_given_settings_when_create_model_then_uses_ollama_provider_and_model(self):
        with (
            patch(
                "infrastructure.adapter.external.study_program_agent_parser.ollama_model_factory.OllamaProvider"
            ) as provider_class,
            patch(
                "infrastructure.adapter.external.study_program_agent_parser.ollama_model_factory.OllamaModel"
            ) as model_class,
        ):
            provider = MagicMock()
            model = MagicMock()
            provider_class.return_value = provider
            model_class.return_value = model
            settings = Settings(
                ollama_llm_base_url="https://ollama", ollama_llm_model_name="llama"
            )

            result = OllamaModelFactory().create_model(settings)

        assert result == model
        provider_class.assert_called_once_with(base_url="https://ollama")
        model_class.assert_called_once_with(model_name="llama", provider=provider)
