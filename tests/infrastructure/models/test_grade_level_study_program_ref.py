from infrastructure.models.grade_level_study_program_ref import (
    GradeLevelStudyProgramRef,
)


class TestGradeLevelStudyProgramRef:
    def test_given_ids_when_created_then_keeps_composite_key_values(self):
        model = GradeLevelStudyProgramRef(grade_level_id=1, study_program_ref_id=2)

        assert model.grade_level_id == 1
        assert model.study_program_ref_id == 2
