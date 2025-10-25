#!/usr/bin/python3
"""Tests for create command with params (FileStorage only)."""
import io
import sys
import unittest
from models import storage
from console import HBNBCommand
try:
    from models.engine.file_storage import FileStorage
except Exception:
    FileStorage = None


@unittest.skipIf(not FileStorage or not isinstance(storage, FileStorage),
                 "Only for FileStorage")
class TestCreateParams(unittest.TestCase):
    """Test create command handling of parameters."""

    def setUp(self):
        # ensure clean storage
        for k in list(storage.all().keys()):
            del storage.all()[k]

    def tearDown(self):
        try:
            import os
            os.remove('file.json')
        except Exception:
            pass

    def test_create_place_with_params(self):
        cons = HBNBCommand()
        captured = io.StringIO()
        sys_stdout = sys.stdout
        try:
            sys.stdout = captured
            cons.onecmd('create Place name="My_little_house" number_rooms=4 price_by_night=100.5')
        finally:
            sys.stdout = sys_stdout
        out = captured.getvalue().strip()
        # printed id
        self.assertTrue(out)
        obj_key = 'Place.' + out
        self.assertIn(obj_key, storage.all())
        obj = storage.all()[obj_key]
        self.assertEqual(obj.name, 'My little house')
        self.assertEqual(int(obj.number_rooms), 4)
        # price_by_night may be float or int depending on parsing
        self.assertAlmostEqual(float(obj.price_by_night), 100.5)
