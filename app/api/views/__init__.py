from flask import Blueprint

api: Blueprint = Blueprint(
    name="tracking-delivery", import_name=__name__, url_prefix="/api"
)

from .delivery.v1.delivery_view import *  # noqa isort:skip
