#!/usr/bin/env python3
"""
User model using SQLAlchemy
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from typing import Optional


# Create a base class using declarative_base()
Base = declarative_base()


class User(Base):
    """
    User class that represents the users table
    """
    __tablename__ = 'users'

    # Define the columns for the users table
    id: int = Column(Integer, primary_key=True)
    email: str = Column(String(250), nullable=False)
    hashed_password: str = Column(String(250), nullable=False)
    session_id: Optional[str] = Column(String(250), nullable=True)
    reset_token: Optional[str] = Column(String(250), nullable=True)

    def __init__(self, email: str, hashed_password: str,
                 session_id: Optional[str] = None,
                 reset_token: Optional[str] = None):
        self.email = email
        self.hashed_password = hashed_password
        self.session_id = session_id
        self.reset_token = reset_token
