#!/usr/bin/python3
"""Unit tests for DB storage behavior (run only when HBNB_TYPE_STORAGE=db)."""
import unittest
from os import getenv

db_env = getenv('HBNB_TYPE_STORAGE') == 'db'


@unittest.skipUnless(db_env, "DB storage tests only")
class TestDBStorage(unittest.TestCase):
    """Tests for the minimal DBStorage placeholder or real DBStorage."""

    def setUp(self):
        from models import storage
        self.storage = storage

    def test_storage_class(self):
        """Storage should be an instance of DBStorage when DB enabled."""
        from models.engine.db_storage import DBStorage
        self.assertEqual(type(self.storage), DBStorage)

    def test_new_and_all(self):
        """New object should be registered in storage.all()."""
        from models.base_model import BaseModel
        bm = BaseModel()
        # Ensure new() registers the object
        self.storage.new(bm)
        key = bm.__class__.__name__ + '.' + bm.id
        self.assertIn(key, self.storage.all())

    def test_delete(self):
        """Delete should remove object from storage if present."""
        from models.base_model import BaseModel
        bm = BaseModel()
        self.storage.new(bm)
        key = bm.__class__.__name__ + '.' + bm.id
        self.storage.delete(bm)
        self.assertNotIn(key, self.storage.all())

    def test_save_reload_noop(self):
        """Placeholder save/reload should at least not raise."""
        # These are no-op for placeholder but must not raise
        self.storage.save()
        self.storage.reload()
