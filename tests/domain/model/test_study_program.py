from datetime import datetime

from domain.model.study_program import StudyProgram


class TestStudyProgram:
    def test_given_valid_values_when_created_then_stores_values_and_extraction_time(
        self,
    ):
        model = StudyProgram(
            id=1,
            study_program_ref_id=2,
            url="url",
            title="title",
            content=b"pdf",
            checksum="abc",
        )

        assert model.content == b"pdf"
        assert isinstance(model.extracted_at, datetime)

    def test_given_checksum_when_reading_md5sum_then_returns_checksum_alias(self):
        model = StudyProgram(1, 2, "url", "title", b"pdf", "abc")

        assert model.md5sum == "abc"
