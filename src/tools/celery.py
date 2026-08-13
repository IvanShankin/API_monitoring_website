from src.core.config import create_config
from src.infrastructure.celery.app import configure_celery_app, celery_app

config = create_config()

configure_celery_app(
    broker_url=config.env.rabbitmq_url,
    result_backend=config.env.redis_url,
)