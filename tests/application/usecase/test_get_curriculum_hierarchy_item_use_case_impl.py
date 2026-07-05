from unittest.mock import AsyncMock

from application.usecase.get_curriculum_hierarchy_item_usecase import (
    GetCurriculumHierarchyItemUseCaseImpl,
)


class TestGetCurriculumHierarchyItemUseCaseImpl:
    async def test_given_existing_id_when_execute_then_returns_repository_item(self):
        repository = AsyncMock()
        repository.find_by_id.return_value = {"id": 1}
        use_case = GetCurriculumHierarchyItemUseCaseImpl(repository)

        result = await use_case.execute(1)

        assert result == {"id": 1}
        repository.find_by_id.assert_awaited_once_with(1)

    async def test_given_missing_id_when_execute_then_returns_none(self):
        repository = AsyncMock()
        repository.find_by_id.return_value = None
        use_case = GetCurriculumHierarchyItemUseCaseImpl(repository)

        assert await use_case.execute(99) is None
