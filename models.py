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
        return "<Compositiondt>"


class CompositionConfig:
    def __init__(
        self, total: int, layers: list[Layer], fixed_compositions: list[Composition]
    ):
        self.total = total
        self.layers = layers
        self.fixed_compositions = fixed_compositions

    def __repr__(self) -> str:
        return "<CompositionConfi>"
