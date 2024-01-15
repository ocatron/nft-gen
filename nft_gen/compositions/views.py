from flask import request
from marshmallow import ValidationError
from models import CompositionConfig

from schemas import CompositionConfigSchema
from tasks import compositions
from . import compositions_bp


@compositions_bp.route("/generate", methods=["POST"])
def generate():
    schema = CompositionConfigSchema()
    data = request.get_json()
    errors = schema.validate(data)

    if errors:
        return {"status": "bad request", "messages": errors}, 400

    compositions.generate.delay(data)
    return {"status": "queued"}, 202


@compositions_bp.route("/status/<id>", methods=["GET"])
def status():
    return {"status": "queued"}, 200


@compositions_bp.route("<id>", methods=["GET"])
def get_compositions():
    return {"status": "done"}, 200
