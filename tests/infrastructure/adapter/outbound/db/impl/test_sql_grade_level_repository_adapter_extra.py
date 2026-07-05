from infrastructure.adapter.outbound.db.impl.sql_grade_level_repository_adapter import (
    SqlGradeLevelRepositoryAdapter,
)
from infrastructure.models import GradeLevel


class TestSqlGradeLevelRepositoryAdapterFindGradeLevelByTitleAndSubject:
    async def test_given_matching_title_and_subject_when_find_then_returns_grade_level(
        self, session
    ):
        repository = SqlGradeLevelRepositoryAdapter(session)
        await repository.save(
            GradeLevel(id=1, subject_id=2, url="url", title="1st", content="html")
        )

        found = await repository.find_grade_level_by_title_and_subject("1st", 2)

        assert found is not None
        assert found.url == "url"
