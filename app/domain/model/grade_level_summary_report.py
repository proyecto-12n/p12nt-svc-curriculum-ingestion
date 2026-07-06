from dataclasses import dataclass


@dataclass
class GradeLevelSummaryReport:
    study_program_ref_sum: int
    study_program_sum: int
    study_program_markitdown_sum: int
    study_program_pymupdf4llm_sum: int
    total: int
