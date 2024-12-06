from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.database.models import User
from src.schemas import CreateUser, UserResponse, Token
from src.services.auth import Hash, create_access_token
from src.services.users import UserService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register",
             response_model=UserResponse,
             response_description="Create a new user",
             status_code=status.HTTP_201_CREATED)
async def register_user(user_data: CreateUser,
                        db: AsyncSession = Depends(get_db)) -> User:
    user_service = UserService(db)
    email_user = await user_service.get_user_by_email(user_data.email)
    if email_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"User with email {user_data.email} already exists")
    username_user = await user_service.get_user_by_username(user_data.username)
    if username_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"User with username {user_data.username} already exists")
    user_data.password = Hash().get_password_hash(user_data.password)
    new_user = await user_service.create_user(user_data)
    return new_user


@router.post("/login",
             response_model=Token,
             response_description="Login user",
             status_code=status.HTTP_200_OK)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(),
                     db: AsyncSession = Depends(get_db)) -> dict:
    user_service = UserService(db)
    user = await user_service.get_user_by_username(form_data.username)
    if not user or not Hash().verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})

    access_token = await create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}