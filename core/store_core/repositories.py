import datetime
from datetime import timedelta
from store_core.factories import Dog, Order
from decimal import Decimal
from sqlalchemy import or_, and_, desc
from sqlalchemy.sql import tuple_
from sqlalchemy.sql import func
from sqlalchemy.sql import select
from sqlalchemy.sql import extract


class DefaultRepository(object):
    model = None
    model_id_field = None

    def __init__(self, model=None, model_id_field=None):
        if model:
            self.model = model
        if model_id_field:
            self.model_id_field = model_id_field

    def get_or_create(self, gateway, defaults=None, **kwargs):
        with gateway.session_scope() as session:
            obj, created = gateway.get_or_create(
                session, self.model.alchemy_model, defaults=defaults, **kwargs
            )
            obj = self.model.from_alchemy(obj) if obj else None
        return obj, created

    def get_by_id(self, gateway, ident):
        with gateway.session_scope() as session:
            obj = gateway.get_by_id(session, self.model.alchemy_model, ident=ident)
            obj = self.model.from_alchemy(obj) if obj else None
        return obj

    def get(self, gateway, **kwargs):
        with gateway.session_scope() as session:
            obj = gateway.get(session, self.model.alchemy_model, **kwargs)
            obj = self.model.from_alchemy(obj) if obj else None
        return obj

    def filter(self, gateway, **kwargs):
        with gateway.session_scope() as session:
            objs = gateway.filter(session, self.model.alchemy_model, **kwargs)
            objs = list(map(lambda obj: self.model.from_alchemy(obj), objs))
        return objs

    def get_all(self, gateway):
        with gateway.session_scope() as session:
            objs = gateway.get_all(session, self.model.alchemy_model)
            objs = list(map(lambda obj: self.model.from_alchemy(obj), objs))
        return objs

    def update(self, gateway, obj, **kwargs):
        with gateway.session_scope() as session:
            obj = gateway.update(
                session,
                self.model.alchemy_model,
                getattr(obj, self.model_id_field),
                **kwargs
            )
            obj = self.model.from_alchemy(obj) if obj else None
        return obj

    def update_all(self, gateway, criterion, **kwargs):
        with gateway.session_scope() as session:
            ids = gateway.update_all(
                session, self.model.alchemy_model, criterion, **kwargs
            )
            # objs = list(map(lambda obj: self.model.from_alchemy(obj), objs))
        return ids

    def create(self, gateway, **kwargs):
        with gateway.session_scope() as session:
            obj = gateway.create(session, self.model.alchemy_model, **kwargs)
            obj = self.model.from_alchemy(obj)
        return obj

    def clear_all_data(self, gateway):
        with gateway.session_scope() as session:
            return gateway.clear_all_data(session, self.model.alchemy_model)


class DogRepository(DefaultRepository):
    model = Dog
    model_id_field = "dog_id"

    def create(self, gateway, **kwargs):
        with gateway.session_scope() as session:
            dog = gateway.create(session, self.model.alchemy_model, **kwargs)
            # session.refresh(usr)
            obj = self.model.from_alchemy(dog)
        return obj

    def get_or_create(self, gateway, defaults=None, **kwargs):
        raise NotImplementedError("TODO: to be implemented")

    def get_all_dogs(self, gateway):
        return self.get_all(gateway)


class OrderRepository(DefaultRepository):
    model = Order
    model_id_field = "id"

    def get_by_id(self, gateway, ident):
        with gateway.session_scope() as session:
            obj = gateway.get_by_id(session, self.model.alchemy_model, ident=ident)
            dogs = obj.dogs
            obj.dogs = []
            obj = self.model.from_alchemy(obj) if obj else None
            obj.dogs = [Dog.from_alchemy(dog) for dog in dogs]
        return obj

    def create(self, gateway, **kwargs):
        with gateway.session_scope() as session:
            dogs = kwargs.pop("dogs", None)
            order = gateway.create(session, self.model.alchemy_model, **kwargs)
            for dog in dogs:
                dog["order_id"] = order.id
                dog["available"] = False
                gateway.update(session, Dog.alchemy_model, dog["dog_id"], **dog)
                dog["order_id"] = order.id
            session.refresh(order)
            obj = self.model.from_alchemy(order)
            obj.dogs = dogs
            return obj
