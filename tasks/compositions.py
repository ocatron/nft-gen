from celery import shared_task

from models import CompositionConfig
from schemas import CompositionConfigSchema


@shared_task
def generate(data):
    comp_config: CompositionConfig = CompositionConfigSchema().load(data)  # type: ignore
