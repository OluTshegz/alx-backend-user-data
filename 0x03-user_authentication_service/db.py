#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Adds a new user to the database and returns the User object.

        Args:
            email (str): The email of the user.
            hashed_password (str): The hashed password of the user.

        Returns:
            User: The created User object.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Finds a user by the given keyword arguments.

        Args:
            **kwargs: Arbitrary keyword arguments to filter the users.

        Returns:
            User: The first User object that matches the filter criteria.

        Raises:
            NoResultFound: If no user is found.
            InvalidRequestError: If invalid query arguments are passed.
        """
        session = self._session
        try:
            query = session.query(User).filter_by(**kwargs)
            user = query.first()
            if user is None:
                raise NoResultFound("No user found")
            return user
        except InvalidRequestError:
            self._session.rollback()
            raise

    def update_user(self, user_id: int, **kwargs) -> None:
        """Updates a user's attributes and commits the changes to the db.

        Args:
            user_id (int): The ID of the user to update.
            kwargs: Arbitrary keyword arguments representing the
            attributes to update.

        Raises:
            ValueError: If any of the arguments do not correspond to
            valid user attributes.
            NoResultFound: If no user with the given user_id is found.

        Returns:
            None.
        """
        try:
            user = self.find_user_by(id=user_id)
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
                else:
                    raise ValueError("Invalid attribute: {}".format(key))
            self._session.commit()
        except NoResultFound:
            raise
        except InvalidRequestError:
            self._session.rollback()
            raise ValueError("Invalid update request")
