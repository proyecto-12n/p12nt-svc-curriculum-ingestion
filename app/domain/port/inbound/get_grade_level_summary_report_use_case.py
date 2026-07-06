from typing import Protocol

from domain.model.grade_level_summary_report import GradeLevelSummaryReport


class GetGradeLevelSummaryReportUseCase(Protocol):
    async def execute(self) -> GradeLevelSummaryReport: ...
