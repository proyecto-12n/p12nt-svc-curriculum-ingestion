from unittest.mock import AsyncMock

from application.usecase.list_grade_level_report_usecase import (
    ListGradeLevelReportUseCaseImpl,
)


class TestListGradeLevelReportUseCaseImpl:
    async def test_given_repository_when_execute_then_delegates_to_list_report(
        self,
    ):
        repository = AsyncMock()
        repository.list_report.return_value = ["report"]
        use_case = ListGradeLevelReportUseCaseImpl(repository)

        result = await use_case.execute()

        assert result == ["report"]
        repository.list_report.assert_awaited_once_with()
