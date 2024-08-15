#!/usr/bin/env python3
"""
DB module for interacting with the database.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
# from sqlalchemy.exc import InvalidRequestError
# from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
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
        """
        Add a new user to the database.

        Parameters:
        - email (str): The user's email.
        - hashed_password (str): The user's hashed password.

        Returns:
        - User: The created User object.
        """
        try:
            new_user = User(email=email, hashed_password=hashed_password)
            self._session.add(new_user)
            self._session.commit()
        except Exception:
            self._session.rollback()
            new_user = None
        return new_user
    
    # def find_user_by(self, **kwargs) -> User:
    #     """
    #     Find a user by given keyword arguments.

    #     Parameters:
    #     - **kwargs: Search criteria.

    #     Returns:
    #     - User: The found User object.

    #     Raises:
    #     - InvalidRequestError: If the query arguments are invalid.
    #     - NoResultFound: If no results are found.
    #     """
    #     try:
    #         user = self._session.query(User).filter_by(**kwargs).one()
    #     except Exception as e:
    #         if isinstance(e, NoResultFound):
    #             raise NoResultFound("No result found")
    #         elif isinstance(e, InvalidRequestError):
    #             raise InvalidRequestError("Invalid request")
    #         raise
    #     return user

    # def update_user(self, user_id: int, **kwargs) -> None:
    #     """
    #     Update a user's attributes.

    #     Parameters:
    #     - user_id (int): The ID of the user to update.
    #     - **kwargs: Attributes to update.

    #     Raises:
    #     - ValueError: If an invalid attribute is passed.
    #     """
    #     user = self.find_user_by(id=user_id)
    #     for key, value in kwargs.items():
    #         if hasattr(user, key):
    #             setattr(user, key, value)
    #         else:
    #             raise ValueError(f"Invalid attribute {key}")
    #     self._session.commit()
