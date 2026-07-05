from infrastructure.adapter.external.study_program_agent_parser.llm_model_factory import (
    LLMModelFactory,
)


class ConcreteLLMModelFactory:
    def create_model(self, settings):
        return settings


class TestLLMModelFactory:
    def test_given_concrete_factory_when_create_model_then_contract_is_satisfied(self):
        factory: LLMModelFactory = ConcreteLLMModelFactory()

        assert factory.create_model("settings") == "settings"
