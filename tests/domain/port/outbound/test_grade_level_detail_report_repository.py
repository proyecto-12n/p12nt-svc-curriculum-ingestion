from domain.port.outbound.grade_level_detail_report_repository import (
    GradeLevelDetailReportRepository,
)


class ConcreteGradeLevelDetailReportRepository:
    async def list_detail_report(self):
        return ["report"]


class TestGradeLevelDetailReportRepository:
    async def test_given_concrete_implementation_when_method_called_then_contract_is_satisfied(
        self,
    ):
        repository: GradeLevelDetailReportRepository = (
            ConcreteGradeLevelDetailReportRepository()
        )

        assert await repository.list_detail_report() == ["report"]
