from domain.model.grade_level_report import GradeLevelReport
from domain.port.inbound.list_grade_level_report_use_case import (
    ListGradeLevelReportUseCase,
)
from domain.port.outbound.grade_level_report_repository import (
    GradeLevelReportRepository,
)


class ListGradeLevelReportUseCaseImpl(ListGradeLevelReportUseCase):
    def __init__(self, repository: GradeLevelReportRepository):
        self.repository = repository

    async def execute(self) -> list[GradeLevelReport]:
        return await self.repository.list_report()
