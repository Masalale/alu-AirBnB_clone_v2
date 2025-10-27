#!/usr/bin/python3
""" State Module for HBNB project """
from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """

    __tablename__ = 'states'

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        name = Column(String(128), nullable=False)
        # DB relationship: State has many cities; deleting a State cascades
        cities = relationship(
            'City', backref='state', cascade='all, delete, delete-orphan'
        )
    else:
        name = ""

        @property
        def cities(self):
            """Return list of City instances with state_id == self.id (FileStorage)"""
            from models import storage
            from models.city import City
            return [
                c for c in storage.all().values()
                if isinstance(c, City) and c.state_id == self.id
            ]
