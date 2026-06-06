from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from src.models.users.depends import get_user_service
from src.models.users.dto_models import UsersDTO, RegisterUserRequestDTO
from src.models.users.service import UsersService

router = APIRouter()


@router.get("/me", response_model=UsersDTO, status_code=status.HTTP_200_OK)
async def get_me():
    pass
    # Сперва сделать сервис аунтификации

