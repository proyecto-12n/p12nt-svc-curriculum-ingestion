from infrastructure.models.study_program_markdown import StudyProgramMarkdown


class TestStudyProgramMarkdown:
    def test_given_values_when_created_then_keeps_content_and_tool_name(self):
        model = StudyProgramMarkdown(
            id=1,
            study_program_id=1,
            content="# Program",
            tool_name="pymupdf4llm",
        )

        assert model.id == 1
        assert model.study_program_id == 1
        assert model.content == "# Program"
        assert model.tool_name == "pymupdf4llm"
