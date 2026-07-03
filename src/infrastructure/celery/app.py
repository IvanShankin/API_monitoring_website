from celery import Celery


celery_app = Celery("monitoring")


celery_app.autodiscover_tasks(
    ["src.models.monitoring"]
)

celery_app.conf.beat_schedule = {
    "schedule-websites": {
        "task": "src.models.monitoring.tasks.schedule_checks",
        "schedule": 5.0,
    }
}

def configure_celery_app(
    broker_url: str,
    result_backend: str,
) -> Celery:
    celery_app.conf.update(
        broker_url=broker_url,
        result_backend=result_backend,
    )

    # раз в 5 секунд будет вызвана функция schedule_checks
    celery_app.conf.beat_schedule = {
        "schedule-websites": {
            "task": "src.models.monitoring.tasks.schedule_checks",
            "schedule": 5.0,
        }
    }
    return celery_app


