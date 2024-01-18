import random
import copy
from celery import shared_task
from models import ComposedLayer, Composition, CompositionConfig
from schemas import CompositionConfigSchema, CompositionSchema


@shared_task(bind=True)
def generate(self, data):
    comp_config: CompositionConfig = CompositionConfigSchema().load(data)  # type: ignore
    comps: list[Composition] = []
    visited: set[str] = set()
    total: int = 0
    progress: int = 0
    self.update_state(state="PROGRESS", meta={"progress": 0})

    for comp in comp_config.fixed_compositions:
        comps.append(comp)
        visited.add(comp.as_string())

    while total < comp_config.total:
        layer_configs = copy.deepcopy(comp_config.layers)
        composed_layers: list[ComposedLayer] = []

        for layer_config in layer_configs:
            trait_weights = list(map(lambda trait: trait.weight, layer_config.traits))

            if sum(trait_weights) <= 0:
                composed_layers.append(
                    ComposedLayer(layer_id=layer_config.id, trait_id="")
                )
                continue

            selected_trait = random.choices(
                population=layer_config.traits, weights=trait_weights, k=1
            )[0]

            composed_layers.append(
                ComposedLayer(layer_id=layer_config.id, trait_id=selected_trait.id)
            )

            for avoided in selected_trait.avoid:
                for temp_layer_config in layer_configs:
                    if temp_layer_config.id == avoided.layer_id:
                        if not avoided.trait_ids:
                            for trait in temp_layer_config.traits:
                                trait.weight = 0
                        else:
                            for trait in temp_layer_config.traits:
                                if any(
                                    trait_id == trait.id
                                    for trait_id in avoided.trait_ids
                                ):
                                    trait.weight = 0
                        break

        comp = comp_config.make_sorted_composition(composed_layers)
        comp_string = comp.as_string()
        if comp_string not in visited:
            comps.append(comp)
            visited.add(comp.as_string())
            total += 1
            new_progress = total * 100 // comp_config.total
            if new_progress > progress:
                self.update_state(state="PROGRESS", meta={"progress": new_progress})
                progress = new_progress

    result = dict(compositions=CompositionSchema().dump(comps, many=True))

    return result
