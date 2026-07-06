from pydantic import BaseModel

from domain.model.grade_level_summary_report import GradeLevelSummaryReport


class GradeLevelSummaryReportResponse(BaseModel):
    ref_sum: int
    program_sum: int
    markitdown_sum: int
    pymupdf4llm_sum: int
    total: int

    @classmethod
    def from_domain(
        cls, grade_level_summary_report: GradeLevelSummaryReport
    ) -> "GradeLevelSummaryReportResponse":
        return cls(
            ref_sum=grade_level_summary_report.study_program_ref_sum,
            program_sum=grade_level_summary_report.study_program_sum,
            markitdown_sum=grade_level_summary_report.study_program_markitdown_sum,
            pymupdf4llm_sum=grade_level_summary_report.study_program_pymupdf4llm_sum,
            total=grade_level_summary_report.total,
        )
