from fastapi import Request

from src.config import Config


def get_config(request: Request) -> Config:
    return request.app.state.config