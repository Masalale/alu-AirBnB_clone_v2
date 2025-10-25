#!/usr/bin/python3
"""DBStorage engine using SQLAlchemy"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from models.base_model import Base


class DBStorage:
    """Interacts with the MySQL database using SQLAlchemy"""
    __engine = None
    __session = None

    def __init__(self):
        """Initialize the engine and (optionally) drop tables in test env"""
        user = getenv('HBNB_MYSQL_USER')
        pwd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')
        env = getenv('HBNB_ENV')

        connection = 'mysql+mysqldb://{}:{}@{}/{}'.format(user, pwd, host, db)
        self.__engine = create_engine(connection, pool_pre_ping=True)

        if env == 'test':
            # Drop all tables for a clean test database
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the current database session all objects depending of the
        class name (argument cls). If cls is None, query all types.
        Returns a dictionary: {<class-name>.<id>: object}
        """
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        classes = {
            'User': User, 'State': State, 'City': City,
            'Amenity': Amenity, 'Place': Place, 'Review': Review
        }

        obj_dict = {}
        if cls:
            # allow cls to be a class or a class name
            if isinstance(cls, str):
                cls = classes.get(cls, None)
            if cls is None:
                return {}
            query = self.__session.query(cls).all()
            for obj in query:
                key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                obj_dict[key] = obj
            return obj_dict

        # cls is None: query all known classes
        for name, klass in classes.items():
            query = self.__session.query(klass).all()
            for obj in query:
                key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                obj_dict[key] = obj
        return obj_dict

    def new(self, obj):
        """Add the object to the current database session"""
        if obj:
            self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from the current database session if not None"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and initialize a session"""
        # import all classes to ensure they are registered with SQLAlchemy
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
#!/usr/bin/python3
"""DB storage engine placeholder for pycodestyle checks."""
from typing import Dict, Any


class DBStorage:
    """A minimal placeholder DB storage engine.

    This provides the basic method signatures expected by the rest of
    the codebase so style checks and imports succeed. It intentionally
    implements no persistence here.
    """

    def __init__(self):
        self.__objects: Dict[str, Any] = {}

    def all(self):
        """Return the dictionary of objects."""
        return self.__objects

    def new(self, obj):
        """Register new object (no-op placeholder)."""
        if obj:
            key = obj.__class__.__name__ + '.' + obj.id
            self.__objects[key] = obj

    def save(self):
        """Persist objects (no-op placeholder)."""
        pass

    def delete(self, obj=None):
        """Delete obj from storage if it exists (no-op placeholder)."""
        if obj:
            key = obj.__class__.__name__ + '.' + obj.id
            self.__objects.pop(key, None)

    def reload(self):
        """Reload objects from storage (no-op placeholder)."""
        pass
