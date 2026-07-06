from typing import Protocol

from domain.model.grade_level_report import GradeLevelReport


class ListGradeLevelReportUseCase(Protocol):
    async def execute(self) -> list[GradeLevelReport]: ...
