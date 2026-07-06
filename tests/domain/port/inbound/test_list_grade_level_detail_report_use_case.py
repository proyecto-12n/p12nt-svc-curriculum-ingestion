from domain.port.inbound.list_grade_level_detail_report_use_case import (
    ListGradeLevelDetailReportUseCase,
)


class ConcreteListGradeLevelDetailReportUseCase:
    async def execute(self):
        return ["report"]


class TestListGradeLevelDetailReportUseCase:
    async def test_given_concrete_implementation_when_method_called_then_contract_is_satisfied(
        self,
    ):
        port: ListGradeLevelDetailReportUseCase = (
            ConcreteListGradeLevelDetailReportUseCase()
        )

        assert await port.execute() == ["report"]
