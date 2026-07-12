from types import SimpleNamespace
from unittest.mock import AsyncMock

from application.usecase.get_subject_summary_report_usecase import (
    GetSubjectSummaryReportUseCaseImpl,
)


class TestGetSubjectSummaryReportUseCaseImpl:
    async def test_given_detail_reports_when_execute_then_counts_not_null_ids(self):
        repository = AsyncMock()
        repository.list_detail_report.return_value = [
            SimpleNamespace(
                id=1,
                study_program_ref_id=2,
                study_program_id=3,
                study_program_markitdown_id=4,
                study_program_pymupdf4llm_id=None,
            ),
            SimpleNamespace(
                id=5,
                study_program_ref_id=None,
                study_program_id=6,
                study_program_markitdown_id=None,
                study_program_pymupdf4llm_id=7,
            ),
            SimpleNamespace(
                id=8,
                study_program_ref_id=None,
                study_program_id=None,
                study_program_markitdown_id=None,
                study_program_pymupdf4llm_id=None,
            ),
        ]
        use_case = GetSubjectSummaryReportUseCaseImpl(repository)

        result = await use_case.execute()

        assert result.study_program_ref_sum == 1
        assert result.study_program_sum == 2
        assert result.study_program_markitdown_sum == 1
        assert result.study_program_pymupdf4llm_sum == 1
        assert result.total == 3
        repository.list_detail_report.assert_awaited_once_with()
