from dataclasses import dataclass


@dataclass
class GradeLevelDetailReport:
    subject_id: int
    subject_name: str
    subject_url: str
    grade_level_id: int
    grade_level_title: str
    grade_level_url: str
    study_program_ref_id: int | None
    study_program_id: int | None
    study_program_markitdown_id: int | None
    study_program_pymupdf4llm_id: int | None
