from unittest.mock import MagicMock, patch

import pytest

from app.config import Settings
from infrastructure.adapter.external.study_program_agent_parser_provider import (
    StudyProgramAgentParserProvider,
)


class TestStudyProgramAgentParserProvider:
    def test_given_configured_parser_when_get_parser_then_returns_cached_parser(self):
        settings = Settings(llm_agent_parser="gemini", gemini_api_key="secret")
        provider = StudyProgramAgentParserProvider(settings)
        factory = MagicMock()
        model = MagicMock()
        factory.create_model.return_value = model
        provider._factories["gemini"] = factory
        parser_class = MagicMock()
        parser = MagicMock()
        parser_class.return_value = parser

        with patch(
            "infrastructure.adapter.external.study_program_agent_parser_provider.PydanticAiStudyProgramAgentParser",
            new=parser_class,
        ):
            first = provider.get_parser()
            second = provider.get_parser("gemini")

        assert first == parser
        assert second == parser
        factory.create_model.assert_called_once_with(settings)

    def test_given_unknown_parser_name_when_get_parser_then_raises_value_error(self):
        provider = StudyProgramAgentParserProvider(
            Settings(llm_agent_parser="gemini", gemini_api_key="secret")
        )

        with pytest.raises(ValueError, match="Unknown LLM model type"):
            provider.get_parser("unknown")
