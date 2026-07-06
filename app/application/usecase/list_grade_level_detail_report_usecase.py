from domain.model.grade_level_detail_report import GradeLevelDetailReport
from domain.port.inbound.list_grade_level_detail_report_use_case import (
    ListGradeLevelDetailReportUseCase,
)
from domain.port.outbound.grade_level_detail_report_repository import (
    GradeLevelDetailReportRepository,
)


class ListGradeLevelDetailReportUseCaseImpl(ListGradeLevelDetailReportUseCase):
    def __init__(self, repository: GradeLevelDetailReportRepository):
        self.repository = repository

    async def execute(self) -> list[GradeLevelDetailReport]:
        return await self.repository.list_detail_report()
