from pydantic import BaseModel

from domain.model.grade_level_report import GradeLevelReport


class GradeLevelReportResponse(BaseModel):
    id: int
    title: str
    url: str
    study_program_ref_id: int | None
    study_program_id: int | None
    by_markitdown: int | None
    by_pymupdf4llm: int | None

    @classmethod
    def from_domain(
        cls, grade_level_report: GradeLevelReport
    ) -> "GradeLevelReportResponse":
        return cls(
            id=grade_level_report.id,
            title=grade_level_report.title,
            url=grade_level_report.url,
            study_program_ref_id=grade_level_report.study_program_ref_id,
            study_program_id=grade_level_report.study_program_id,
            by_markitdown=grade_level_report.by_markitdown,
            by_pymupdf4llm=grade_level_report.by_pymupdf4llm,
        )
