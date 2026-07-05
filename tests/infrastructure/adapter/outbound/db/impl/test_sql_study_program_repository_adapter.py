from infrastructure.adapter.outbound.db.impl.sql_study_program_repository_adapter import (
    SqlStudyProgramRepositoryAdapter,
)
from infrastructure.models import StudyProgram


class TestSqlStudyProgramRepositoryAdapter:
    async def test_given_new_model_when_save_then_can_find_by_id_and_url(self, session):
        repository = SqlStudyProgramRepositoryAdapter(session)
        model = StudyProgram(
            id=1,
            study_program_ref_id=10,
            url="url",
            title="title",
            content=b"pdf",
            checksum="abc",
        )

        saved = await repository.save(model)
        by_id = await repository.find_by_id(saved.id)
        by_url = await repository.find_by_url("url")

        assert by_id is not None
        assert by_url is not None
        assert by_url.title == "title"

    async def test_given_existing_model_when_save_then_updates_existing_record(
        self, session
    ):
        repository = SqlStudyProgramRepositoryAdapter(session)
        model = StudyProgram(
            id=1,
            study_program_ref_id=10,
            url="url",
            title="title",
            content=b"pdf",
            checksum="abc",
        )
        await repository.save(model)
        model.title = "updated"

        await repository.save(model)
        found = await repository.find_by_url("url")

        assert found.title == "updated"

    async def test_given_parent_filter_when_list_then_returns_matching_records(
        self, session
    ):
        repository = SqlStudyProgramRepositoryAdapter(session)
        await repository.save(
            StudyProgram(
                id=1,
                study_program_ref_id=10,
                url="url",
                title="title",
                content=b"pdf",
                checksum="abc",
            )
        )

        listed = await repository.list(10)

        assert len(listed) == 1
        assert listed[0].parent_id == 10
