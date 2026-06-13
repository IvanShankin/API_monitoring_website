from fastapi import FastAPI
from starlette.responses import JSONResponse

from src.models.auth.exception import InvalidCredentials
from src.models.base.exception import ServiceException, NoDataForUpdate
from src.models.refresh_tokens.exception import RefreshTokenNotFound
from src.models.users.exception import UserAlreadyExit, UserNotFound
from src.models.utils.exception import NotPermission


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(ServiceException)
    async def service_handler(request, exc):
        return JSONResponse(status_code=500, content={"detail": "Server Error"})

    @app.exception_handler(UserAlreadyExit)
    async def service_handler(request, exc):
        return JSONResponse(status_code=409, content={"detail": "Email already exit"})

    @app.exception_handler(NotPermission)
    async def service_handler(request, exc):
        return JSONResponse(status_code=403, content={"detail": "Not permission"})

    @app.exception_handler(InvalidCredentials)
    async def service_handler(request, exc):
        return JSONResponse(status_code=401, content={"detail": "Incorrect login or password"})

    @app.exception_handler(RefreshTokenNotFound)
    async def service_handler(request, exc):
        return JSONResponse(status_code=401, content={"detail": "Refresh token not found"})

    @app.exception_handler(UserNotFound)
    async def service_handler(request, exc):
        return JSONResponse(status_code=401, content={"detail": "User not found"})

    @app.exception_handler(NoDataForUpdate)
    async def service_handler(request, exc):
        return JSONResponse(status_code=400, content={"detail": "did not transmit data"})
