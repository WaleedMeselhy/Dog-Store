from flask import Blueprint
from .apis import create_dog, update_dog, get_dog, add_order, get_order

rest_api = Blueprint("rest api", __name__)
# TODO: authentication
rest_api.route("/dog/", methods=("POST",))(create_dog)
rest_api.route("/dog/<dog_id>/", methods=("PUT",))(update_dog)
rest_api.route("/dog/<dog_id>/", methods=("GET",))(get_dog)
rest_api.route("/order/", methods=("POST",))(add_order)
rest_api.route("/order/<order_id>/", methods=("GET",))(get_order)
