from domain.model.grade_level_summary_report import GradeLevelSummaryReport
from domain.port.inbound.get_subject_summary_report_use_case import (
    GetSubjectSummaryReportUseCase,
)
from domain.port.outbound.grade_level_detail_report_repository import (
    GradeLevelDetailReportRepository,
)


class GetSubjectSummaryReportUseCaseImpl(GetSubjectSummaryReportUseCase):
    def __init__(self, repository: GradeLevelDetailReportRepository):
        self.repository = repository

    async def execute(self) -> GradeLevelSummaryReport:
        reports = await self.repository.list_detail_report()
        study_program_ref_sum = sum(
            1 for report in reports if report.study_program_ref_id is not None
        )
        study_program_sum = sum(
            1 for report in reports if report.study_program_id is not None
        )
        study_program_markitdown_sum = sum(
            1 for report in reports if report.study_program_markitdown_id is not None
        )
        study_program_pymupdf4llm_sum = sum(
            1 for report in reports if report.study_program_pymupdf4llm_id is not None
        )

        return GradeLevelSummaryReport(
            study_program_ref_sum=study_program_ref_sum,
            study_program_sum=study_program_sum,
            study_program_markitdown_sum=study_program_markitdown_sum,
            study_program_pymupdf4llm_sum=study_program_pymupdf4llm_sum,
            total=(len(reports)),
        )
