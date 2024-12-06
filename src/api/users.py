from fastapi import APIRouter, Depends

from src.database.models import User
from src.schemas import UserResponse
from src.services.auth import get_current_user

router = APIRouter(prefix="/users", tags=["user"])

@router.get('/me', response_model=UserResponse,
            response_description="Get current user info")
async def get_current_user(user: UserResponse = Depends(get_current_user)) -> User:
    return user