#!/usr/bin/env python3
"""
Unit Tests for the FileStorage class in a hypothetical data storage system.

Test Suites:
    InitializationTestsForFileStorage
    OperationalTestsForFileStorage
"""

import unittest
import models
import os
import json
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class InitializationTestsForFileStorage(unittest.TestCase):
    """Suite for testing initialization aspects of FileStorage."""

    def test_initialization_without_parameters(self):
        self.assertIsInstance(FileStorage(), FileStorage)

    def test_initialization_with_extra_parameter(self):
        with self.assertRaises(TypeError):
            FileStorage("extra_param")

    def test_file_path_private_string(self):
        self.assertIsInstance(FileStorage._FileStorage__file_path, str)

    def test_objects_private_dict(self):
        self.assertIsInstance(FileStorage._FileStorage__objects, dict)

    def test_storage_instance_creation(self):
        self.assertIsInstance(models.storage, FileStorage)


class OperationalTestsForFileStorage(unittest.TestCase):
    """Suite for testing operations of FileStorage."""

    @classmethod
    def setUpClass(cls):
        cls.backup_filename = "file_backup.json"
        cls.original_filename = "file.json"
        if os.path.exists(cls.original_filename):
            os.rename(cls.original_filename, cls.backup_filename)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.original_filename):
            os.remove(cls.original_filename)
        if os.path.exists(cls.backup_filename):
            os.rename(cls.backup_filename, cls.original_filename)
        FileStorage._FileStorage__objects = {}

    def test_all_method_returns_dict(self):
        self.assertIsInstance(models.storage.all(), dict)

    def test_all_method_with_argument(self):
        with self.assertRaises(TypeError):
            models.storage.all("unexpected_arg")

    def test_new_method_storage(self):
        entities = [BaseModel(), User(), State(), Place(), City(),
                    Amenity(), Review()]
        for entity in entities:
            models.storage.new(entity)
            entity_key = f"{entity.__class__.__name__}.{entity.id}"
            self.assertIn(entity_key, models.storage.all())

    def test_new_method_invalid_argument(self):
        with self.assertRaises(TypeError):
            models.storage.new(BaseModel, "extra")

        with self.assertRaises(AttributeError):
            models.storage.new(None)

    def test_save_method_file_creation(self):
        instance = BaseModel()
        models.storage.new(instance)
        models.storage.save()
        self.assertTrue(os.path.isfile('file.json'))

    def test_save_method_with_argument(self):
        with self.assertRaises(TypeError):
            models.storage.save("unexpected_arg")

    def test_reload(self):
        bm = BaseModel()
        us = User()
        st = State()
        pl = Place()
        cy = City()
        am = Amenity()
        rv = Review()
        models.storage.new(bm)
        models.storage.new(us)
        models.storage.new(st)
        models.storage.new(pl)
        models.storage.new(cy)
        models.storage.new(am)
        models.storage.new(rv)
        models.storage.save()
        models.storage.reload()
        objs = models.storage._FileStorage__objects
        self.assertIn("BaseModel." + bm.id, objs)
        self.assertIn("User." + us.id, objs)
        self.assertIn("State." + st.id, objs)
        self.assertIn("Place." + pl.id, objs)
        self.assertIn("City." + cy.id, objs)
        self.assertIn("Amenity." + am.id, objs)
        self.assertIn("Review." + rv.id, objs)

    def test_reload_without_existing_file(self):
        if os.path.exists('file.json'):
            os.remove('file.json')
        try:
            models.storage.reload()
            exception_raised = False
        except FileNotFoundError:
            exception_raised = True
        self.assertFalse(exception_raised)

    def test_reload_with_argument(self):
        with self.assertRaises(TypeError):
            models.storage.reload("unexpected_arg")


if __name__ == "__main__":
    unittest.main()
