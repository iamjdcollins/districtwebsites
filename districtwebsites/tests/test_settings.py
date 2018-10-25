from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase

from districtwebsites.settings.base import load_secrets, get_secret
from districtwebsites.settings import (
    development,
    testing,
    production
)


class BaseTestCase(TestCase):

    def test_invalid_secret_file(self):
        with self.assertRaises(ImproperlyConfigured):
            load_secrets('.invaid_file')

    def test_secret_key_exists(self):
        self.assertIsInstance(get_secret('SECRET_KEY'), str)

    def test_invalid_secret_key(self):
        with self.assertRaises(ImproperlyConfigured):
            get_secret('NOT_VALID')

    def test_true_key(self):
        settings = {'True': 'True'}
        self.assertTrue(get_secret('True', settings))

    def test_false_key(self):
        settings = {'False': 'False'}
        self.assertFalse(get_secret('False', settings))


class DevelopmentTestCase(TestCase):

    def test_correct_environment(self):
        self.assertEqual(development.ENVIRONMENT, 'DEVELOPMENT')


class TestingTestCase(TestCase):

    def test_correct_environment(self):
        self.assertEqual(testing.ENVIRONMENT, 'TESTING')


class ProductionTestCase(TestCase):

    def test_correct_environment(self):
        self.assertEqual(production.ENVIRONMENT, 'PRODUCTION')
