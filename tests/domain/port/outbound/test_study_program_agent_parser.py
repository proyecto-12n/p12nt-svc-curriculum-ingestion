from domain.port.outbound.study_program_agent_parser import StudyProgramAgentParser


class ConcreteStudyProgramAgentParser:
    async def run(self, content):
        return content


class TestStudyProgramAgentParser:
    async def test_given_concrete_implementation_when_method_called_then_contract_is_satisfied(
        self,
    ):
        port: StudyProgramAgentParser = ConcreteStudyProgramAgentParser()

        assert await port.run("content") == "content"
