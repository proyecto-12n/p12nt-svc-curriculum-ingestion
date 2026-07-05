from pydantic import BaseModel


class MarkdownSizeResponse(BaseModel):
    study_program_id: int
    tool_name: str
    size_bytes: int
