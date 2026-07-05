from infrastructure.adapter.outbound.db.impl.sql_subject_repository_adapter import (
    SqlSubjectRepositoryAdapter,
)
from infrastructure.models import Subject
from tests.infrastructure.adapter.outbound.db.conftest import (
    configure_all_result,
    configure_first_result,
)


class TestSqlSubjectRepositoryAdapter:
    async def test_given_id_when_find_by_id_then_returns_first_exec_result(
        self, session
    ):
        expected = Subject(
            id=1, modality_id=10, url="url", title="title", content="html"
        )
        configure_first_result(session, expected)
        repository = SqlSubjectRepositoryAdapter(session)

        result = await repository.find_by_id(1)

        assert result == expected
        session.exec.assert_called_once()

    async def test_given_url_when_find_by_url_then_returns_first_exec_result(
        self, session
    ):
        expected = Subject(
            id=1, modality_id=10, url="url", title="title", content="html"
        )
        configure_first_result(session, expected)
        repository = SqlSubjectRepositoryAdapter(session)

        result = await repository.find_by_url("url")

        assert result == expected
        session.exec.assert_called_once()

    async def test_given_parent_filter_when_list_then_returns_matching_records(
        self, session
    ):
        expected = [
            Subject(id=1, modality_id=10, url="url", title="title", content="html")
        ]
        configure_all_result(session, expected)
        repository = SqlSubjectRepositoryAdapter(session)

        result = await repository.list(10)

        assert result == expected
        session.exec.assert_called_once()

    async def test_given_new_model_when_save_then_adds_commits_and_refreshes_model(
        self, session
    ):
        configure_first_result(session, None)
        repository = SqlSubjectRepositoryAdapter(session)
        model = Subject(id=1, modality_id=10, url="url", title="title", content="html")

        result = await repository.save(model)

        assert result == model
        session.add.assert_called_once()
        session.commit.assert_called_once()
        session.refresh.assert_called_once()

    async def test_given_existing_model_when_save_then_updates_without_add(
        self, session
    ):
        existing = Subject(id=1, modality_id=10, url="url", title="old", content="old")
        configure_first_result(session, existing)
        repository = SqlSubjectRepositoryAdapter(session)
        model = Subject(
            id=1, modality_id=11, url="updated-url", title="updated", content="html"
        )

        result = await repository.save(model)

        assert result == model
        assert existing.url == "updated-url"
        assert existing.parent_id == 11
        assert existing.title == "updated"
        assert existing.content == "html"
        session.add.assert_not_called()
        session.commit.assert_called_once()
        session.refresh.assert_called_once_with(existing)
