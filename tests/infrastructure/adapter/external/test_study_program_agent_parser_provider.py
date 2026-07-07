from unittest.mock import MagicMock, patch

import pytest

from app.config import Settings
from infrastructure.adapter.external.study_program_agent_parser_provider import (
    StudyProgramAgentParserProvider,
)


class TestStudyProgramAgentParserProvider:
    def setup_method(self):
        self.settings = Settings(llm_agent_parser="gemini", gemini_api_key="secret")
        self.provider = StudyProgramAgentParserProvider(self.settings)

    def test_given_configured_parser_when_get_parser_then_returns_cached_parser(self):
        factory = MagicMock()
        model = MagicMock()
        factory.create_model.return_value = model
        self.provider._factories["gemini"] = factory
        parser_class = MagicMock()
        parser = MagicMock()
        parser_class.return_value = parser

        with patch(
            "infrastructure.adapter.external.study_program_agent_parser_provider.PydanticAiStudyProgramAgentParser",
            new=parser_class,
        ):
            first = self.provider.get_parser()
            second = self.provider.get_parser("gemini")

        assert first == parser
        assert second == parser
        factory.create_model.assert_called_once_with(self.settings)

    def test_given_unknown_parser_name_when_get_parser_then_raises_value_error(self):
        with pytest.raises(ValueError, match="Unknown LLM model type"):
            self.provider.get_parser("unknown")
