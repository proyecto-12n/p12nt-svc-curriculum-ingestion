from pydantic import BaseModel

from domain.model.grade_level_detail_report import GradeLevelDetailReport


class GradeLevelDetailReportResponse(BaseModel):
    id: int
    title: str
    url: str
    study_program_ref_id: int | None
    study_program_id: int | None
    study_program_markitdown_id: int | None
    study_program_pymupdf4llm_id: int | None

    @classmethod
    def from_domain(
        cls, grade_level_detail_report: GradeLevelDetailReport
    ) -> "GradeLevelDetailReportResponse":
        return cls(
            id=grade_level_detail_report.id,
            title=grade_level_detail_report.title,
            url=grade_level_detail_report.url,
            study_program_ref_id=grade_level_detail_report.study_program_ref_id,
            study_program_id=grade_level_detail_report.study_program_id,
            study_program_markitdown_id=grade_level_detail_report.study_program_markitdown_id,
            study_program_pymupdf4llm_id=grade_level_detail_report.study_program_pymupdf4llm_id,
        )
