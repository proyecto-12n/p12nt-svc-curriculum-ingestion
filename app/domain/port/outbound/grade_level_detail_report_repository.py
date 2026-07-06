from typing import Protocol

from domain.model.grade_level_detail_report import GradeLevelDetailReport


class GradeLevelDetailReportRepository(Protocol):
    async def list_detail_report(self) -> list[GradeLevelDetailReport]: ...
