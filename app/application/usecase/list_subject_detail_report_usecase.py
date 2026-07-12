from typing import List

from domain.model.grade_level_detail_report import GradeLevelDetailReport
from domain.port.inbound.list_subject_detail_report_use_case import (
    ListSubjectDetailReportUseCase,
)
from domain.port.outbound.grade_level_detail_report_repository import (
    GradeLevelDetailReportRepository,
)


class ListSubjectDetailReportUseCaseImpl(ListSubjectDetailReportUseCase):
    def __init__(self, repository: GradeLevelDetailReportRepository):
        self.repository = repository

    async def execute(self) -> List[GradeLevelDetailReport]:
        return await self.repository.list_detail_report()
