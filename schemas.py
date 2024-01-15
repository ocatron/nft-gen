from marshmallow import Schema, ValidationError, fields, post_load
from models import (
    Avoided,
    ComposedLayer,
    Composition,
    CompositionConfig,
    Layer,
    Trait,
)


class NonEmptyString(fields.String):
    def _deserialize(self, value, attr, data, **kwargs):
        value = super()._deserialize(value, attr, data, **kwargs)
        value = value.strip()
        if not value:
            raise ValidationError(f"{attr} cannot be empty")
        return value


class AvoidedSchema(Schema):
    layer_id = NonEmptyString(required=True)
    trait_ids = fields.List(NonEmptyString)

    @post_load
    def make_avoided(self, data, **kwargs):
        return Avoided(**data)


class TraitSchema(Schema):
    id = NonEmptyString(required=True)
    display_name = fields.Str(required=True)
    weight = fields.Float()
    avoid = fields.List(fields.Nested(AvoidedSchema))

    @post_load
    def make_trait(self, data, **kwargs):
        return Trait(**data)


class LayerSchema(Schema):
    id = NonEmptyString(required=True)
    display_name = fields.Str(required=True)
    priority = fields.Integer(required=True)
    traits = fields.List(fields.Nested(TraitSchema))

    @post_load
    def make_layer(self, data, **kwargs):
        return Layer(**data)


class ComposedLayerSchema(Schema):
    layer_id = NonEmptyString(required=True)
    trait_id = NonEmptyString(required=True)

    @post_load
    def make_composed_layer(self, data, **kwargs):
        return ComposedLayer(**data)


class CompositionSchema(Schema):
    layers = fields.List(fields.Nested(ComposedLayerSchema))

    @post_load
    def make_composition(self, data, **kwargs):
        return Composition(**data)


class CompositionConfigSchema(Schema):
    total = fields.Int()
    layers = fields.List(fields.Nested(LayerSchema))
    fixed_compositions = fields.List(fields.Nested(CompositionSchema))

    @post_load
    def make_composition_config(self, data, **kwargs):
        return CompositionConfig(**data)
