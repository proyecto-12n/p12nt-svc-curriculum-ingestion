# -*- coding: utf-8 -*-
import sys
from unittest.mock import MagicMock

# Global mocks for external packages to prevent collection failures
sys.modules["fitz"] = MagicMock()
sys.modules["pymupdf"] = MagicMock()
sys.modules["pymupdf4llm"] = MagicMock()
sys.modules["markitdown"] = MagicMock()
