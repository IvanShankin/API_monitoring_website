import asyncio

import uvicorn

from src.api.app import init_fastapi_app


async def main():
    app = init_fastapi_app()
    uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True
        )

if __name__ == '__main__':
    asyncio.run(main())
