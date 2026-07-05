from domain.port.outbound.curriculum_hierarchy_mapper import CurriculumHierarchyMapper


class ConcreteCurriculumHierarchyMapper:
    def to_edge(self, model):
        return model

    def to_model(self, edge):
        return edge


class TestCurriculumHierarchyMapper:
    async def test_given_concrete_implementation_when_method_called_then_contract_is_satisfied(
        self,
    ):
        port: CurriculumHierarchyMapper = ConcreteCurriculumHierarchyMapper()

        assert port.to_edge("model") == "model"
        assert port.to_model("edge") == "edge"
