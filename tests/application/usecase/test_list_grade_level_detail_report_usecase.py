from unittest.mock import AsyncMock

from application.usecase.list_grade_level_detail_report_usecase import (
    ListGradeLevelDetailReportUseCaseImpl,
)


class TestListGradeLevelDetailReportUseCaseImpl:
    async def test_given_repository_when_execute_then_delegates_to_list_detail_report(
        self,
    ):
        repository = AsyncMock()
        repository.list_detail_report.return_value = ["report"]
        use_case = ListGradeLevelDetailReportUseCaseImpl(repository)

        result = await use_case.execute()

        assert result == ["report"]
        repository.list_detail_report.assert_awaited_once_with()
