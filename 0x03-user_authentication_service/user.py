#!/usr/bin/env python3
"""A SQLAlchemy model."""

# from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from typing import Optional


Base = declarative_base()


class User(Base):
    """The SQLAlchemy model, User, for the database table users."""
    __tablename__ = 'users'

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
