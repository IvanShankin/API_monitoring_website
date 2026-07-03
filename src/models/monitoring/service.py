import asyncio
import time

import httpx
from httpx import (
    AsyncClient,
    ConnectError,
    ConnectTimeout,
    ReadTimeout,
    WriteTimeout,
    PoolTimeout,
    HTTPStatusError,
    UnsupportedProtocol,
    DecodingError,
    RemoteProtocolError,
)
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.website_check.models import ErrorType
from src.models.website_check.models_dto import CreateWebsiteChecksDTO
from src.models.website_check.repository import WebsiteCheckRepository
from src.models.websites.models_dto import WebsitesDTO


class WebsiteMonitorService:

    def __init__(
        self,
        website_check_repo: WebsiteCheckRepository,
        session_db: AsyncSession,
    ):
        self.semaphore = asyncio.Semaphore(50)
        self.website_check_repo = website_check_repo
        self.session_db = session_db

    async def monitor(
        self,
        websites: list[WebsitesDTO]
    ):
        async with httpx.AsyncClient() as client:

            tasks = [
                self.fetch_site(
                    client,
                    website
                )
                for website in websites
            ]

            results = await asyncio.gather(
                *tasks,
                return_exceptions=True
            )

            await self.website_check_repo.bulk_add(results)
            await self.session_db.commit()


    async def fetch_site(
        self,
        client: AsyncClient,
        website: WebsitesDTO,
    ) -> CreateWebsiteChecksDTO:
        async with self.semaphore:
            try:
                start = time.monotonic()

                response = await client.get(
                    website.url,
                    timeout=float(website.timeout_in_seconds)
                )

                response.raise_for_status()

                return CreateWebsiteChecksDTO(
                    website_id=website.id,
                    http_status_code=response.status_code,
                    response_time_ms=int((time.monotonic() - start) * 1000), # перевод в миллисекунды
                    is_available=200 <= response.status_code < 400,
                )

            except ConnectError as e:
                error_type = ErrorType.CONNECTION_ERROR
                error_msg = f"Не удалось подключиться: {str(e)}"

            except ConnectTimeout as e:
                error_type = ErrorType.CONNECTION_TIMEOUT
                error_msg = f"Таймаут подключения: {str(e)}"

            except ReadTimeout as e:
                error_type = ErrorType.READ_TIMEOUT
                error_msg = f"Таймаут ожидания ответа: {str(e)}"

            except WriteTimeout as e:
                error_type = ErrorType.WRITE_TIMEOUT
                error_msg = f"Таймаут отправки запроса: {str(e)}"

            except PoolTimeout as e:
                error_type = ErrorType.POOL_TIMEOUT
                error_msg = f"Таймаут ожидания соединения из пула: {str(e)}"

            except UnsupportedProtocol as e:
                error_type = ErrorType.INVALID_URL
                error_msg = f"Неверный протокол URL: {str(e)}"

            except HTTPStatusError as e:
                # Возникает только если вызвать response.raise_for_status()
                error_type = ErrorType.HTTP_ERROR
                error_msg = f"HTTP ошибка: {e.response.status_code}"

            except DecodingError as e:
                error_type = ErrorType.DECODING_ERROR
                error_msg = f"Ошибка декодирования: {str(e)}"

            except RemoteProtocolError as e:
                error_type = ErrorType.PROTOCOL_ERROR
                error_msg = f"Ошибка протокола: {str(e)}"

            except Exception as e:
                error_type = ErrorType.OTHER_ERROR
                error_msg = str(e)

            response_time = int((time.monotonic() - start) * 1000)

            return CreateWebsiteChecksDTO(
                website_id=website.id,
                http_status_code=None,
                response_time_ms=response_time,
                is_available=False,
                error_type=error_type,
                error_message=error_msg,
            )
