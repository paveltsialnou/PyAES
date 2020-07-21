"""Module for testing padding."""

import pathlib
import tempfile
import unittest

import padding

import base


class TestPadding(base.BaseTestCase):
    """Tests for padding."""

    def setUp(self):
        self.file = pathlib.Path(tempfile.NamedTemporaryFile().name)

    def test_add(self):
        """Tests adding padding."""
        for size in range(self.tests):
            self._write_data(self.file, self._generate_data(size))

            with self.subTest(size=size):
                padding.add(self.file, self.size)

                self.assertFalse(len(self._read_data(self.file)) % self.size)

    def test_remove(self):
        """Tests removing padding."""
        for size in range(self.tests):
            data = self._generate_data(size)
            data += b'\x01'
            data += b'\x00' * (self.size - size % self.size)
            self._write_data(self.file, data)

            with self.subTest(size=size):
                padding.remove(self.file)

                self.assertEqual(
                    data.rpartition(b'\x01')[0], self._read_data(self.file))


if __name__ == "__main__":
    unittest.main()
