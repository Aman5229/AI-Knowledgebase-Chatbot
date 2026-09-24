from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.auth.security import hash_password, verify_password
from app.schemas.user import UserCreate, UserLogin
from sqlalchemy import select

class UserService:
  @staticmethod
  def create_user(db: Session, user_data: UserCreate) -> User:
    stmt = select(User).where(User.email == user_data.email)
    result = db.execute(stmt)
    existing_user = result.scalar_one_or_none()
    if existing_user:
      raise HTTPException(status_code=409, detail="Email should be unique")

    hashed_password = hash_password(user_data.password)
    user = User(email = user_data.email, password_hash = hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)

    return user

  @staticmethod
  def authenticate_user(db: Session, user_data: UserLogin) -> User:
    stmt = select(User).where(User.email == user_data.email)
    result = db.execute(stmt)
    user = result.scalar_one_or_none()

    if user is None:
      raise HTTPException(status_code=401, detail="Unauthorized")
    if not verify_password(user_data.password, user.password_hash):
      raise HTTPException(status_code=401, detail="Unauthorized")

    return user
