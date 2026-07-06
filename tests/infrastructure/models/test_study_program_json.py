from infrastructure.models.study_program_json import StudyProgramJson


class TestStudyProgramJson:
    def test_given_values_when_created_then_keeps_content_and_tool_name(self):
        content = {"units": [{"title": "Unit 1"}]}

        model = StudyProgramJson(
            id=1,
            study_program_id=1,
            content=content,
            tool_name="pydantic-ai",
        )

        assert model.id == 1
        assert model.study_program_id == 1
        assert model.content == content
        assert model.tool_name == "pydantic-ai"
