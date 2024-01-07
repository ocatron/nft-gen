import os
from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is None:
        app.config.from_prefixed_env()
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/hello")
    def hello():
        return "Hello world!"

    return app
