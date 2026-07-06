from dataclasses import dataclass


@dataclass
class GradeLevelReport:
    id: int
    title: str
    url: str
    study_program_ref_id: int | None
    study_program_id: int | None
    by_markitdown: int | None
    by_pymupdf4llm: int | None
