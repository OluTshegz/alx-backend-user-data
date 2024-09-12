#!/usr/bin/env python3
"""
User model using SQLAlchemy
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Create a base class using declarative_base()
Base = declarative_base()


class User(Base):
    """
    User class that represents the users table
    """
    __tablename__ = 'users'

    # Define the columns for the users table
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
