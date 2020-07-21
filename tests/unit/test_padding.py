"""Module for testing padding."""

import pathlib
import unittest

from unittest import mock

import padding

import base


class TestPadding(base.BaseTestCase):
    """Tests for padding."""

    def test_add(self):
        """Tests adding padding."""
        for size in range(self.tests):
            data = bytearray(self._generate_data(size))

            with self.subTest(size=size):
                padding.add(data, self.size)

                self.assertFalse(len(data) % self.size)

    def test_add_to_file(self):
        """Tests adding padding to file."""
        file_mock = mock.MagicMock(spec=pathlib.Path)

        open_mock = mock.mock_open(file_mock)

        file_handler_mock = open_mock.return_value
        for size in range(self.size):
            file_handler_mock.tell.return_value = size + 1

            with self.subTest(size=size):
                open_mock.reset_mock()

                with mock.patch('builtins.open', open_mock):
                    padding.add(file_mock, self.size)

                open_mock.assert_called_once_with(file_mock, 'ab')
                file_handler_mock.write.assert_any_call(b'\x01')
                file_handler_mock.tell.assert_called_once()
                zeros_padding = b'\x00' * (
                    self.size - file_handler_mock.tell() % self.size)
                file_handler_mock.write.assert_any_call(zeros_padding)

    def test_add_to_non_bytes(self):
        """Tests adding padding to non-bytes."""
        self.assertRaises(NotImplementedError, padding.add, 42, self.size)

    def test_remove(self):
        """Tests removing padding."""
        for size in range(self.tests):
            data = bytearray(self._generate_data(size))
            padding.add(data, self.size)

            with self.subTest(size=size):
                padding.remove(data)

                self.assertEqual(size, len(data))

    def test_remove_from_file(self):
        """Tests removing padding from file."""
        file_mock = mock.MagicMock(spec=pathlib.Path)

        for size in range(self.tests):
            data = self._generate_data(size)
            data += b'\x01'
            zeros = (self.size - (size + 1) % self.size)
            data += b'\x00' * zeros

            open_mock = mock.mock_open(file_mock, data)

            file_handler_mock = open_mock.return_value
            file_handler_mock.tell.return_value = size + 1

            with self.subTest(size=size):
                open_mock.reset_mock()

                with mock.patch('builtins.open', open_mock):
                    padding.remove(file_mock)

                open_mock.assert_called_once_with(file_mock, 'ab+')
                file_handler_mock.seek.assert_any_call(-1, 1)
                file_handler_mock.read.assert_called_with(1)
                file_handler_mock.truncate.assert_called_with(size)

    def test_remove_from_non_bytes(self):
        """Tests removing padding from non-bytes."""
        self.assertRaises(NotImplementedError, padding.remove, 42)


if __name__ == "__main__":
    unittest.main()
