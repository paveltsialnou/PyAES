"""Module with base test class."""

import random
import secrets
import unittest

from aes import constants


class BaseTestCase(unittest.TestCase):
    """Base test class."""

    @classmethod
    def setUpClass(cls):
        cls.offset = 0
        cls.size = 4 * constants.NB
        cls.tests = 200

    @staticmethod
    def _generate_data(size, *, urlsafe=False):
        if urlsafe:
            token = secrets.token_urlsafe
        else:
            token = secrets.token_bytes

        return token(size)

    @staticmethod
    def _generate_sizes(sample, amount, *, exclude=frozenset()):
        yield from random.choices(tuple(set(sample) - set(exclude)), k=amount)

    @staticmethod
    def _read_data(file_path):
        with open(file_path, 'rb') as file:
            return file.read()

    @staticmethod
    def _write_data(file_path, data):
        with open(file_path, 'wb') as file:
            file.write(data)
