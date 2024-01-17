class Avoided:
    def __init__(self, layer_id: str, trait_ids: list[str]):
        self.layer_id = layer_id
        self.trait_ids = trait_ids

    def __repr__(self):
        return "<Avoided>"


class Trait:
    def __init__(self, id: str, display_name: str, weight: float, avoid: list[Avoided]):
        self.id = id
        self.display_name = display_name
        self.weight = weight
        self.avoid = avoid

    def __repr__(self) -> str:
        return f"<Trait (id={self.id})>"


class Layer:
    def __init__(self, id: str, display_name: str, priority: int, traits: list[Trait]):
        self.id = id
        self.display_name = display_name
        self.priority = priority
        self.traits = traits

    def __repr__(self) -> str:
        return f"<Layer (id={self.id})>"


class ComposedLayer:
    def __init__(self, layer_id: str, trait_id: str):
        self.layer_id = layer_id
        self.trait_id = trait_id

    def __repr__(self) -> str:
        return f"<ComposedLayer (layer_id={self.layer_id})>"


class Composition:
    def __init__(self, layers: list[ComposedLayer]):
        self.layers = layers

    def __repr__(self) -> str:
        prefix = "<Composition ("
        mid = ""
        suffix = ")>"
        for layer in self.layers:
            mid += f"{layer.layer_id}:{layer.trait_id};"
        return f"{prefix}{mid}{suffix}"


class CompositionConfig:
    def __init__(
        self, total: int, layers: list[Layer], fixed_compositions: list[Composition]
    ):
        self.total = total
        self.layers = layers
        self.fixed_compositions = fixed_compositions
        self.sort_fixed_comps()

    def __repr__(self) -> str:
        return "<CompositionConfig>"

    def get_layer_priority(self, layer_id: str):
        layer = next((x for x in self.layers if x.id == layer_id), None)
        if layer:
            return layer.priority
        else:
            return -1

    def sort_fixed_comps(self):
        for comp in self.fixed_compositions:
            comp.layers.sort(key=lambda layer: self.get_layer_priority(layer.layer_id))
