from pydantic import BaseModel

from infrastructure.adapter.inbound.web.dto.markdown_size_response import (
    MarkdownSizeResponse,
)


class DataQualityKPIResponse(BaseModel):
    study_programs_without_pdf_count: int
    study_programs_without_markdown_count: int
    duplicate_resource_url_count: int
    orphan_hierarchy_items_count: int
    empty_content_count: int
    markdown_size_bytes: list[MarkdownSizeResponse]
