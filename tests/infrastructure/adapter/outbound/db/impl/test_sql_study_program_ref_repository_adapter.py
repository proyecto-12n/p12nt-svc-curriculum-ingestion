from infrastructure.adapter.outbound.db.impl.sql_study_program_ref_repository_adapter import (
    SqlStudyProgramRefRepositoryAdapter,
)
from infrastructure.models import StudyProgramRef


class TestSqlStudyProgramRefRepositoryAdapter:
    async def test_given_new_model_when_save_then_can_find_by_id_and_url(self, session):
        repository = SqlStudyProgramRefRepositoryAdapter(session)
        model = StudyProgramRef(
            id=1, grade_level_id=10, url="url", title="title", content="html"
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
        repository = SqlStudyProgramRefRepositoryAdapter(session)
        model = StudyProgramRef(
            id=1, grade_level_id=10, url="url", title="title", content="html"
        )
        await repository.save(model)
        model.title = "updated"

        await repository.save(model)
        found = await repository.find_by_url("url")

        assert found.title == "updated"

    async def test_given_parent_filter_when_list_then_returns_matching_records(
        self, session
    ):
        repository = SqlStudyProgramRefRepositoryAdapter(session)
        await repository.save(
            StudyProgramRef(
                id=1, grade_level_id=10, url="url", title="title", content="html"
            )
        )

        listed = await repository.list(10)

        assert len(listed) == 1
        assert listed[0].parent_id == 10
