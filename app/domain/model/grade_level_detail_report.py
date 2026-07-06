from dataclasses import dataclass


@dataclass
class GradeLevelDetailReport:
    id: int
    title: str
    url: str
    study_program_ref_id: int | None
    study_program_id: int | None
    study_program_markitdown_id: int | None
    study_program_pymupdf4llm_id: int | None
