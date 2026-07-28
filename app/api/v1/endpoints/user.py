from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.schemas.user import UserCreate, UserResponse, UserToken, UserLogin
from app.auth.jwt import create_access_token
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/create_user", response_model=UserResponse)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
  return UserService.create_user(db, user_data)

@router.post("/login", response_model=UserToken)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
  user = UserService.authenticate_user(db, user_data)
  access_token = create_access_token({"subject": str(user.id)})

  return {
    "access_token": access_token,
    "token_type": "bearer"
  }
