from domain.port.outbound.curriculum_hierarchy_mapper_provider import (
    CurriculumHierarchyMapperProvider,
)


class ConcreteCurriculumHierarchyMapperProvider:
    def get_mapper(self, node_type):
        return node_type


class TestCurriculumHierarchyMapperProvider:
    async def test_given_concrete_implementation_when_method_called_then_contract_is_satisfied(
        self,
    ):
        port: CurriculumHierarchyMapperProvider = (
            ConcreteCurriculumHierarchyMapperProvider()
        )

        assert port.get_mapper("type") == "type"
