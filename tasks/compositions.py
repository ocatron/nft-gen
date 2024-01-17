import copy
from celery import shared_task

from models import ComposedLayer, Composition, CompositionConfig
from schemas import CompositionConfigSchema


@shared_task
def generate(data):
    comp_config: CompositionConfig = CompositionConfigSchema().load(data)  # type: ignore
    comps: list[Composition] = []
    visited: set[str] = set()
    total: int = 0

    for comp in comp_config.fixed_compositions:
        comps.append(comp)
        visited.add(comp.as_string())

    while total < comp_config.total:
        local_layers = copy.deepcopy(comp_config.layers)
        composed_layers: list[ComposedLayer] = []

        for layer in local_layers:
            pass
