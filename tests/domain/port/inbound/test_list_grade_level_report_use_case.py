from domain.port.inbound.list_grade_level_report_use_case import (
    ListGradeLevelReportUseCase,
)


class ConcreteListGradeLevelReportUseCase:
    async def execute(self):
        return ["report"]


class TestListGradeLevelReportUseCase:
    async def test_given_concrete_implementation_when_method_called_then_contract_is_satisfied(
        self,
    ):
        port: ListGradeLevelReportUseCase = ConcreteListGradeLevelReportUseCase()

        assert await port.execute() == ["report"]
