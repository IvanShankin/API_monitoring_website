from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.config import create_config


def _include_routers(app: FastAPI) -> FastAPI:
    pass

def init_fastapi_app() -> FastAPI:
    app = FastAPI(
        title="Auth Service",
        lifespan=lifespan
    )

    app.state.config = create_config()

    _include_routers(app)

    return app


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.config = create_config()

    try:
        yield
    finally:
        pass