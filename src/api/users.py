from fastapi import APIRouter, Depends, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from src.database.models import User
from src.schemas import UserResponse
from src.services.auth import get_current_user

router = APIRouter(prefix="/users", tags=["user"])
limiter = Limiter(key_func=get_remote_address)

@router.get('/me', response_model=UserResponse,
            response_description="Get current user info (no more than 10 requests per minute)")
@limiter.limit("10/minute")
async def get_current_user(request: Request, user: UserResponse = Depends(get_current_user)) -> User:
    return user