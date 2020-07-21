"""Module for testing actions."""

import pathlib
import tempfile
import unittest

from aes import constants
from aes import errors
from tool import actions

import base


class TestActions(base.BaseTestCase):
    """Tests for actions."""

    def setUp(self):
        self.file = pathlib.Path(tempfile.NamedTemporaryFile().name)
        self.key = pathlib.Path(tempfile.NamedTemporaryFile().name)

        actions.generate(self.key, constants.DEFAULT_KEY_SIZE)

    def test_decrypt(self):
        """Tests decrypting file."""
        for size in range(self.tests):
            data = self._generate_data(size)
            self._write_data(self.file, data)

            with self.subTest(size=size):
                actions.encrypt(self.file, self.key)
                actions.decrypt(self.file, self.key)

                self.assertEqual(data, self._read_data(self.file))

    def test_encrypt(self):
        """Tests encrypting file."""
        for size in range(self.tests):
            data = self._generate_data(size)
            self._write_data(self.file, data)

            with self.subTest(size=size):
                actions.encrypt(self.file, self.key)

                self.assertNotEqual(data, self._read_data(self.file))

    def test_generate_allowed_sizes(self):
        """Tests generating keys of allowed sizes."""
        for size in constants.ALLOWED_KEY_SIZES:
            with self.subTest(size=size):
                actions.generate(self.key, size)

                self.assertEqual(size >> 3, len(self._read_data(self.key)))

    def test_generate_not_allowed_sizes(self):
        """Tests generating keys of not allowed sizes."""
        sizes = self._generate_sizes(
            range(max(constants.ALLOWED_KEY_SIZES) << 1),
            self.tests,
            exclude=constants.ALLOWED_KEY_SIZES
        )
        for size in sizes:
            with self.subTest(size=size):
                self.assertRaises(
                    errors.KeySizeError, actions.generate, self.key, size)


if __name__ == "__main__":
    unittest.main()
