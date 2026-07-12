from pydantic import BaseModel

from domain.model.grade_level_detail_report import GradeLevelDetailReport


class SubjectDetailReportResponse(BaseModel):
    subject_id: int
    subject_name: str
    subject_url: str
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
    ) -> "SubjectDetailReportResponse":
        return cls(
            subject_id=grade_level_detail_report.subject_id,
            subject_name=grade_level_detail_report.subject_name,
            subject_url=grade_level_detail_report.subject_url,
            id=grade_level_detail_report.grade_level_id,
            title=grade_level_detail_report.grade_level_title,
            url=grade_level_detail_report.grade_level_url,
            reference_id=grade_level_detail_report.study_program_ref_id,
            book_id=grade_level_detail_report.study_program_id,
            markitdown_id=grade_level_detail_report.study_program_markitdown_id,
            pymupdf4llm_id=grade_level_detail_report.study_program_pymupdf4llm_id,
        )
