# -*- coding: utf-8 -*-
import sys
from unittest.mock import MagicMock, AsyncMock, patch

# Mock optional/external libraries so import succeeds without installing them
sys.modules["fitz"] = MagicMock()
sys.modules["pymupdf4llm"] = MagicMock()
sys.modules["markitdown"] = MagicMock()

import pytest
import httpx

from app.domain.model.node import Node
from app.domain.model.resource_type import ResourceType
from app.domain.model.pdf_resource import PDFResource
from app.config import Settings
from app.infrastructure.adapter.external.downloader.html_downloader import HTMLDownloader
from app.infrastructure.adapter.external.downloader.pdf_downloader import PDFDownloader
from app.infrastructure.adapter.external.downloader_provider import DownloaderProvider
from app.infrastructure.adapter.external.pdf_converter.pymupdf_pdf_converter import PyMuPDFPDFConverter
from app.infrastructure.adapter.external.pdf_converter.markitdown_pdf_converter import MarkItDownPDFConverter
from app.infrastructure.adapter.external.pdf_converter_provider import PDFConverterProvider
from app.infrastructure.adapter.external.study_program_agent_parser.ollama_model_factory import OllamaModelFactory
from app.infrastructure.adapter.external.study_program_agent_parser.gemini_model_factory import GeminiModelFactory
from app.infrastructure.adapter.external.study_program_agent_parser.pydantic_ai_study_program_agent_parser import PydanticAiStudyProgramAgentParser
from app.infrastructure.adapter.external.study_program_agent_parser_provider import StudyProgramAgentParserProvider


@pytest.mark.asyncio
async def test_html_downloader():
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.text = "<html><body>Hello</body></html>"
    mock_response.raise_for_status = MagicMock()
    
    mock_client = AsyncMock(spec=httpx.AsyncClient)
    mock_client.get.return_value = mock_response
    mock_client.__aenter__.return_value = mock_client
    
    with patch("httpx.AsyncClient", return_value=mock_client):
        downloader = HTMLDownloader()
        node = await downloader.download("http://example.com/html")
        assert node.url == "http://example.com/html"
        assert node.type == ResourceType.HTML
        assert "Hello" in node.content


@pytest.mark.asyncio
async def test_pdf_downloader():
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.content = b"pdf-bytes"
    mock_response.raise_for_status = MagicMock()
    
    mock_client = AsyncMock(spec=httpx.AsyncClient)
    mock_client.get.return_value = mock_response
    mock_client.__aenter__.return_value = mock_client
    
    with patch("httpx.AsyncClient", return_value=mock_client):
        downloader = PDFDownloader()
        node = await downloader.download("http://example.com/pdf")
        assert node.url == "http://example.com/pdf"
        assert node.type == ResourceType.PDF
        assert node.content == b"pdf-bytes"


def test_downloader_provider():
    provider = DownloaderProvider()
    html_dl = provider.get_downloader(ResourceType.HTML)
    pdf_dl = provider.get_downloader(ResourceType.PDF)
    assert isinstance(html_dl, HTMLDownloader)
    assert isinstance(pdf_dl, PDFDownloader)
    
    with pytest.raises(ValueError, match="No downloader configured"):
        provider.get_downloader(None)


def test_pymupdf_pdf_converter():
    mock_doc = MagicMock()
    with patch("app.infrastructure.adapter.external.pdf_converter.pymupdf_pdf_converter.Document", return_value=mock_doc) as mock_doc_class, \
         patch("app.infrastructure.adapter.external.pdf_converter.pymupdf_pdf_converter.pymupdf4llm") as mock_pymupdf4llm:
        mock_pymupdf4llm.to_markdown.return_value = "markdown content"
        
        converter = PyMuPDFPDFConverter()
        res = PDFResource(content=b"bytes")
        result = converter.convert(res)
        
        assert result == "markdown content"
        mock_doc_class.assert_called_once()
        mock_pymupdf4llm.to_markdown.assert_called_once_with(
            mock_doc, header=False, use_ocr=False, show_progress=True, write_images=False
        )


def test_markitdown_pdf_converter():
    mock_mid = MagicMock()
    mock_response = MagicMock()
    mock_response.markdown = "markdown from markitdown"
    mock_mid.convert_stream.return_value = mock_response
    
    with patch("app.infrastructure.adapter.external.pdf_converter.markitdown_pdf_converter.MarkItDown", return_value=mock_mid) as mock_mid_class, \
         patch("app.infrastructure.adapter.external.pdf_converter.markitdown_pdf_converter.StreamInfo") as mock_stream_info:
        
        converter = MarkItDownPDFConverter()
        res = PDFResource(content=b"bytes")
        result = converter.convert(res)
        
        assert result == "markdown from markitdown"
        mock_mid_class.assert_called_once()
        mock_mid.convert_stream.assert_called_once()


def test_pdf_converter_provider():
    provider = PDFConverterProvider()
    with patch("app.infrastructure.adapter.external.pdf_converter.markitdown_pdf_converter.MarkItDownPDFConverter") as mock_mid_class, \
         patch("app.infrastructure.adapter.external.pdf_converter.pymupdf_pdf_converter.PyMuPDFPDFConverter") as mock_pymupdf_class:
        
        mock_mid_inst = MagicMock()
        mock_mid_class.return_value = mock_mid_inst
        mock_mid_class.__name__ = "MarkItDownPDFConverter"
        
        mock_pymupdf_inst = MagicMock()
        mock_pymupdf_class.return_value = mock_pymupdf_inst
        mock_pymupdf_class.__name__ = "PyMuPDFPDFConverter"
        
        mid_conv = provider.get_converter("markitdown")
        assert mid_conv == mock_mid_inst
        
        pymu_conv = provider.get_converter("pymupdf4llm")
        assert pymu_conv == mock_pymupdf_inst
        
        with pytest.raises(ValueError, match="No PDF converter found with name"):
            provider.get_converter("invalid_name")


def test_ollama_model_factory():
    with patch("app.infrastructure.adapter.external.study_program_agent_parser.ollama_model_factory.OllamaProvider") as mock_provider_class, \
         patch("app.infrastructure.adapter.external.study_program_agent_parser.ollama_model_factory.OllamaModel") as mock_model_class:
        
        mock_provider = MagicMock()
        mock_provider_class.return_value = mock_provider
        mock_model = MagicMock()
        mock_model_class.return_value = mock_model
        
        factory = OllamaModelFactory()
        settings = Settings(llm_base_url_ollama="http://test-ollama", llm_model_name_ollama="my-llama")
        result = factory.create_model(settings)
        
        assert result == mock_model
        mock_provider_class.assert_called_once_with(base_url="http://test-ollama")
        mock_model_class.assert_called_once_with(model_name="my-llama", provider=mock_provider)


def test_gemini_model_factory():
    with patch("app.infrastructure.adapter.external.study_program_agent_parser.gemini_model_factory.GoogleProvider") as mock_provider_class, \
         patch("app.infrastructure.adapter.external.study_program_agent_parser.gemini_model_factory.GoogleModel") as mock_model_class:
        
        mock_provider = MagicMock()
        mock_provider_class.return_value = mock_provider
        mock_model = MagicMock()
        mock_model_class.return_value = mock_model
        
        factory = GeminiModelFactory()
        settings = Settings(gemini_api_key="secret-key", llm_model_name_gemini="gemini-test")
        result = factory.create_model(settings)
        
        assert result == mock_model
        mock_provider_class.assert_called_once_with(api_key="secret-key")
        mock_model_class.assert_called_once_with("gemini-test", provider=mock_provider)
        
        settings_no_key = Settings(gemini_api_key=None)
        with pytest.raises(ValueError, match="GEMINI_API_KEY is not set"):
            factory.create_model(settings_no_key)


@pytest.mark.asyncio
async def test_pydantic_ai_study_program_agent_parser():
    mock_agent_class = MagicMock()
    mock_agent_instance = MagicMock()
    mock_agent_class.return_value = mock_agent_instance
    
    mock_result = MagicMock()
    mock_result.output = "parsed study program"
    
    mock_agent_instance.run = AsyncMock(return_value=mock_result)
    
    with patch("app.infrastructure.adapter.external.study_program_agent_parser.pydantic_ai_study_program_agent_parser.Agent", new=mock_agent_class):
        mock_model = MagicMock()
        parser = PydanticAiStudyProgramAgentParser(model=mock_model)
        
        result = await parser.run("document text")
        assert result == "parsed study program"
        mock_agent_instance.run.assert_called_once()


def test_study_program_agent_parser_provider():
    settings = Settings(llm_agent_parser="gemini", gemini_api_key="api-key")
    
    mock_gemini_factory = MagicMock()
    mock_gemini_model = MagicMock()
    mock_gemini_factory.create_model.return_value = mock_gemini_model
    
    mock_parser_class = MagicMock()
    mock_parser_instance = MagicMock()
    mock_parser_class.return_value = mock_parser_instance
    
    provider = StudyProgramAgentParserProvider(settings)
    provider._factories["gemini"] = mock_gemini_factory
    
    with patch("app.infrastructure.adapter.external.study_program_agent_parser_provider.PydanticAiStudyProgramAgentParser", new=mock_parser_class):
        parser = provider.get_parser()
        assert parser == mock_parser_instance
        mock_gemini_factory.create_model.assert_called_once_with(settings)
        mock_parser_class.assert_called_once_with(model=mock_gemini_model)
        
        parser_cached = provider.get_parser("gemini")
        assert parser_cached == mock_parser_instance
        
        with pytest.raises(ValueError, match="Unknown LLM model type"):
            provider.get_parser("unknown-model")
