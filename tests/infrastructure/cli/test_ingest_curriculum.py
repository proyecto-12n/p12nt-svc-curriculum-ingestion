from unittest.mock import AsyncMock, MagicMock, patch

from infrastructure.cli import ingest_curriculum


class TestIngestCurriculumCli:
    async def test_given_ignore_pdf_resources_argument_when_run_cli_then_passes_option(
        self,
    ):
        session = MagicMock()
        session_context = MagicMock()
        session_context.__enter__.return_value = session
        use_case = MagicMock()
        use_case.execute = AsyncMock()

        with (
            patch("sys.argv", ["ingest_curriculum", "--ignore-pdf-resources"]),
            patch("infrastructure.database.init_db"),
            patch("infrastructure.database.engine"),
            patch.object(ingest_curriculum, "Session", return_value=session_context),
            patch.object(
                ingest_curriculum, "IngestCurriculumUseCaseImpl"
            ) as use_case_class,
        ):
            use_case_class.return_value = use_case
            await ingest_curriculum.run_cli()

        use_case.execute.assert_awaited_once_with(
            refresh=False,
            ignore_pdf_resources=True,
            reprocess_titles=False,
        )

    async def test_given_reprocess_titles_argument_when_run_cli_then_passes_option(
        self,
    ):
        session = MagicMock()
        session_context = MagicMock()
        session_context.__enter__.return_value = session
        use_case = MagicMock()
        use_case.execute = AsyncMock()

        with (
            patch("sys.argv", ["ingest_curriculum", "--reprocess-titles"]),
            patch("infrastructure.database.init_db"),
            patch("infrastructure.database.engine"),
            patch.object(ingest_curriculum, "Session", return_value=session_context),
            patch.object(
                ingest_curriculum, "IngestCurriculumUseCaseImpl"
            ) as use_case_class,
        ):
            use_case_class.return_value = use_case
            await ingest_curriculum.run_cli()

        use_case.execute.assert_awaited_once_with(
            refresh=False,
            ignore_pdf_resources=False,
            reprocess_titles=True,
        )

    async def test_given_init_db_disabled_when_run_cli_then_skips_database_init(self):
        session = MagicMock()
        session_context = MagicMock()
        session_context.__enter__.return_value = session
        use_case = MagicMock()
        use_case.execute = AsyncMock()

        with (
            patch("sys.argv", ["ingest_curriculum"]),
            patch.object(ingest_curriculum.settings, "P12NT_CURRICULUM_INIT_DB", False),
            patch("infrastructure.database.init_db") as init_db,
            patch("infrastructure.database.engine"),
            patch.object(ingest_curriculum, "Session", return_value=session_context),
            patch.object(
                ingest_curriculum, "IngestCurriculumUseCaseImpl"
            ) as use_case_class,
        ):
            use_case_class.return_value = use_case
            await ingest_curriculum.run_cli()

        init_db.assert_not_called()
