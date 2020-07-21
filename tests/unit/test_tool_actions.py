"""Module for testing AES tool actions."""

import pathlib
import unittest

from unittest import mock

from aes import constants
from aes import errors
from tool import actions

import base


class TestToolActions(base.BaseTestCase):
    """Tests for AES tool actions."""

    @mock.patch('padding.remove')
    @mock.patch('aes.decrypt')
    @mock.patch('aes.state.State.load')
    @mock.patch('aes.key.Key.load')
    def test_tool_decrypt(
            self,
            key_load_mock,
            state_load_mock,
            decrypt_mock,
            padding_remove_mock
    ):
        """Tests decrypting file."""
        file_mock = mock.MagicMock(spec=pathlib.Path)

        key_file_mock = mock.MagicMock(spec=pathlib.Path)
        key_mock = key_load_mock.return_value

        state_mock = mock.MagicMock()
        state_load_mock.side_effect = [state_mock, None]

        actions.decrypt(file_mock, key_file_mock)

        key_load_mock.assert_called_once_with(key_file_mock)
        self.assertEqual(2, state_load_mock.call_count)
        state_load_mock.assert_any_call(file_mock, 0)
        state_load_mock.assert_any_call(file_mock, 4 * constants.NB)
        decrypt_mock.assert_called_once_with(state_mock, key_mock)
        state_mock.dump.assert_called_once_with(file_mock, 0)
        padding_remove_mock.assert_called_once_with(file_mock)

    @mock.patch('aes.encrypt')
    @mock.patch('aes.state.State.load')
    @mock.patch('aes.key.Key.load')
    @mock.patch('padding.add')
    def test_tool_encrypt(
            self,
            padding_add_mock,
            key_load_mock,
            state_load_mock,
            encrypt_mock
    ):
        """Tests encrypting file."""
        file_mock = mock.MagicMock(spec=pathlib.Path)

        key_file_mock = mock.MagicMock(spec=pathlib.Path)
        key_mock = key_load_mock.return_value

        state_mock = mock.MagicMock()
        state_load_mock.side_effect = [state_mock, None]

        actions.encrypt(file_mock, key_file_mock)

        padding_add_mock.assert_called_once_with(file_mock, 4 * constants.NB)
        key_load_mock.assert_called_once_with(key_file_mock)
        self.assertEqual(2, state_load_mock.call_count)
        state_load_mock.assert_any_call(file_mock, 0)
        state_load_mock.assert_any_call(file_mock, 4 * constants.NB)
        encrypt_mock.assert_called_once_with(state_mock, key_mock)
        state_mock.dump.assert_called_once_with(file_mock, 0)

    @mock.patch('secrets.token_bytes')
    def test_tool_generate(self, token_bytes_mock):
        """Tests generating key."""
        token_bytes_mock.return_value = 42

        key_file_mock = mock.MagicMock(spec=pathlib.Path)

        for size in constants.ALLOWED_KEY_SIZES:
            open_mock = mock.mock_open(key_file_mock)

            file_handler_mock = open_mock.return_value

            with self.subTest(size=size):
                open_mock.reset_mock()
                token_bytes_mock.reset_mock()

                with mock.patch('builtins.open', open_mock):
                    actions.generate(key_file_mock, size)

                open_mock.assert_called_once_with(key_file_mock, 'wb')
                file_handler_mock.write.assert_called_once_with(42)
                token_bytes_mock.assert_called_once_with(size >> 3)

    def test_tool_generate_not_allowed_size(self):
        """Tests generating key of not allowed size."""
        sizes = self._generate_sizes(
            range(max(constants.ALLOWED_KEY_SIZES) << 1),
            self.tests,
            exclude=constants.ALLOWED_KEY_SIZES
        )

        key_file_mock = mock.MagicMock(spec=pathlib.Path)

        open_mock = mock.mock_open(key_file_mock)

        file_handler_mock = open_mock.return_value

        for size in sizes:
            self.assertRaises(
                errors.KeySizeError, actions.generate, key_file_mock, size)
            open_mock.assert_not_called()
            file_handler_mock.assert_not_called()


if __name__ == '__main__':
    unittest.main()
