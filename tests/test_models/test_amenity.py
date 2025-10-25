#!/usr/bin/python3
""" """
import os
import unittest
from tests.test_models.test_base_model import test_basemodel
from models.amenity import Amenity
from models import storage
try:
    from models.engine.file_storage import FileStorage
except Exception:
    FileStorage = None


@unittest.skipIf(not FileStorage or not isinstance(storage, FileStorage),
                 "Skipping file-storage Amenity tests when storage is not FileStorage")
class test_Amenity(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "Amenity"
        self.value = Amenity

    def test_name2(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.name), str)
