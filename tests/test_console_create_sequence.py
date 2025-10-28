#!/usr/bin/python3
"""Sequence tests for create command with params (FileStorage only)."""
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
class TestCreateSequence(unittest.TestCase):
    """Run a sequence of creates and validate attributes and references."""

    def setUp(self):
        # clear storage
        for k in list(storage.all().keys()):
            del storage.all()[k]

    def tearDown(self):
        try:
            import os
            os.remove('file.json')
        except Exception:
            pass

    def _run_cmd(self, cmd):
        cons = HBNBCommand()
        captured = io.StringIO()
        sys_stdout = sys.stdout
        try:
            sys.stdout = captured
            cons.onecmd(cmd)
        finally:
            sys.stdout = sys_stdout
        return captured.getvalue().strip()

    def test_create_state_present(self):
        # console_0.py: create State name="California"
        sid = self._run_cmd('create State name="California"')
        self.assertTrue(sid)
        key = 'State.' + sid
        self.assertIn(key, storage.all())
        st = storage.all()[key]
        self.assertEqual(st.name, 'California')

    def test_create_city_with_state(self):
        # console_1.py: create State then City with state_id and name
        sid = self._run_cmd('create State name="California"')
        self.assertTrue(sid)
        cid = self._run_cmd(f'create City state_id="{sid}" name="Fremont"')
        self.assertTrue(cid)
        key = 'City.' + cid
        self.assertIn(key, storage.all())
        city = storage.all()[key]
        self.assertEqual(city.state_id, sid)
        self.assertEqual(city.name, 'Fremont')

    def test_create_city_underscore_space(self):
        # console_2.py: underscores in name become spaces
        sid = self._run_cmd('create State name="California"')
        self.assertTrue(sid)
        cid = self._run_cmd(
            f'create City state_id="{sid}" name="San_Francisco"'
        )
        self.assertTrue(cid)
        city = storage.all()['City.' + cid]
        self.assertEqual(city.name, 'San Francisco')

    def test_create_full_sequence_and_show_place(self):
        # console_3/4.py: create state, city, user, place
        # and verify place attributes
        sid = self._run_cmd('create State name="California"')
        cid = self._run_cmd(
            f'create City state_id="{sid}" '
            'name="San_Francisco_is_super_cool"'
        )
        uid = self._run_cmd(
            'create User email="my@me.com" password="pwd" '
            'first_name="FN" last_name="LN"'
        )
        pid = self._run_cmd(
            f'create Place city_id="{cid}" user_id="{uid}" '
            'name="My_house" description="no_description_yet" '
            'number_rooms=4 number_bathrooms=1 max_guest=3 '
            'price_by_night=100 latitude=120.12 longitude=101.4'
        )
        self.assertTrue(pid)
        place = storage.all()['Place.' + pid]
        self.assertEqual(place.name, 'My house')
        self.assertEqual(place.description, 'no description yet')
        self.assertEqual(int(place.number_rooms), 4)
        self.assertEqual(int(place.number_bathrooms), 1)
        self.assertEqual(int(place.max_guest), 3)
        # floats
        self.assertAlmostEqual(float(place.price_by_night), 100.0)
        self.assertAlmostEqual(float(place.latitude), 120.12)
        self.assertAlmostEqual(float(place.longitude), 101.4)

        # show command prints object representation
        # containing id and attributes
        cons = HBNBCommand()
        captured = io.StringIO()
        sys_stdout = sys.stdout
        try:
            sys.stdout = captured
            cons.onecmd(f'show Place {pid}')
        finally:
            sys.stdout = sys_stdout
        out = captured.getvalue()
        # must contain the place id and the name with spaces
        self.assertIn(pid, out)
        self.assertIn('My house', out)


if __name__ == '__main__':
    unittest.main()
