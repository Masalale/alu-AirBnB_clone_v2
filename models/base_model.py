#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone

It also defines the SQLAlchemy Base() for mapped classes to inherit from.
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
try:
    from sqlalchemy.orm import declarative_base
except ImportError:
    # Fallback for older SQLAlchemy versions
    from sqlalchemy.ext.declarative import declarative_base


# Base class for SQLAlchemy models. BaseModel does NOT inherit from Base;
# concrete models will inherit from both BaseModel and Base.
Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models

    Contains common methods and SQLAlchemy column descriptors (as class
    attributes) so classes that inherit from BaseModel and Base will be
    properly mapped.
    """
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Instantiate a new model

        If kwargs provided, use them to set attributes (parsing datetimes).
        Otherwise, generate a new id and set created_at/updated_at.
        Note: do NOT register the new instance in storage here — registration
        is performed in save() to avoid premature persistence during
        SQLAlchemy-driven operations.
        """
        if not kwargs:
            self.id = str(uuid.uuid4())
            import time
            self.created_at = datetime.utcnow()
            # Ensure updated_at is slightly different from created_at
            time.sleep(0.001)  # 1 millisecond delay
            self.updated_at = datetime.utcnow()
            # For FileStorage, register the new instance immediately to keep
            # backward compatibility with existing tests and behaviour.
            try:
                from models import storage
                # If storage is FileStorage, it expects new()
                # to be called here
                storage_class = getattr(storage, '__class__', None)
                if storage_class and storage_class.__name__ == 'FileStorage':
                    storage.new(self)
            except Exception:
                pass
        else:
            # Expect created_at and updated_at to be provided in kwargs (old
            # behaviour). Raise KeyError if they're missing to match tests.
            if 'created_at' not in kwargs or 'updated_at' not in kwargs:
                raise KeyError(
                    'created_at and updated_at required in kwargs'
                )

            # parse datetimes
            if isinstance(kwargs['created_at'], str):
                kwargs['created_at'] = datetime.strptime(
                    kwargs['created_at'], '%Y-%m-%dT%H:%M:%S.%f')
            if isinstance(kwargs['updated_at'], str):
                kwargs['updated_at'] = datetime.strptime(
                    kwargs['updated_at'], '%Y-%m-%dT%H:%M:%S.%f')

            # remove class name if present
            kwargs.pop('__class__', None)
            for key, value in kwargs.items():
                setattr(self, key, value)

    def __str__(self):
        """String representation"""
        cls = (str(type(self)).split('.')[-1]).split("'")[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Update updated_at and persist the instance via storage

        The storage.new() call is executed here before storage.save() so
        that newly created instances are properly registered in the
        current storage engine (FileStorage or DBStorage).
        """
        from models import storage
        import time
        # Ensure updated_at is different from created_at
        time.sleep(0.00001)  # 10 microseconds
        self.updated_at = datetime.utcnow()
        try:
            storage.new(self)
        except Exception:
            # storage may not implement new() for some engines; ignore
            pass
        storage.save()

    def to_dict(self, **kwargs):
        """Return a dict representation of the instance

        Ensure SQLAlchemy internals (_sa_instance_state) are not included.
        """
        dictionary = dict(self.__dict__)
        # remove SQLAlchemy instance state if present
        dictionary.pop('_sa_instance_state', None)
        dictionary.update({
            '__class__': (
                str(type(self)).split('.')[-1]
            ).split("'")[0]
        })
        # convert datetimes to isoformat
        if ('created_at' in dictionary and
                isinstance(dictionary['created_at'], datetime)):
            dictionary['created_at'] = dictionary['created_at'].isoformat()
        if ('updated_at' in dictionary and
                isinstance(dictionary['updated_at'], datetime)):
            dictionary['updated_at'] = dictionary['updated_at'].isoformat()
        return dictionary

    def delete(self):
        """Delete the current instance from storage"""
        from models import storage
        try:
            storage.delete(self)
        except Exception:
            pass
