import infrastructure.adapter.external.study_program_agent_parser.output as output
from infrastructure.adapter.external.study_program_agent_parser.output import (
    Activity,
    ActivityType,
    Assessment,
    CurriculumItem,
    CurriculumModule,
    EvaluationIndicator,
    GlossaryTerm,
    Guidance,
    GuidanceType,
    LearningObjective,
    LearningObjectiveType,
    LearningResource,
    SourceReference,
    StudyProgramOutput,
    Unit,
)
from infrastructure.adapter.external.study_program_agent_parser.output.schema_examples import (
    schema_examples,
)


class TestStudyProgramOutput:
    def test_given_output_package_when_imported_then_exports_all_models(self):
        assert set(output.__all__) == {
            "Activity",
            "ActivityType",
            "Assessment",
            "CurriculumItem",
            "CurriculumModule",
            "EvaluationIndicator",
            "GlossaryTerm",
            "Guidance",
            "GuidanceType",
            "LearningObjective",
            "LearningObjectiveType",
            "LearningResource",
            "SourceReference",
            "StudyProgramOutput",
            "Unit",
        }

    def test_given_nested_payload_when_validate_then_builds_study_program_output(self):
        result = StudyProgramOutput.model_validate(
            {
                "title": "Programa",
                "learning_objectives": [
                    {
                        "type": "OA",
                        "code": "OA 1",
                        "description": "Leer textos.",
                        "extra_field": "kept",
                    }
                ],
                "units": [
                    {
                        "code": "U1",
                        "activities": [
                            {
                                "type": "aprendizaje",
                                "title": "Actividad 1",
                                "resources": [{"title": "Video"}],
                            }
                        ],
                        "guidance": [{"description": "Orientar la clase."}],
                        "assessments": [{"title": "Evaluacion"}],
                    }
                ],
                "glossary": [{"term": "Objetivo de Aprendizaje"}],
                "sources": [{"document": "programa.pdf", "page": 1}],
            }
        )

        objective = result.learning_objectives[0]
        unit = result.units[0]

        assert result.title == "Programa"
        assert objective.type == LearningObjectiveType.OA
        assert objective.model_extra == {"extra_field": "kept"}
        assert unit.activities[0].type == ActivityType.LEARNING
        assert unit.activities[0].resources[0].title == "Video"
        assert unit.guidance[0].description == "Orientar la clase."
        assert result.glossary[0].term == "Objetivo de Aprendizaje"
        assert result.sources[0].document == "programa.pdf"

    def test_given_models_when_created_without_optional_lists_then_defaults_are_empty(
        self,
    ):
        assert StudyProgramOutput().units == []
        assert Unit().activities == []
        assert Activity().resources == []
        assert Assessment().indicators == []
        assert CurriculumModule().units == []
        assert LearningObjective(type=LearningObjectiveType.OA).indicators == []

    def test_given_schema_examples_when_created_then_keeps_examples_and_extra_allowed(
        self,
    ):
        config = schema_examples({"field": "value"})

        assert config["extra"] == "allow"
        assert config["json_schema_extra"] == {"examples": [{"field": "value"}]}

    def test_given_leaf_models_when_created_then_store_values(self):
        source = SourceReference(document="programa.pdf", page=2)
        item = CurriculumItem(code="Eje 1", source=source)
        indicator = EvaluationIndicator(objective_code="OA 1")
        resource = LearningResource(title="Video", url="https://example.cl")
        glossary = GlossaryTerm(term="OA", source=source)
        guidance = Guidance(
            description="Planificar evaluacion.",
            type=GuidanceType.ASSESSMENT,
        )

        assert item.source == source
        assert indicator.objective_code == "OA 1"
        assert resource.url == "https://example.cl"
        assert glossary.source == source
        assert guidance.type == GuidanceType.ASSESSMENT
