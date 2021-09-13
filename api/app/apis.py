from store_core.database.gateway import DBGateway
from store_core.factories import Dog, Order
from store_core.repositories import DogRepository, OrderRepository
from datetime import datetime
from flask import jsonify, request, abort, make_response
from schematics.exceptions import ValidationError, DataError
from sqlalchemy.exc import IntegrityError

dog_repository = DogRepository()
order_repository = OrderRepository()


def create_dog():
    try:
        dog = Dog(request.json)
        dog.validate()
        obj = dog_repository.create(DBGateway, **dog.to_native())
        return jsonify(obj.to_native()), 201
    except IntegrityError as e:
        abort(make_response(jsonify(message="dog already exist"), 409))
    except (ValidationError, DataError) as e:
        abort(make_response(jsonify(e.to_primitive()), 400))


def update_dog(dog_id):
    try:
        data = request.json
        dog = Dog(data)
        dog.validate()
        if dog_id != dog.dog_id:
            abort(make_response(jsonify(message="integrity error"), 409))
        obj = dog_repository.update(DBGateway, dog, **dog.to_native())
        return jsonify(obj.to_native()), 200
    except IntegrityError as e:
        abort(make_response(jsonify(message="integrity error"), 409))
    except (ValidationError, DataError) as e:
        abort(make_response(jsonify(e.to_primitive()), 400))


def get_dog(dog_id):
    obj = dog_repository.get_by_id(DBGateway, ident=dog_id)
    if obj is None:
        abort(make_response(jsonify(message="dog does not exist"), 404))
    return jsonify(obj.to_native()), 200


def add_order():
    order = Order(request.json)
    order.validate()
    obj = order_repository.create(DBGateway, **order.to_native())
    return jsonify(obj.to_native()), 201


def get_order(order_id):
    obj = order_repository.get_by_id(DBGateway, ident=order_id)
    if obj is None:
        abort(make_response(jsonify(message="order does not exist"), 404))
    return jsonify(obj.to_native()), 200
