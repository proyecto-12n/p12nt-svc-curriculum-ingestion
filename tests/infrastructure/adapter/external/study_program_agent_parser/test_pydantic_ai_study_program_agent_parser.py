from unittest.mock import AsyncMock, MagicMock, patch

from infrastructure.adapter.external.study_program_agent_parser.pydantic_ai_study_program_agent_parser import (
    PydanticAiStudyProgramAgentParser,
)


class TestPydanticAiStudyProgramAgentParser:
    async def test_given_content_when_run_then_returns_agent_output(self):
        agent_class = MagicMock()
        agent = MagicMock()
        result = MagicMock()
        result.output = "parsed"
        agent.run = AsyncMock(return_value=result)
        agent_class.return_value = agent

        with patch(
            "infrastructure.adapter.external.study_program_agent_parser.pydantic_ai_study_program_agent_parser.Agent",
            new=agent_class,
        ):
            parser = PydanticAiStudyProgramAgentParser(model=MagicMock())
            output = await parser.run("content")

        assert output == "parsed"
        agent.run.assert_awaited_once()
