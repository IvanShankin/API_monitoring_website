from datetime import datetime, timedelta
from typing import List

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from helpers.functions import random_string
from models.websites.fixtures.models_dto import CreateWebsiteFixtureDTO
from src.models.website_check.models import WebsiteChecks, ErrorType
from src.models.websites.models_dto import WebsitesDTO

WORKING_URLS = [
    "https://google.com",
    "https://facebook.com",
    "https://cloudflare.com",
    "https://akamai.com",
    "https://fastly.com",
    "https://wikipedia.org",
    "https://github.com",
]


@pytest.mark.asyncio
async def test_schedule_checks_async(
    monkeypatch,
    website_monitor_service_fixture,
    create_user_fixture,
    create_website_fixture,
    session_db: AsyncSession,
):
    user, accesses_token = await create_user_fixture()

    websites_bads: List[WebsitesDTO] = []
    for i in range(350):
        websites_bads.append(
            await create_website_fixture(
                CreateWebsiteFixtureDTO(
                    user_id=user.id,
                    url=f"https://{random_string(length=30)}.com",
                    is_active=True,
                    timeout_in_seconds=1,
                    created_at=datetime.now() - timedelta(days=1),
                )
            )
        )

    websites_goods: List[WebsitesDTO] = []
    for url in WORKING_URLS:
        websites_goods.append(
            await create_website_fixture(
                CreateWebsiteFixtureDTO(
                    user_id=user.id,
                    url=url,
                    is_active=True,
                    timeout_in_seconds=1,
                    created_at=datetime.now() - timedelta(days=1),
                )
            )
        )

    await website_monitor_service_fixture.monitor(websites_bads)
    await website_monitor_service_fixture.monitor(websites_goods)

    result_db = await session_db.execute(
        select(WebsiteChecks)
        .where(
            WebsiteChecks.website_id.in_(
                [website.id for website in websites_bads]
            )
        )
    )
    website_bad_db: List[WebsiteChecks] = result_db.scalars().all()

    # сайты не должны пройти проверку
    assert not any([website.is_available for website in website_bad_db])
    for website in website_bad_db:
        assert website.error_type == ErrorType.CONNECTION_ERROR


    result_db = await session_db.execute(
        select(WebsiteChecks)
        .where(
            WebsiteChecks.website_id.in_(
                [website.id for website in websites_goods]
            )
        )
    )
    website_goods_db: List[WebsiteChecks] = result_db.scalars().all()

    # сайты должны пройти проверку
    assert any([website.is_available for website in website_goods_db])

