from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from src.models.users.depends import get_user_service
from src.models.users.models_dto import UsersDTO, RegisterUserRequestDTO
from src.models.users.service import UsersService

router = APIRouter(prefix="/users")


@router.get("/me", response_model=UsersDTO, status_code=status.HTTP_200_OK)
async def get_me():
    pass
    # Сперва сделать сервис аунтификации

