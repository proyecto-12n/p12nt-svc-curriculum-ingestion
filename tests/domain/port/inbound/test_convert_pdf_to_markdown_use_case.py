from domain.port.inbound.convert_pdf_to_markdown_use_case import (
    ConvertPDFToMarkdownUseCase,
)


class ConcreteConvertPDFToMarkdownUseCase:
    async def execute(self, pdf_resource, provider_name=None):
        return "markdown"


class TestConvertPDFToMarkdownUseCase:
    async def test_given_concrete_implementation_when_method_called_then_contract_is_satisfied(
        self,
    ):
        port: ConvertPDFToMarkdownUseCase = ConcreteConvertPDFToMarkdownUseCase()

        assert await port.execute(object()) == "markdown"
