#!/usr/bin/python3
"""Defines the BaseModel class"""
from uuid import uuid4
from datetime import datetime
import models
class BaseModel:
    """The BaseModel for HBNB project."""

    def __init__(self, *args, **kwargs):
        """ Initialize a new BaseModel instance
        Args:
            *args: Unused
            **kwargs(dict): key/value pairs of attributes.
        """
        tform = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()
        
        ignored_attr = ['__class__']
        if len(kwargs) !=0:
            for key, value in kwargs.items():
                if key in ['created_at', 'updated_at']:
                        setattr(self, key, datetime.strptime(value, tform))
                elif key not in ignored_attr:
                    setattr(self, key, value)
        else:
            models.storage.new(self)

    def __str__(self):
        """Return the formated string representation"""
        return "[{}] ({}) {}".format(
            self.__class__.__name__,
            self.id,
            self.__dict__
        )

    def save(self):
        """updates the updated_at with the current datetime."""
        self.updated_at = datetime.today()
        models.storage.save()

    def to_dict(self):
        """Returns a dictionary containing all k/v of __dict__ of
        the instance"""
        idict = self.__dict__.copy()
        idict["__class__"] = self.__class__.__name__
        idict["updated_at"] = self.updated_at.isoformat()
        idict["created_at"] = self.created_at.isoformat()
        return idict
