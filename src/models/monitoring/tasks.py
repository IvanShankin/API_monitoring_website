import asyncio

from src.core.container import create_container
from src.infrastructure.celery.app import celery_app
from src.models.monitoring.service import WebsiteMonitorService
from src.models.websites.models_dto import WebsitesDTO


async def monitor_batch_async(
    websites: list[WebsitesDTO]
):
    container = create_container()

    async with container.async_session_factory() as session:
        service = WebsiteMonitorService(
            website_check_repo=container.get_website_check_repository(session),
            website_repo=container.get_website_repository(session),
            session_db=session,
            logger=container.logger,
        )

        await service.monitor(websites)


@celery_app.task
def monitor_batch(websites: list[dict]):
    dto_list = [
        WebsitesDTO.model_validate(item)
        for item in websites
    ]

    asyncio.run(
        monitor_batch_async(dto_list)
    )


async def schedule_checks_async():
    container = create_container()

    async with container.async_session_factory() as session:
        website_service = container.get_website_service(
            session=session
        )

        websites = await website_service.get_websites_for_tests()

        if not websites:
            return

        batches = [
            websites[i:i + container.config.size_batch_website]
            for i in
            range(0, len(websites), container.config.size_batch_website)
        ]

        for batch in batches:
            monitor_batch.delay(
                [
                    website.model_dump()
                    for website in batch
                ]
            )


@celery_app.task
def schedule_checks():
    asyncio.run(schedule_checks_async())
