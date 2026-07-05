from infrastructure.adapter.outbound.db.impl.sql_subject_repository_adapter import (
    SqlSubjectRepositoryAdapter,
)
from infrastructure.models import Subject


class TestSqlSubjectRepositoryAdapterFindSubjectByTitleAndModality:
    async def test_given_matching_title_and_modality_when_find_then_returns_subject(
        self, session
    ):
        repository = SqlSubjectRepositoryAdapter(session)
        await repository.save(
            Subject(id=1, modality_id=2, url="url", title="Math", content="html")
        )

        found = await repository.find_subject_by_title_and_modality("Math", 2)

        assert found is not None
        assert found.url == "url"
