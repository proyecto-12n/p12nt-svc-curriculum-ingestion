from domain.port.inbound.ingest_curriculum_use_case import IngestCurriculumUseCase


class ConcreteIngestCurriculumUseCase:
    async def execute(self, refresh=False, ignore_pdf_resources=False):
        return refresh, ignore_pdf_resources


class TestIngestCurriculumUseCase:
    async def test_given_concrete_implementation_when_method_called_then_contract_is_satisfied(
        self,
    ):
        port: IngestCurriculumUseCase = ConcreteIngestCurriculumUseCase()

        assert await port.execute(refresh=True, ignore_pdf_resources=True) == (
            True,
            True,
        )
