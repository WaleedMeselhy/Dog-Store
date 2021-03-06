# coding=utf-8

from sqlalchemy import Column, Integer, ForeignKey, String, Boolean
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import relationship


class Base(object):
    """
    a base class for all of our models, this defines:
    1) the table name to be the lower-cased version of the class name
    2) generic __init__ and __repr__ functions
    """

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def __init__(self, **kwargs):
        for key in kwargs:
            if key not in self.attr_accessor:
                raise Exception(f"Invalid Prop: {key}")
            setattr(self, key, kwargs[key])

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}

    def __repr__(self):
        def filter_properties(obj):
            # this function decides which properties should be exposed through repr
            properties = obj.__dict__.keys()
            for prop in properties:
                if prop[0] != "_" and not callable(prop):
                    yield (prop, str(getattr(obj, prop)))
            return

        prop_tuples = filter_properties(self)
        prop_string_tuples = (": ".join(prop) for prop in prop_tuples)
        prop_output_string = " | ".join(prop_string_tuples)
        cls_name = self.__module__ + "." + self.__class__.__name__

        return "<%s('%s')>" % (cls_name, prop_output_string)


Base = declarative_base(cls=Base)


class Dog(Base):
    __tablename__ = "dog"
    dog_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    breed = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    available = Column(Boolean)
    order_id = Column(Integer, ForeignKey("order.id"))


class Order(Base):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String, nullable=False)
    dogs = relationship("Dog", lazy="joined")
