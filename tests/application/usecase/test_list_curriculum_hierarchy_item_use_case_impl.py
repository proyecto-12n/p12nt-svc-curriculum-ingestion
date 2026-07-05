from unittest.mock import AsyncMock

from application.usecase.list_curriculum_hierarchy_item_usecase import (
    ListCurriculumHierarchyItemUseCaseImpl,
)


class TestListCurriculumHierarchyItemUseCaseImpl:
    async def test_given_parent_id_when_execute_then_delegates_to_repository_list(self):
        repository = AsyncMock()
        repository.list.return_value = ["item"]
        use_case = ListCurriculumHierarchyItemUseCaseImpl(repository)

        result = await use_case.execute(parent_id=7)

        assert result == ["item"]
        repository.list.assert_awaited_once_with(7)

    async def test_given_no_parent_id_when_execute_then_lists_all_items(self):
        repository = AsyncMock()
        repository.list.return_value = []
        use_case = ListCurriculumHierarchyItemUseCaseImpl(repository)

        assert await use_case.execute() == []
        repository.list.assert_awaited_once_with(None)
