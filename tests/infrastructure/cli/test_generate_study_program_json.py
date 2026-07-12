from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

from infrastructure.cli import generate_study_program_json


class TestGenerateStudyProgramJsonCli:
    async def test_given_markdown_when_run_cli_then_saves_missing_json(self):
        session_context = MagicMock()
        markdown = SimpleNamespace(
            study_program_id=1,
            content="# Program",
            tool_name="pymupdf4llm",
        )
        repository = MagicMock()
        repository.list_markdowns = AsyncMock(return_value=[markdown])
        repository.find_json_by_study_program_id_and_tool_name = AsyncMock(
            return_value=None
        )
        repository.save_json = AsyncMock()
        agent_parser = MagicMock()
        output = MagicMock()
        output.model_dump.return_value = {"title": "Program"}
        agent_parser.run = AsyncMock(return_value=output)
        parser_provider = MagicMock()
        parser_provider.get_parser.return_value = agent_parser

        with (
            patch(
                "sys.argv",
                [
                    "generate_study_program_json",
                    "--markdown-tool",
                    "pymupdf4llm",
                    "--llm-agent-parser",
                    "gemini",
                ],
            ),
            patch("infrastructure.database.init_db"),
            patch("infrastructure.database.engine"),
            patch.object(
                generate_study_program_json,
                "Session",
                return_value=session_context,
            ),
            patch.object(
                generate_study_program_json,
                "SqlStudyProgramRepositoryAdapter",
                return_value=repository,
            ),
            patch.object(
                generate_study_program_json,
                "StudyProgramAgentParserProvider",
                return_value=parser_provider,
            ),
        ):
            await generate_study_program_json.run_cli()

        repository.list_markdowns.assert_awaited_once_with("pymupdf4llm", None)
        parser_provider.get_parser.assert_called_once_with("gemini")
        agent_parser.run.assert_awaited_once_with("# Program")
        output.model_dump.assert_called_once_with(mode="json")
        repository.save_json.assert_awaited_once_with(
            1,
            {"title": "Program"},
            "gemini",
        )

    async def test_given_existing_json_when_run_cli_then_skips_generation(self):
        session_context = MagicMock()
        markdown = SimpleNamespace(
            study_program_id=1,
            content="# Program",
            tool_name="pymupdf4llm",
        )
        repository = MagicMock()
        repository.list_markdowns = AsyncMock(return_value=[markdown])
        repository.find_json_by_study_program_id_and_tool_name = AsyncMock(
            return_value=SimpleNamespace(content={"title": "Existing"})
        )
        repository.save_json = AsyncMock()
        agent_parser = MagicMock()
        agent_parser.run = AsyncMock()
        parser_provider = MagicMock()
        parser_provider.get_parser.return_value = agent_parser

        with (
            patch("sys.argv", ["generate_study_program_json"]),
            patch("infrastructure.database.init_db"),
            patch("infrastructure.database.engine"),
            patch.object(
                generate_study_program_json,
                "Session",
                return_value=session_context,
            ),
            patch.object(
                generate_study_program_json,
                "SqlStudyProgramRepositoryAdapter",
                return_value=repository,
            ),
            patch.object(
                generate_study_program_json,
                "StudyProgramAgentParserProvider",
                return_value=parser_provider,
            ),
        ):
            await generate_study_program_json.run_cli()

        agent_parser.run.assert_not_awaited()
        repository.save_json.assert_not_awaited()

    async def test_given_refresh_when_json_exists_then_regenerates_json(self):
        session_context = MagicMock()
        markdown = SimpleNamespace(
            study_program_id=1,
            content="# Program",
            tool_name="pymupdf4llm",
        )
        repository = MagicMock()
        repository.list_markdowns = AsyncMock(return_value=[markdown])
        repository.find_json_by_study_program_id_and_tool_name = AsyncMock(
            return_value=SimpleNamespace(content={"title": "Existing"})
        )
        repository.save_json = AsyncMock()
        agent_parser = MagicMock()
        output = MagicMock()
        output.model_dump.return_value = {"title": "Updated"}
        agent_parser.run = AsyncMock(return_value=output)
        parser_provider = MagicMock()
        parser_provider.get_parser.return_value = agent_parser

        with (
            patch(
                "sys.argv",
                [
                    "generate_study_program_json",
                    "--llm-agent-parser",
                    "gemini",
                    "--refresh",
                ],
            ),
            patch("infrastructure.database.init_db"),
            patch("infrastructure.database.engine"),
            patch.object(
                generate_study_program_json,
                "Session",
                return_value=session_context,
            ),
            patch.object(
                generate_study_program_json,
                "SqlStudyProgramRepositoryAdapter",
                return_value=repository,
            ),
            patch.object(
                generate_study_program_json,
                "StudyProgramAgentParserProvider",
                return_value=parser_provider,
            ),
        ):
            await generate_study_program_json.run_cli()

        agent_parser.run.assert_awaited_once_with("# Program")
        repository.save_json.assert_awaited_once_with(
            1,
            {"title": "Updated"},
            "gemini",
        )

    async def test_given_study_program_id_when_run_cli_then_filters_markdowns(self):
        session_context = MagicMock()
        repository = MagicMock()
        repository.list_markdowns = AsyncMock(return_value=[])
        repository.find_json_by_study_program_id_and_tool_name = AsyncMock()
        repository.save_json = AsyncMock()
        agent_parser = MagicMock()
        parser_provider = MagicMock()
        parser_provider.get_parser.return_value = agent_parser

        with (
            patch(
                "sys.argv",
                ["generate_study_program_json", "--study-program-id", "2"],
            ),
            patch("infrastructure.database.init_db"),
            patch("infrastructure.database.engine"),
            patch.object(
                generate_study_program_json,
                "Session",
                return_value=session_context,
            ),
            patch.object(
                generate_study_program_json,
                "SqlStudyProgramRepositoryAdapter",
                return_value=repository,
            ),
            patch.object(
                generate_study_program_json,
                "StudyProgramAgentParserProvider",
                return_value=parser_provider,
            ),
        ):
            await generate_study_program_json.run_cli()

        repository.list_markdowns.assert_awaited_once_with("pymupdf4llm", 2)
        repository.save_json.assert_not_awaited()
