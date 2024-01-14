from flask import Blueprint


compositions_bp = Blueprint("compositions", __name__, url_prefix="/compositions")

from . import views
