from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.schemas.user import UserCreate, UserResponse, UserToken, UserLogin
from app.auth.jwt import create_access_token
from app.services.user_service import UserService
from app.models.user import User
from app.auth.dependencies import get_current_user
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/create_user", response_model=UserResponse)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
  return UserService.create_user(db, user_data)

@router.post("/login", response_model=UserToken)
@router.post("/login", response_model=UserToken)
def login(form_data: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    user_data = UserLogin(
        email=form_data.username,
        password=form_data.password,
    )

    user = UserService.authenticate_user(db, user_data)
    access_token = create_access_token({"sub": str(user.id)})

    return {"access_token": access_token,"token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
  return current_user
