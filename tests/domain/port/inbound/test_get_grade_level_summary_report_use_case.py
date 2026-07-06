from domain.port.inbound.get_grade_level_summary_report_use_case import (
    GetGradeLevelSummaryReportUseCase,
)


class ConcreteGetGradeLevelSummaryReportUseCase:
    async def execute(self):
        return "summary"


class TestGetGradeLevelSummaryReportUseCase:
    async def test_given_concrete_implementation_when_method_called_then_contract_is_satisfied(
        self,
    ):
        port: GetGradeLevelSummaryReportUseCase = (
            ConcreteGetGradeLevelSummaryReportUseCase()
        )

        assert await port.execute() == "summary"
