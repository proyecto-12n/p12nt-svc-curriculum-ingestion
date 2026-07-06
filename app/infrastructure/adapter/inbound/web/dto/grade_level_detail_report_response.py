from pydantic import BaseModel

from domain.model.grade_level_detail_report import GradeLevelDetailReport


class GradeLevelDetailReportResponse(BaseModel):
    id: int
    title: str
    url: str
    reference_id: int | None
    book_id: int | None
    markitdown_id: int | None
    pymupdf4llm_id: int | None

    @classmethod
    def from_domain(
        cls, grade_level_detail_report: GradeLevelDetailReport
    ) -> "GradeLevelDetailReportResponse":
        return cls(
            id=grade_level_detail_report.id,
            title=grade_level_detail_report.title,
            url=grade_level_detail_report.url,
            reference_id=grade_level_detail_report.study_program_ref_id,
            book_id=grade_level_detail_report.study_program_id,
            markitdown_id=grade_level_detail_report.study_program_markitdown_id,
            pymupdf4llm_id=grade_level_detail_report.study_program_pymupdf4llm_id,
        )
