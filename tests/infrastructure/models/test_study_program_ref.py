from infrastructure.models.study_program_ref import StudyProgramRef


class TestStudyProgramRef:
    def test_given_parent_id_when_created_then_parent_id_is_set(self):
        model = StudyProgramRef(
            id=1, parent_id=2, url="url", title="title", content="html"
        )

        assert model.parent_id == 2
