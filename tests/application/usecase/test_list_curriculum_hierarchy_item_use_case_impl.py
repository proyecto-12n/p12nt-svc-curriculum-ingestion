from unittest.mock import AsyncMock

from application.usecase.list_curriculum_hierarchy_item_usecase import (
    ListCurriculumHierarchyItemUseCaseImpl,
)


class TestListCurriculumHierarchyItemUseCaseImpl:
    def setup_method(self):
        self.repository = AsyncMock()
        self.use_case = ListCurriculumHierarchyItemUseCaseImpl(self.repository)

    async def test_given_parent_id_when_execute_then_delegates_to_repository_list(self):
        self.repository.list.return_value = ["item"]

        result = await self.use_case.execute(parent_id=7)

        assert result == ["item"]
        self.repository.list.assert_awaited_once_with(7)

    async def test_given_no_parent_id_when_execute_then_lists_all_items(self):
        self.repository.list.return_value = []

        assert await self.use_case.execute() == []
        self.repository.list.assert_awaited_once_with(None)
