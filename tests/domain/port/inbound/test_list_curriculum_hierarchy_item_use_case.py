from domain.port.inbound.list_curriculum_hierarchy_item_use_case import (
    ListCurriculumHierarchyItemUseCase,
)


class ConcreteListCurriculumHierarchyItemUseCase:
    async def execute(self, parent_id=None):
        return [parent_id]


class TestListCurriculumHierarchyItemUseCase:
    async def test_given_concrete_implementation_when_method_called_then_contract_is_satisfied(
        self,
    ):
        port: ListCurriculumHierarchyItemUseCase = (
            ConcreteListCurriculumHierarchyItemUseCase()
        )

        assert await port.execute(3) == [3]
