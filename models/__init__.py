#!/usr/bin/python3
"""
__init__ the constructor for the models dir
"""
from .engine.file_storage import FileStorage


storage = FileStorage()
storage.reload()
