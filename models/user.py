#!/usr/bin/python3
"""This module defines a class User"""
from os import getenv
from models.base_model import BaseModel, Base


class User(BaseModel, Base):
    """This class defines a user by various attributes"""
    __tablename__ = 'users'

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        # Additional columns (email, password, first_name, last_name) can be
        # added as Column() definitions if needed. For now rely on
        # BaseModel columns and manage attributes dynamically.
        pass
    else:
        email = ''
        password = ''
        first_name = ''
        last_name = ''
