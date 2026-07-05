from domain.port.outbound.pdf_converter import PDFConverter


class ConcretePDFConverter:
    def convert(self, resource):
        return "markdown"


class TestPDFConverter:
    async def test_given_concrete_implementation_when_method_called_then_contract_is_satisfied(
        self,
    ):
        port: PDFConverter = ConcretePDFConverter()

        assert port.convert(object()) == "markdown"
