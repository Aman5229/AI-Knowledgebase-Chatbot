from pydantic import BaseModel, Field, ConfigDict, EmailStr

class UserCreate(BaseModel):
  email: EmailStr
  password: str = Field(..., min_length=8, max_length=255)

class UserResponse(BaseModel):
  id: int
  email: EmailStr

  model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
  email: EmailStr
  password: str = Field(..., min_length=8, max_length=255)

class UserToken(BaseModel):
  access_token: str
  token_type: str
