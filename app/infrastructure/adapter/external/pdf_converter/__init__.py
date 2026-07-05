import importlib
import sys

_pymupdf_module = importlib.import_module(
    "infrastructure.adapter.external.pdf_converter.impl.pymupdf_pdf_converter"
)
_markitdown_module = importlib.import_module(
    "infrastructure.adapter.external.pdf_converter.impl.markitdown_pdf_converter"
)

sys.modules[__name__ + ".pymupdf_pdf_converter"] = _pymupdf_module
sys.modules[__name__ + ".markitdown_pdf_converter"] = _markitdown_module

pymupdf_pdf_converter = _pymupdf_module
markitdown_pdf_converter = _markitdown_module
