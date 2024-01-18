from flask import request
from celery.result import AsyncResult

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

    result = compositions.generate.delay(data)

    response_data = dict(status="queued", result=f"{request.host_url}compositions/result/{result.id}")
    return response_data, 202


@compositions_bp.route("/status/<id>", methods=["GET"])
def status():
    return {"status": "queued"}, 200


@compositions_bp.route("/result/<id>", methods=["GET"])
def get_compositions(id: str):
    result = AsyncResult(id)
    if not result.ready():
        return dict(status="pending"), 200
    if result.failed():
        return dict(status="failed"), 200
    if result.successful():
        return dict(status="done", result=result.result), 200
    return {"status": "unknown"}, 200
