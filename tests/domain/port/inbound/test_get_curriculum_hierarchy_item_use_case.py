from domain.port.inbound.get_curriculum_hierarchy_item_use_case import (
    GetCurriculumHierarchyItemUseCase,
)


class ConcreteGetCurriculumHierarchyItemUseCase:
    async def execute(self, id):
        return {"id": id}


class TestGetCurriculumHierarchyItemUseCase:
    async def test_given_concrete_implementation_when_method_called_then_contract_is_satisfied(
        self,
    ):
        port: GetCurriculumHierarchyItemUseCase = (
            ConcreteGetCurriculumHierarchyItemUseCase()
        )

        assert await port.execute(1) == {"id": 1}
