from domain.port.outbound.curriculum_hierarchy_repository_provider import (
    CurriculumHierarchyRepositoryProvider,
)


class ConcreteCurriculumHierarchyRepositoryProvider:
    def get_repository(self, node_type):
        return node_type


class TestCurriculumHierarchyRepositoryProvider:
    async def test_given_concrete_implementation_when_method_called_then_contract_is_satisfied(
        self,
    ):
        port: CurriculumHierarchyRepositoryProvider = (
            ConcreteCurriculumHierarchyRepositoryProvider()
        )

        assert port.get_repository("type") == "type"
