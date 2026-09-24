from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DocumentUpdate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)


class DocumentResponse(BaseModel):
    id: int
    title: str
    filename: str
    content_type: str
    uploaded_at: datetime
    user_id: int

    model_config = ConfigDict(from_attributes=True)


class DocumentListResponse(BaseModel):
    items: list[DocumentResponse]
    total: int
    skip: int
    limit: int
