from fastapi import FastAPI
from starlette.responses import JSONResponse

from src.models.auth.exception import InvalidCredentials
from src.models.base.exception import ServiceException
from src.models.refresh_tokens.exception import RefreshTokenNotFound
from src.models.users.exception import UserAlreadyExit, UserNotFound


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(ServiceException)
    async def service_handler(request, exc):
        return JSONResponse(status_code=500, content={"detail": "Server Error"})

    @app.exception_handler(UserAlreadyExit)
    async def service_handler(request, exc):
        return JSONResponse(status_code=409, content={"detail": "Email already exit"})

    @app.exception_handler(InvalidCredentials)
    async def service_handler(request, exc):
        return JSONResponse(status_code=401, content={"detail": "Incorrect login or password"})

    @app.exception_handler(RefreshTokenNotFound)
    async def service_handler(request, exc):
        return JSONResponse(status_code=401, content={"detail": "Refresh token not found"})

    @app.exception_handler(UserNotFound)
    async def service_handler(request, exc):
        return JSONResponse(status_code=401, content={"detail": "User not found"})
