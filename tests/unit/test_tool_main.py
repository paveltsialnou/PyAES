"""Module for testing AES tool main."""

import io
import pathlib
import sys
import unittest

from unittest import mock

from tool import __main__

from aes import constants

import base


class TestMain(base.BaseTestCase):
    """Tests for AES tool main."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.file = pathlib.Path(cls._generate_data(42, urlsafe=True))
        cls.key = pathlib.Path(
            cls._generate_data(42, urlsafe=True)).with_suffix('.key')

        cls.stderr, cls.stdout = sys.stderr, sys.stdout
        sys.stderr, sys.stdout = io.StringIO(), io.StringIO()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

        sys.stderr, sys.stdout = cls.stderr, cls.stdout

    @mock.patch('tool.actions.decrypt')
    def test_main_decrypt(self, decrypt_mock):
        """Tests decrypting with key."""
        command = f'decrypt {self.file.name} {self.key.name}'.split()

        __main__.main(*command)

        decrypt_mock.assert_called_once_with(self.file, self.key)

    @mock.patch('tool.actions.decrypt')
    def test_main_decrypt_no_file(self, decrypt_mock):
        """Tests decrypting without file."""
        command = f'decrypt {self.key.name}'.split()

        self.assertRaises(SystemExit, __main__.main, *command)
        decrypt_mock.assert_not_called()

    @mock.patch('tool.actions.decrypt')
    def test_main_decrypt_no_key(self, decrypt_mock):
        """Tests decrypting without key."""
        command = f'decrypt {self.file.name}'.split()

        self.assertRaises(SystemExit, __main__.main, *command)
        decrypt_mock.assert_not_called()

    @mock.patch('tool.actions.encrypt')
    def test_main_encrypt(self, encrypt_mock):
        """Tests encrypting with key."""
        command = f'encrypt {self.file.name} {self.key.name}'.split()

        __main__.main(*command)

        encrypt_mock.assert_called_once_with(self.file, self.key)

    @mock.patch('tool.actions.encrypt')
    def test_main_encrypt_no_file(self, encrypt_mock):
        """Tests encrypting without file."""
        command = f'encrypt {self.key.name}'.split()

        self.assertRaises(SystemExit, __main__.main, *command)
        encrypt_mock.assert_not_called()

    @mock.patch('tool.actions.encrypt')
    def test_main_encrypt_no_key(self, encrypt_mock):
        """Tests encrypting without key."""
        command = f'encrypt {self.file.name}'.split()

        self.assertRaises(SystemExit, __main__.main, *command)
        encrypt_mock.assert_not_called()

    @mock.patch('tool.actions.generate')
    def test_main_generate(self, generate_mock):
        """Tests generating keys."""
        for size in constants.ALLOWED_KEY_SIZES:
            command = f'generate -s {size} {self.key.name}'.split()

            with self.subTest(size=size):
                generate_mock.reset_mock()

                __main__.main(*command)

                generate_mock.assert_called_once_with(self.key, size)

    @mock.patch('tool.actions.generate')
    def test_main_generate_default(self, generate_mock):
        """Tests generating key of default size."""
        command = f'generate {self.key.name}'.split()

        __main__.main(*command)

        generate_mock.assert_called_once_with(
            self.key, constants.DEFAULT_KEY_SIZE)

    @mock.patch('tool.actions.generate')
    def test_main_generate_no_file_path(self, generate_mock):
        """Tests generating key without path."""
        for size in constants.ALLOWED_KEY_SIZES:
            command = f'generate -s {size}'.split()

            with self.subTest(size=size):
                self.assertRaises(SystemExit, __main__.main, *command)

                generate_mock.assert_not_called()

    @mock.patch('tool.actions.generate')
    def test_main_generate_no_key_size(self, generate_mock):
        """Tests generating key without key size."""
        for size in constants.ALLOWED_KEY_SIZES:
            command = f'generate {self.key.name} -s'.split()

            with self.subTest(size=size):
                self.assertRaises(SystemExit, __main__.main, *command)

                generate_mock.assert_not_called()

    @mock.patch('tool.actions.generate')
    def test_main_generate_not_allowed_size(self, generate_mock):
        """Tests generating key of not allowed  sizes."""
        sizes = self._generate_sizes(
            range(max(constants.ALLOWED_KEY_SIZES) << 1),
            self.tests,
            exclude=constants.ALLOWED_KEY_SIZES
        )
        for size in sizes:
            command = f'generate -s {size} {self.key.name}'.split()

            with self.subTest(size=size):
                self.assertRaises(SystemExit, __main__.main, *command)

                generate_mock.assert_not_called()


if __name__ == '__main__':
    unittest.main()
