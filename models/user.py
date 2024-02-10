#!/usr/bin/python3
"""Defines a User class"""
from .base_model import BaseModel


class User(BaseModel):
    """represents a User """

    email = ""
    password = ""
    first_name = ""
    last_name = ""
