from pydantic import BaseModel, ConfigDict


class CurriculumOutputModel(BaseModel):
    model_config = ConfigDict(extra="allow")
