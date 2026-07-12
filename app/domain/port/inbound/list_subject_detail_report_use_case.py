from typing import Protocol

from domain.model.grade_level_detail_report import GradeLevelDetailReport


class ListSubjectDetailReportUseCase(Protocol):
    async def execute(self) -> list[GradeLevelDetailReport]: ...
