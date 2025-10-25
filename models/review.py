#!/usr/bin/python3
""" Review module for the HBNB project """
from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Text, ForeignKey


class Review(BaseModel, Base):
    __tablename__ = 'reviews'

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        text = Column(Text, nullable=True)
    else:
        place_id = ""
        user_id = ""
        text = ""
