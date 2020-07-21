"""Module for testing AES keys."""

import pathlib
import unittest

from unittest import mock

from aes import constants
from aes import errors
from aes import key

import base


class TestAESKey(base.BaseTestCase):
    """Tests for AES keys."""

    def test_key_allowed_sizes(self):
        """Tests initializing Key of allowed sizes."""
        for size in constants.ALLOWED_KEY_SIZES:
            data = self._generate_data(size >> 3)

            with self.subTest(size=size):
                key_ = key.Key(data)

                self.assertEqual(size, key_.size)
                self.assertEqual(size >> 5, key_.words)
                self.assertEqual(data, key_.data)
                self.assertIsInstance(key_.schedule, key.KeySchedule)

    def test_key_load_from_bytes(self):
        """Tests loading Key from bytes."""
        for size in constants.ALLOWED_KEY_SIZES:
            data = self._generate_data(size >> 3)

            with self.subTest(size=size):
                self.assertEqual(key.Key(data), key.Key.load(data))

    def test_key_load_from_file(self):
        """Tests loading Key from file."""
        key_file_mock = mock.MagicMock(spec=pathlib.Path)

        for size in constants.ALLOWED_KEY_SIZES:
            data = self._generate_data(size >> 3)

            open_mock = mock.mock_open(key_file_mock, data)

            file_handler_mock = open_mock.return_value

            with self.subTest(size=size):
                open_mock.reset_mock()

                with mock.patch('builtins.open', open_mock):
                    key_ = key.Key.load(key_file_mock)

                self.assertEqual(data, key_.data)
                open_mock.assert_called_once_with(key_file_mock, 'rb')
                file_handler_mock.read.assert_called_once()

    def test_key_load_from_non_bytes(self):
        """Tests loading Key from non-bytes."""
        self.assertRaises(NotImplementedError, key.Key.load, 42)

    def test_key_not_allowed_sizes(self):
        """Tests initializing Key of not allowed sizes."""
        sizes = self._generate_sizes(
            range(max(constants.ALLOWED_KEY_SIZES) << 1),
            self.tests,
            exclude={size >> 3 for size in constants.ALLOWED_KEY_SIZES}
        )
        for size in sizes:
            data = self._generate_data(size)

            with self.subTest(size=size):
                self.assertRaises(errors.KeySizeError, key.Key, data)


if __name__ == '__main__':
    unittest.main()
