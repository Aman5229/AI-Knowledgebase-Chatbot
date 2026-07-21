from pydantic import BaseModel, Field, ConfigDict

class DocumentCreate(BaseModel):
  title: str = Field(..., min_length=1, max_length=255)
  filename: str = Field(..., min_length=1, max_length=255)

class DocumentResponse(BaseModel):
  id: int
  title: str
  filename: str

  model_config = ConfigDict(from_attributes=True)