from infrastructure.adapter.outbound.db.impl.sql_curriculum_repository_adapter import (
    SqlCurriculumRepositoryAdapter,
)
from infrastructure.models import Curriculum
from tests.infrastructure.adapter.outbound.db.conftest import (
    configure_all_result,
    configure_first_result,
)


class TestSqlCurriculumRepositoryAdapter:
    async def test_given_id_when_find_by_id_then_returns_first_exec_result(
        self, session
    ):
        expected = Curriculum(id=1, url="url", title="title", content="html")
        configure_first_result(session, expected)
        repository = SqlCurriculumRepositoryAdapter(session)

        result = await repository.find_by_id(1)

        assert result == expected
        session.exec.assert_called_once()

    async def test_given_url_when_find_by_url_then_returns_first_exec_result(
        self, session
    ):
        expected = Curriculum(id=1, url="url", title="title", content="html")
        configure_first_result(session, expected)
        repository = SqlCurriculumRepositoryAdapter(session)

        result = await repository.find_by_url("url")

        assert result == expected
        session.exec.assert_called_once()

    async def test_given_no_parent_filter_when_list_then_returns_all_exec_results(
        self, session
    ):
        expected = [Curriculum(id=1, url="url", title="title", content="html")]
        configure_all_result(session, expected)
        repository = SqlCurriculumRepositoryAdapter(session)

        result = await repository.list(None)

        assert result == expected
        session.exec.assert_called_once()

    async def test_given_new_model_when_save_then_adds_commits_and_refreshes_model(
        self, session
    ):
        configure_first_result(session, None)
        repository = SqlCurriculumRepositoryAdapter(session)
        model = Curriculum(id=1, url="url", title="title", content="html")

        result = await repository.save(model)

        assert result == model
        session.add.assert_called_once()
        session.commit.assert_called_once()
        session.refresh.assert_called_once()

    async def test_given_existing_model_when_save_then_updates_without_add(
        self, session
    ):
        existing = Curriculum(id=1, url="url", title="old", content="old")
        configure_first_result(session, existing)
        repository = SqlCurriculumRepositoryAdapter(session)
        model = Curriculum(id=1, url="url", title="updated", content="html")

        result = await repository.save(model)

        assert result == model
        assert existing.title == "updated"
        assert existing.content == "html"
        session.add.assert_not_called()
        session.commit.assert_called_once()
        session.refresh.assert_called_once_with(existing)
