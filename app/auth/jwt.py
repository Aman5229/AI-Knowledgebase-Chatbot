from fastapi import HTTPException
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from app.core.config import settings

def create_access_token(data: dict) -> str:
  to_encode = data.copy()
  expiry = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
  to_encode["exp"] = expiry

  return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

def verify_access_token(token: str) -> dict:
    try:
      payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])

      return payload
    except JWTError:
       raise HTTPException(status_code=401, detail="Unauthorized")
