#!/usr/bin/env python3
"""
Unit Tests for BaseModel class in a hypothetical model system.

Test Suites:
    BaseModelCreationTests
    BaseModelPersistenceTests
    BaseModelSerializationTests
"""

import unittest
from models.base_model import BaseModel
from datetime import datetime
import models
from time import sleep
import os


class BaseModelCreationTests(unittest.TestCase):
    """Test suite for validating instantiation of BaseModel."""

    def test_default_constructor(self):
        instance = BaseModel()
        self.assertIsInstance(instance, BaseModel)

    def test_unique_id_for_each_instance(self):
        instance1 = BaseModel()
        instance2 = BaseModel()
        self.assertNotEqual(instance1.id, instance2.id)

    def test_public_attributes(self):
        instance = BaseModel()
        self.assertTrue(hasattr(instance, "id"))
        self.assertTrue(hasattr(instance, "created_at"))
        self.assertTrue(hasattr(instance, "updated_at"))
        self.assertIsInstance(instance.created_at, datetime)
        self.assertIsInstance(instance.updated_at, datetime)

    def test_time_attributes_differ_for_separate_instances(self):
        instance1 = BaseModel()
        sleep(0.1)
        instance2 = BaseModel()
        self.assertNotEqual(instance1.created_at, instance2.created_at)
        self.assertNotEqual(instance1.updated_at, instance2.updated_at)

    def test_string_representation_format(self):
        instance = BaseModel()
        str_format = f"[BaseModel] ({instance.id}) {instance.__dict__}"
        self.assertEqual(str_format, instance.__str__())

    def test_constructor_ignores_args(self):
        instance = BaseModel("arg1", "arg2")
        self.assertNotIn("arg1", instance.__dict__)
        self.assertNotIn("arg2", instance.__dict__)

    def test_constructor_with_kwargs(self):
        time_now = datetime.now()
        instance = BaseModel(id="123", created_at=time_now.isoformat(),
                             updated_at=time_now.isoformat())
        self.assertEqual(instance.id, "123")
        self.assertEqual(instance.created_at, time_now)
        self.assertEqual(instance.updated_at, time_now)


class BaseModelPersistenceTests(unittest.TestCase):
    """Test suite for testing persistence methods of BaseModel."""

    @classmethod
    def setUpClass(cls):
        cls.prev_filename = "file.json"
        cls.temp_filename = "temp.json"
        if os.path.exists(cls.prev_filename):
            os.rename(cls.prev_filename, cls.temp_filename)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.prev_filename):
            os.remove(cls.prev_filename)
        if os.path.exists(cls.temp_filename):
            os.rename(cls.temp_filename, cls.prev_filename)

    def test_save_method_updates_time(self):
        instance = BaseModel()
        original_time = instance.updated_at
        sleep(0.05)
        instance.save()
        self.assertNotEqual(original_time, instance.updated_at)

    def test_save_creates_or_updates_file(self):
        instance = BaseModel()
        instance.save()
        self.assertTrue(os.path.isfile('file.json'))
        with open('file.json', 'r') as f:
            self.assertIn(instance.id, f.read())


class BaseModelSerializationTests(unittest.TestCase):
    """Tests for verifying the serialization of BaseModel to a dictionary."""

    def test_to_dict_returns_dictionary(self):
        instance = BaseModel()
        self.assertIsInstance(instance.to_dict(), dict)

    def test_to_dict_contains_expected_keys(self):
        instance = BaseModel()
        self.assertIn("id", instance.to_dict())
        self.assertIn("created_at", instance.to_dict())
        self.assertIn("updated_at", instance.to_dict())
        self.assertIn("__class__", instance.to_dict())

    def test_to_dict_with_additional_attributes(self):
        instance = BaseModel()
        instance.name = "Test Name"
        instance.number = 101
        instance_dict = instance.to_dict()
        self.assertIn("name", instance_dict)
        self.assertIn("number", instance_dict)

    def test_datetime_conversion_to_string_in_dict(self):
        instance = BaseModel()
        instance_dict = instance.to_dict()
        self.assertIsInstance(instance_dict["created_at"], str)
        self.assertIsInstance(instance_dict["updated_at"], str)

    def test_to_dict_vs_dunder_dict(self):
        instance = BaseModel()
        self.assertNotEqual(instance.to_dict(), instance.__dict__)

    def test_invalid_argument_to_to_dict(self):
        instance = BaseModel()
        with self.assertRaises(TypeError):
            instance.to_dict("invalid_argument")


if __name__ == "__main__":
    unittest.main()
