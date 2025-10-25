#!/usr/bin/python3
""" Review module for the HBNB project """
from os import getenv
from models.base_model import BaseModel, Base


class Review(BaseModel, Base):
    __tablename__ = 'reviews'

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        pass
    else:
        place_id = ""
        user_id = ""
        text = ""
