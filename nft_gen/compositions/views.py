from . import compositions_bp


@compositions_bp.route("/generate", methods=["POST"])
def generate():
    return {"status": "queued"}, 202


@compositions_bp.route("/status/<id>", methods=["GET"])
def status():
    return {"status": "queued"}, 200


@compositions_bp.route("<id>", methods=["GET"])
def get_compositions():
    return {"status": "done"}, 200
