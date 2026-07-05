from domain.model.curriculum_hierarchy_type import CurriculumHierarchyType


class TestCurriculumHierarchyType:
    def test_given_hierarchy_type_when_reading_value_then_returns_wire_value(self):
        assert CurriculumHierarchyType.CURRICULUM.value == "curriculum"
        assert CurriculumHierarchyType.STUDY_PROGRAM.value == "study_program"
