#!/usr/bin/env python3
"""
DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import Base, User


class DB:
    """DB class for managing database operations
    """

    def __init__(self) -> None:
        """Initialize a new DB instance with an SQLite database
        """
        # Create SQLite engine
        self._engine = create_engine("sqlite:///a.db", echo=True)
        # Drop all tables (for a fresh start)
        Base.metadata.drop_all(self._engine)
        # Create all tables as per the model
        Base.metadata.create_all(self._engine)
        # Session object is initially set to None
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object to interact with the database
        """
        if self.__session is None:
            # Bind engine to sessionmaker
            DBSession = sessionmaker(bind=self._engine)
            # Create a session instance
            self.__session = DBSession()
        return self.__session

    from typing import Optional

    def add_user(self, email: str, hashed_password: str) -> Optional[User]:
        """Add a new user to the database.

        Args:
            email (str): The email of the user.
            hashed_password (str): The hashed password of the user.

        Returns:
            Optional[User]: The User object that was created and added to
            the database, or None if email or hashed_password is empty.
        """
        if not email or not hashed_password:
            return None
        # Create a new User instance
        new_user = User(email=email, hashed_password=hashed_password)
        # Add the new user to the session
        self._session.add(new_user)
        # Commit the session to persist the user to the database
        self._session.commit()
        # Return the newly created User object
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Find a user by arbitrary keyword arguments.

        Args:
            **kwargs: Arbitrary keyword arguments to query the user.

        Returns:
            User: The first user matching the query.

        Raises:
            NoResultFound: If no user matches the query.
            InvalidRequestError: If invalid query arguments are provided.
        """
        if not kwargs:
            raise InvalidRequestError

        user = self._session.query(User).filter_by(**kwargs).first()
        if not user:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update a user's attributes in the database.

        Args:
            user_id (int): The ID of the user to update.
            **kwargs: Arbitrary keyword arguments
            representing attributes to update.

        Raises:
            ValueError: If any of the attributes passed are not valid.
        """
        # Find user by ID
        user = self.find_user_by(id=user_id)

        for key, value in kwargs.items():
            if not hasattr(user, key):
                # Raise if attribute is not valid
                raise ValueError(f"Invalid attribute: {key}")
            # Update the user's attribute
            setattr(user, key, value)

        self._session.commit()  # Commit the changes
        return None
