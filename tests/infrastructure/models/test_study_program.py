from infrastructure.models.study_program import StudyProgram


class TestStudyProgram:
    def test_given_parent_id_when_created_then_parent_id_is_set(self):
        model = StudyProgram(
            id=1,
            parent_id=2,
            url="url",
            title="title",
            checksum="checksum",
            content=b"pdf",
        )

        assert model.parent_id == 2
