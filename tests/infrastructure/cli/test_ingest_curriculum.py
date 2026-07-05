from unittest.mock import MagicMock, patch

from infrastructure.cli import ingest_curriculum


class TestIngestCurriculumCli:
    def test_given_pdf_converter_argument_when_run_cli_then_uses_converter_name(self):
        session = MagicMock()
        session_context = MagicMock()
        session_context.__enter__.return_value = session
        use_case = MagicMock()
        use_case.execute.return_value = None

        with (
            patch("sys.argv", ["ingest_curriculum", "--pdf-converter", "markitdown"]),
            patch("infrastructure.database.init_db"),
            patch("infrastructure.database.engine"),
            patch.object(ingest_curriculum, "Session", return_value=session_context),
            patch.object(
                ingest_curriculum, "IngestCurriculumUseCaseImpl"
            ) as use_case_class,
            patch("asyncio.run"),
        ):
            use_case_class.return_value = use_case
            ingest_curriculum.run_cli()

        assert use_case_class.call_args.kwargs["markdown_tool_name"] == "markitdown"
