from typing import Protocol

from domain.model.grade_level_report import GradeLevelReport


class GradeLevelReportRepository(Protocol):
    async def list_report(self) -> list[GradeLevelReport]: ...
