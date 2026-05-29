from fastapi import FastAPI
from starlette.responses import JSONResponse

from src.models.base.exception import ServiceException
from src.models.users.exception import UserAlreadyExit


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(ServiceException)
    async def service_handler(request, exc):
        return JSONResponse(status_code=500, content={"detail": "Server Error"})

    @app.exception_handler(UserAlreadyExit)
    async def service_handler(request, exc):
        return JSONResponse(status_code=409, content={"detail": "Email already exit"})