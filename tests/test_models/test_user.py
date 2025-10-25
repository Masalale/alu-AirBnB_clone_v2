#!/usr/bin/python3
""" """
import os
import unittest
from tests.test_models.test_base_model import test_basemodel
from models.user import User
from models import storage
try:
    from models.engine.file_storage import FileStorage
except Exception:
    FileStorage = None


@unittest.skipIf(not FileStorage or not isinstance(storage, FileStorage),
                 "Skipping file-storage User tests when storage is not FileStorage")
class test_User(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "User"
        self.value = User

    def test_first_name(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.first_name), str)

    def test_last_name(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.last_name), str)

    def test_email(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.email), str)

    def test_password(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.password), str)
