from domain.port.outbound.grade_level_report_repository import (
    GradeLevelReportRepository,
)


class ConcreteGradeLevelReportRepository:
    async def list_report(self):
        return ["report"]


class TestGradeLevelReportRepository:
    async def test_given_concrete_implementation_when_method_called_then_contract_is_satisfied(
        self,
    ):
        repository: GradeLevelReportRepository = ConcreteGradeLevelReportRepository()

        assert await repository.list_report() == ["report"]
