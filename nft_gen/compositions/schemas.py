from marshmallow import Schema, fields


class Trait(Schema):
    id = fields.Str(required=True)
    display_name = fields.Str(required=True)
    weight = fields.Float()
    avoid = fields.List(
        fields.Nested(
            Schema.from_dict(
                {
                    "layer_id": fields.Str(required=True),
                    "trait_ids": fields.List(fields.Str()),
                }
            )
        )
    )


class Layer(Schema):
    id = fields.Str(required=True)
    display_name = fields.Str(required=True)
    traits = fields.List(fields.Nested(Trait))


class Composition(Schema):
    layers = fields.List(
        fields.Nested(
            Schema.from_dict(
                {
                    "layer_id": fields.Str(required=True),
                    "trait_id": fields.Str(required=True),
                }
            )
        )
    )


class CompositionConfig(Schema):
    total = fields.Int()
    layers = fields.List(fields.Nested(Layer))
    fixed_compositions = fields.List(fields.Nested(Composition))
