#!/usr/bin/python3
"""Defines a city class"""
from .base_model import BaseModel


class City(BaseModel):
    """Represents a city"""
    state_id = ""
    name = ""
