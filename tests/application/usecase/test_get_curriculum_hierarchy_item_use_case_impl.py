from unittest.mock import AsyncMock

from application.usecase.get_curriculum_hierarchy_item_usecase import (
    GetCurriculumHierarchyItemUseCaseImpl,
)


class TestGetCurriculumHierarchyItemUseCaseImpl:
    def setup_method(self):
        self.repository = AsyncMock()
        self.use_case = GetCurriculumHierarchyItemUseCaseImpl(self.repository)

    async def test_given_existing_id_when_execute_then_returns_repository_item(self):
        self.repository.find_by_id.return_value = {"id": 1}

        result = await self.use_case.execute(1)

        assert result == {"id": 1}
        self.repository.find_by_id.assert_awaited_once_with(1)

    async def test_given_missing_id_when_execute_then_returns_none(self):
        self.repository.find_by_id.return_value = None

        assert await self.use_case.execute(99) is None
