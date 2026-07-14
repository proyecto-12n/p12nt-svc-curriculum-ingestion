from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

from infrastructure.cli import generate_study_program_markdown


class TestGenerateStudyProgramMarkdownCli:
    async def test_given_pdf_converter_argument_when_run_cli_then_saves_missing_markdown(
        self,
    ):
        session_context = MagicMock()
        study_program = SimpleNamespace(
            id=1,
            content=b"pdf",
            url="https://example.cl/programa.pdf",
        )
        repository = MagicMock()
        repository.list = AsyncMock(return_value=[study_program])
        repository.find_markdown_by_study_program_id_and_tool_name = AsyncMock(
            return_value=None
        )
        repository.save_markdown = AsyncMock()
        use_case = MagicMock()
        use_case.execute = AsyncMock(return_value="# Program")

        with (
            patch(
                "sys.argv",
                ["generate_study_program_markdown", "--pdf-converter", "pymupdf4llm"],
            ),
            patch("infrastructure.database.init_db"),
            patch("infrastructure.database.engine"),
            patch.object(
                generate_study_program_markdown,
                "Session",
                return_value=session_context,
            ),
            patch.object(
                generate_study_program_markdown,
                "SqlStudyProgramRepositoryAdapter",
                return_value=repository,
            ),
            patch.object(
                generate_study_program_markdown,
                "ConvertPDFToMarkdownUseCaseImpl",
                return_value=use_case,
            ),
        ):
            await generate_study_program_markdown.run_cli()

        repository.find_markdown_by_study_program_id_and_tool_name.assert_awaited_once_with(
            1,
            "pymupdf4llm",
        )
        use_case.execute.assert_awaited_once()
        resource, provider_name = use_case.execute.await_args.args
        assert resource.content == b"pdf"
        assert resource.source_name == "https://example.cl/programa.pdf"
        assert provider_name == "pymupdf4llm"
        repository.save_markdown.assert_awaited_once_with(
            study_program,
            "# Program",
            "pymupdf4llm",
        )

    async def test_given_existing_markdown_when_run_cli_then_skips_generation(self):
        session_context = MagicMock()
        study_program = SimpleNamespace(
            id=1,
            content=b"pdf",
            url="https://example.cl/programa.pdf",
        )
        repository = MagicMock()
        repository.list = AsyncMock(return_value=[study_program])
        repository.find_markdown_by_study_program_id_and_tool_name = AsyncMock(
            return_value=SimpleNamespace(content="# Existing")
        )
        repository.save_markdown = AsyncMock()
        use_case = MagicMock()
        use_case.execute = AsyncMock()

        with (
            patch("sys.argv", ["generate_study_program_markdown"]),
            patch("infrastructure.database.init_db"),
            patch("infrastructure.database.engine"),
            patch.object(
                generate_study_program_markdown,
                "Session",
                return_value=session_context,
            ),
            patch.object(
                generate_study_program_markdown,
                "SqlStudyProgramRepositoryAdapter",
                return_value=repository,
            ),
            patch.object(
                generate_study_program_markdown,
                "ConvertPDFToMarkdownUseCaseImpl",
                return_value=use_case,
            ),
        ):
            await generate_study_program_markdown.run_cli()

        use_case.execute.assert_not_awaited()
        repository.save_markdown.assert_not_awaited()

    async def test_given_study_program_id_when_run_cli_then_processes_only_that_program(
        self,
    ):
        session_context = MagicMock()
        study_program = SimpleNamespace(
            id=2,
            content=b"pdf",
            url="https://example.cl/programa.pdf",
        )
        repository = MagicMock()
        repository.list = AsyncMock()
        repository.find_by_id = AsyncMock(return_value=study_program)
        repository.find_markdown_by_study_program_id_and_tool_name = AsyncMock(
            return_value=None
        )
        repository.save_markdown = AsyncMock()
        use_case = MagicMock()
        use_case.execute = AsyncMock(return_value="# Program")

        with (
            patch(
                "sys.argv",
                ["generate_study_program_markdown", "--study-program-id", "2"],
            ),
            patch("infrastructure.database.init_db"),
            patch("infrastructure.database.engine"),
            patch.object(
                generate_study_program_markdown,
                "Session",
                return_value=session_context,
            ),
            patch.object(
                generate_study_program_markdown,
                "SqlStudyProgramRepositoryAdapter",
                return_value=repository,
            ),
            patch.object(
                generate_study_program_markdown,
                "ConvertPDFToMarkdownUseCaseImpl",
                return_value=use_case,
            ),
        ):
            await generate_study_program_markdown.run_cli()

        repository.find_by_id.assert_awaited_once_with(2)
        repository.list.assert_not_awaited()
        repository.save_markdown.assert_awaited_once()

    async def test_given_init_db_disabled_when_run_cli_then_skips_database_init(self):
        session_context = MagicMock()
        repository = MagicMock()
        repository.list = AsyncMock(return_value=[])

        with (
            patch("sys.argv", ["generate_study_program_markdown"]),
            patch.object(
                generate_study_program_markdown.settings,
                "P12NT_CURRICULUM_INIT_DB",
                False,
            ),
            patch("infrastructure.database.init_db") as init_db,
            patch("infrastructure.database.engine"),
            patch.object(
                generate_study_program_markdown,
                "Session",
                return_value=session_context,
            ),
            patch.object(
                generate_study_program_markdown,
                "SqlStudyProgramRepositoryAdapter",
                return_value=repository,
            ),
        ):
            await generate_study_program_markdown.run_cli()

        init_db.assert_not_called()
