from infrastructure.adapter.outbound.db.impl.sql_study_program_repository_adapter import (
    SqlStudyProgramRepositoryAdapter,
)
from infrastructure.models import StudyProgram, StudyProgramMarkdown
from infrastructure.util import generate_id
from tests.infrastructure.adapter.outbound.db.conftest import (
    configure_all_result,
    configure_first_result,
)


class TestSqlStudyProgramRepositoryAdapter:
    async def test_given_id_when_find_by_id_then_returns_first_exec_result(
        self, session
    ):
        expected = StudyProgram(
            id=1,
            parent_id=10,
            url="url",
            title="title",
            content=b"pdf",
            checksum="abc",
        )
        configure_first_result(session, expected)
        repository = SqlStudyProgramRepositoryAdapter(session)

        result = await repository.find_by_id(1)

        assert result == expected
        session.exec.assert_called_once()

    async def test_given_url_when_find_by_url_then_returns_first_exec_result(
        self, session
    ):
        expected = StudyProgram(
            id=1,
            parent_id=10,
            url="url",
            title="title",
            content=b"pdf",
            checksum="abc",
        )
        configure_first_result(session, expected)
        repository = SqlStudyProgramRepositoryAdapter(session)

        result = await repository.find_by_url("url")

        assert result == expected
        session.exec.assert_called_once()

    async def test_given_parent_filter_when_list_then_returns_matching_records(
        self, session
    ):
        expected = [
            StudyProgram(
                id=1,
                parent_id=10,
                url="url",
                title="title",
                content=b"pdf",
                checksum="abc",
            )
        ]
        configure_all_result(session, expected)
        repository = SqlStudyProgramRepositoryAdapter(session)

        result = await repository.list(10)

        assert result == expected
        session.exec.assert_called_once()

    async def test_given_new_model_when_save_then_adds_commits_and_refreshes_model(
        self, session
    ):
        configure_first_result(session, None)
        repository = SqlStudyProgramRepositoryAdapter(session)
        model = StudyProgram(
            id=1,
            parent_id=10,
            url="url",
            title="title",
            content=b"pdf",
            checksum="abc",
        )

        result = await repository.save(model)

        assert result == model
        session.add.assert_called_once()
        session.commit.assert_called_once()
        session.refresh.assert_called_once()

    async def test_given_existing_model_when_save_then_updates_without_add(
        self, session
    ):
        existing = StudyProgram(
            id=1,
            parent_id=10,
            url="url",
            title="old",
            content=b"old",
            checksum="old",
        )
        configure_first_result(session, existing)
        repository = SqlStudyProgramRepositoryAdapter(session)
        model = StudyProgram(
            id=1,
            parent_id=11,
            url="url",
            title="updated",
            content=b"pdf",
            checksum="abc",
        )

        result = await repository.save(model)

        assert result == model
        assert existing.parent_id == 11
        assert existing.title == "updated"
        assert existing.content == b"pdf"
        assert existing.checksum == "abc"
        session.add.assert_not_called()
        session.commit.assert_called_once()
        session.refresh.assert_called_once_with(existing)

    async def test_given_study_program_id_and_tool_when_find_markdown_then_returns_first_exec_result(
        self, session
    ):
        expected = StudyProgramMarkdown(
            id=1,
            study_program_id=1,
            content="# Program",
            tool_name="pymupdf4llm",
        )
        configure_first_result(session, expected)
        repository = SqlStudyProgramRepositoryAdapter(session)

        result = await repository.find_markdown_by_study_program_id_and_tool_name(
            1, "pymupdf4llm"
        )

        assert result == expected
        session.exec.assert_called_once()

    async def test_given_new_markdown_when_save_markdown_then_adds_commits_and_refreshes(
        self, session
    ):
        configure_first_result(session, None)
        repository = SqlStudyProgramRepositoryAdapter(session)
        study_program = StudyProgram(
            id=1,
            parent_id=10,
            url="url",
            title="Program",
            content=b"pdf",
            checksum="abc",
        )

        result = await repository.save_markdown(
            study_program, "# Program", "pymupdf4llm"
        )

        assert result.id == generate_id("pymupdf4llm", "Program")
        assert result.study_program_id == 1
        assert result.content == "# Program"
        assert result.tool_name == "pymupdf4llm"
        session.add.assert_called_once()
        session.commit.assert_called_once()
        session.refresh.assert_called_once_with(result)

    async def test_given_existing_markdown_when_save_markdown_then_updates_without_add(
        self, session
    ):
        existing = StudyProgramMarkdown(
            id=1,
            study_program_id=1,
            content="# Old",
            tool_name="pymupdf4llm",
        )
        configure_first_result(session, existing)
        repository = SqlStudyProgramRepositoryAdapter(session)
        study_program = StudyProgram(
            id=1,
            parent_id=10,
            url="url",
            title="Program",
            content=b"pdf",
            checksum="abc",
        )

        result = await repository.save_markdown(
            study_program, "# Program", "pymupdf4llm"
        )

        assert result == existing
        assert existing.content == "# Program"
        assert existing.tool_name == "pymupdf4llm"
        session.add.assert_not_called()
        session.commit.assert_called_once()
        session.refresh.assert_called_once_with(existing)

    async def test_given_different_tool_when_save_markdown_then_adds_new_record(
        self, session
    ):
        configure_first_result(session, None)
        repository = SqlStudyProgramRepositoryAdapter(session)
        study_program = StudyProgram(
            id=1,
            parent_id=10,
            url="url",
            title="Program",
            content=b"pdf",
            checksum="abc",
        )

        result = await repository.save_markdown(study_program, "# Gemini", "gemini")

        assert result.id == generate_id("gemini", "Program")
        assert result.study_program_id == 1
        assert result.content == "# Gemini"
        assert result.tool_name == "gemini"
        session.add.assert_called_once()

    async def test_given_markdown_tool_when_list_markdowns_then_returns_matching_records(
        self, session
    ):
        expected = [
            StudyProgramMarkdown(
                id=1,
                study_program_id=1,
                content="# Program",
                tool_name="pymupdf4llm",
            )
        ]
        configure_all_result(session, expected)
        repository = SqlStudyProgramRepositoryAdapter(session)

        result = await repository.list_markdowns("pymupdf4llm")

        assert result == expected
        session.exec.assert_called_once()

    async def test_given_markdown_tool_and_study_program_id_when_list_markdowns_then_returns_matching_records(
        self, session
    ):
        expected = [
            StudyProgramMarkdown(
                id=1,
                study_program_id=2,
                content="# Program",
                tool_name="pymupdf4llm",
            )
        ]
        configure_all_result(session, expected)
        repository = SqlStudyProgramRepositoryAdapter(session)

        result = await repository.list_markdowns("pymupdf4llm", 2)

        assert result == expected
        session.exec.assert_called_once()
