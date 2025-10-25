#!/usr/bin/python3
"""Instantiate the appropriate storage engine based on env vars."""
from os import getenv

# Default to file storage
STORAGE_TYPE = getenv('HBNB_TYPE_STORAGE')

if STORAGE_TYPE == 'db':
	from models.engine.db_storage import DBStorage

	storage = DBStorage()
else:
	from models.engine.file_storage import FileStorage

	storage = FileStorage()

try:
	storage.reload()
except Exception:
	# reload may be a no-op or not implemented for a storage engine
	pass
