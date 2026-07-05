from infrastructure.adapter.outbound.db.impl.sql_grade_level_repository_adapter import (
    SqlGradeLevelRepositoryAdapter,
)
from infrastructure.models import GradeLevel
from tests.infrastructure.adapter.outbound.db.conftest import configure_first_result


class TestSqlGradeLevelRepositoryAdapterFindGradeLevelByTitleAndSubject:
    async def test_given_matching_title_and_subject_when_find_then_returns_grade_level(
        self, session
    ):
        expected = GradeLevel(id=1, parent_id=2, url="url", title="1st", content="html")
        configure_first_result(session, expected)
        repository = SqlGradeLevelRepositoryAdapter(session)

        found = await repository.find_grade_level_by_title_and_subject("1st", 2)

        assert found == expected
        session.exec.assert_called_once()
