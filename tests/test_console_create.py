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
            cons.onecmd(
                'create Place name="My_little_house" number_rooms=4 '
                'price_by_night=100.5'
            )
        finally:
            sys.stdout = sys_stdout
        out = captured.getvalue().strip()
        # printed id
        self.assertTrue(out)
        obj_key = 'Place.' + out
        self.assertIn(obj_key, storage.all())
        obj = storage.all()[obj_key]
            self.assertEqual(obj.name, "My_little_house")
        self.assertEqual(int(obj.number_rooms), 4)
        # price_by_night may be float or int depending on parsing
        self.assertAlmostEqual(float(obj.price_by_night), 100.5)

    def test_create_state_regular(self):
        """Test create State is present (regular case) - FileStorage"""
        cons = HBNBCommand()
        captured = io.StringIO()
        sys_stdout = sys.stdout
        try:
            sys.stdout = captured
            cons.onecmd('create State')
        finally:
            sys.stdout = sys_stdout
        out = captured.getvalue().strip()
        self.assertTrue(out)
        obj_key = 'State.' + out
        self.assertIn(obj_key, storage.all())

    def test_create_state_with_name(self):
        """Test create State name="California" is present (new feature) - FileStorage"""
        cons = HBNBCommand()
        captured = io.StringIO()
        sys_stdout = sys.stdout
        try:
            sys.stdout = captured
            cons.onecmd(
                'create State name="California"'
            )
        finally:
            sys.stdout = sys_stdout
        out = captured.getvalue().strip()
        self.assertTrue(out)
        obj_key = 'State.' + out
        self.assertIn(obj_key, storage.all())
        obj = storage.all()[obj_key]
        self.assertEqual(obj.name, "California")

    def test_create_state_and_city(self):
        """
        Test create State name="California" + create City state_id="<new state ID>" name="Fremont" is present
        (more than one parameter) - FileStorage
        """
        cons = HBNBCommand()
        captured = io.StringIO()
        sys_stdout = sys.stdout
        try:
            sys.stdout = captured
            cons.onecmd(
                'create State name="California"'
            )
            state_id = captured.getvalue().strip()
            cons.onecmd(
                f'create City state_id="{state_id}" name="Fremont"'
            )
        finally:
            sys.stdout = sys_stdout
        out = captured.getvalue().strip()
        # out should be the city id
        city_id = [line for line in out.split('\n') if line][-1]
        self.assertTrue(city_id)
        state_key = 'State.' + state_id
        city_key = 'City.' + city_id
        self.assertIn(state_key, storage.all())
        self.assertIn(city_key, storage.all())
        state_obj = storage.all()[state_key]
        city_obj = storage.all()[city_key]
        self.assertEqual(state_obj.name, 'California')
        self.assertEqual(city_obj.state_id, state_id)
        self.assertEqual(city_obj.name, 'Fremont')

    def test_create_state_and_city_with_underscore(self):
        """Test create State name="California" + create City state_id="<new state ID>" name="San_Francisco" is present (space translated to _) - FileStorage"""
        cons = HBNBCommand()
        captured = io.StringIO()
        sys_stdout = sys.stdout
        try:
            sys.stdout = captured
            cons.onecmd(
                'create State name="California"'
            )
            state_id = captured.getvalue().strip()
            cons.onecmd(
                f'create City state_id="{state_id}" name="San_Francisco"'
            )
        finally:
            sys.stdout = sys_stdout
        out = captured.getvalue().strip()
        city_id = [line for line in out.split('\n') if line][-1]
        self.assertTrue(city_id)
        state_key = 'State.' + state_id
        city_key = 'City.' + city_id
        self.assertIn(state_key, storage.all())
        self.assertIn(city_key, storage.all())
        state_obj = storage.all()[state_key]
        city_obj = storage.all()[city_key]
        self.assertEqual(state_obj.name, 'California')
        self.assertEqual(city_obj.state_id, state_id)
        self.assertEqual(city_obj.name, 'San Francisco')

    def test_complex_creation(self):
        """Test create State name="California" + create City state_id="<new state ID>" name="San_Francisco_is_super_cool" + create User email="my@me.com" password="pwd" first_name="FN" last_name="LN" + create Place city_id="<new city ID>" user_id="<new user ID>" name="My_house" description="no_description_yet" number_rooms=4 number_bathrooms=1 max_guest=3 price_by_night=100 latitude=120.12 longitude=101.4 + show Place <new place ID> is present (integer + float) - FileStorage"""
        cons = HBNBCommand()
        captured = io.StringIO()
        sys_stdout = sys.stdout
        try:
            sys.stdout = captured
            cons.onecmd('create State name="California"')
            state_id = captured.getvalue().strip()
            cons.onecmd(
                f'create City state_id="{state_id}" '
                'name="San_Francisco_is_super_cool"'
            )
            city_id = [line for line in captured.getvalue().strip().split('\n') if line][-1]
            cons.onecmd(
                'create User email="my@me.com" password="pwd" '
                'first_name="FN" last_name="LN"'
            )
            user_id = [line for line in captured.getvalue().strip().split('\n') if line][-1]
            cons.onecmd(
                f'create Place city_id="{city_id}" user_id="{user_id}" '
                'name="My_house" description="no_description_yet" '
                'number_rooms=4 number_bathrooms=1 max_guest=3 '
                'price_by_night=100 latitude=120.12 longitude=101.4'
            )
            place_id = [line for line in captured.getvalue().strip().split('\n') if line][-1]
            cons.onecmd(f'show Place {place_id}')
        finally:
            sys.stdout = sys_stdout
        out = captured.getvalue().strip()
        # Verify all objects exist
        state_key = 'State.' + state_id
        city_key = 'City.' + city_id
        user_key = 'User.' + user_id
        place_key = 'Place.' + place_id
        self.assertIn(state_key, storage.all())
        self.assertIn(city_key, storage.all())
        self.assertIn(user_key, storage.all())
        self.assertIn(place_key, storage.all())
        # Verify attributes
        state_obj = storage.all()[state_key]
        city_obj = storage.all()[city_key]
        user_obj = storage.all()[user_key]
        place_obj = storage.all()[place_key]
        self.assertEqual(state_obj.name, 'California')
        self.assertEqual(city_obj.state_id, state_id)
        self.assertEqual(city_obj.name, 'San_Francisco_is_super_cool')
        self.assertEqual(user_obj.email, 'my@me.com')
        self.assertEqual(user_obj.password, 'pwd')
        self.assertEqual(user_obj.first_name, 'FN')
        self.assertEqual(user_obj.last_name, 'LN')
        self.assertEqual(place_obj.city_id, city_id)
        self.assertEqual(place_obj.user_id, user_id)
        self.assertEqual(place_obj.name, 'My house')
        self.assertEqual(place_obj.description, 'no description yet')
        self.assertEqual(int(place_obj.number_rooms), 4)
        self.assertEqual(int(place_obj.number_bathrooms), 1)
        self.assertEqual(int(place_obj.max_guest), 3)
        self.assertEqual(int(place_obj.price_by_night), 100)
        self.assertAlmostEqual(float(place_obj.latitude), 120.12)
        self.assertAlmostEqual(float(place_obj.longitude), 101.4)
        # Verify show output contains the place
        self.assertIn('Place', out)
        self.assertIn(place_id, out)
