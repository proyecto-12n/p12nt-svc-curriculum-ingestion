from domain.port.outbound.pdf_converter_provider import PDFConverterProvider


class ConcretePDFConverterProvider:
    def get_converter(self, provider_name=None):
        return provider_name


class TestPDFConverterProvider:
    async def test_given_concrete_implementation_when_method_called_then_contract_is_satisfied(
        self,
    ):
        port: PDFConverterProvider = ConcretePDFConverterProvider()

        assert port.get_converter("name") == "name"
