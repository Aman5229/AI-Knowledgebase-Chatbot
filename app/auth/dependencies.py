from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from app.auth.jwt import verify_access_token
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.dependencies import get_db
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
  payload = verify_access_token(token)
  user_id = payload.get("sub")

  if user_id is None:
    raise HTTPException(status_code=401, detail="Invalid token")

  try:
    user_id = int(user_id)
  except (TypeError, ValueError):
    raise HTTPException(
        status_code=401,
        detail="Could not validate credentials"
    )

  stmt = select(User).where(User.id == user_id)
  result = db.execute(stmt)
  user = result.scalar_one_or_none()

  if user is None:
    raise HTTPException(status_code=401, detail="Could not validate credentials")

  return user
