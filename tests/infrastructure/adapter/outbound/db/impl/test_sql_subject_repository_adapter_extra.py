from infrastructure.adapter.outbound.db.impl.sql_subject_repository_adapter import (
    SqlSubjectRepositoryAdapter,
)
from infrastructure.models import Subject
from tests.infrastructure.adapter.outbound.db.conftest import configure_first_result


class TestSqlSubjectRepositoryAdapterFindSubjectByTitleAndModality:
    async def test_given_matching_title_and_modality_when_find_then_returns_subject(
        self, session
    ):
        expected = Subject(id=1, modality_id=2, url="url", title="Math", content="html")
        configure_first_result(session, expected)
        repository = SqlSubjectRepositoryAdapter(session)

        found = await repository.find_subject_by_title_and_modality("Math", 2)

        assert found == expected
        session.exec.assert_called_once()
