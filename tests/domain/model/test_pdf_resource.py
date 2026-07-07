from domain.model.pdf_resource import PDFResource


class TestPDFResource:
    def test_given_pdf_bytes_when_created_then_content_is_available(self):
        resource = PDFResource(content=b"pdf")

        assert resource.content == b"pdf"
        assert resource.source_name == "unknown.pdf"
