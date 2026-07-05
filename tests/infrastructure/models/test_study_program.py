from infrastructure.models.study_program import StudyProgram


class TestStudyProgram:
    def test_given_explicit_parent_alias_when_created_then_parent_id_is_set(self):
        model = StudyProgram(
            id=1,
            study_program_ref_id=2,
            url="url",
            title="title",
            checksum="checksum",
            content=b"pdf",
        )

        assert model.parent_id == 2
        assert model.study_program_ref_id == 2

    def test_given_parent_alias_when_updated_then_parent_id_changes(self):
        model = StudyProgram(
            id=1,
            parent_id=2,
            url="url",
            title="title",
            checksum="checksum",
            content=b"pdf",
        )

        model.study_program_ref_id = 3

        assert model.parent_id == 3
