"""Module for testing AES states."""

import pathlib
import unittest

from unittest import mock

from aes import constants, errors
from aes import key
from aes import state
from aes import steps

import base


class TestState(base.BaseTestCase):
    """Tests for AES states."""

    def setUp(self):
        self.data = self._generate_data(self.size)
        self.key = key.Key(
            self._generate_data(constants.DEFAULT_KEY_SIZE >> 3))

    def test_state_allowed_size(self):
        """Tests initializing State of allowed size."""
        state_ = state.State(bytearray(self.data))

        self.assertEqual(self.size, sum(map(len, state_)))

    def test_state_dump_to_bytes(self):
        """Tests dumping State to bytes."""
        data = bytearray(self.data)
        state_ = state.State.load(data, self.offset)
        steps.add_round_key(state_, self.key.schedule, current_round=2)

        state_.dump(data, self.offset)

        self.assertNotEqual(bytearray(self.data), data)

    def test_state_dump_to_file(self):
        """Tests dumping State to files."""
        file_mock = mock.MagicMock(spec=pathlib.Path)
        open_mock = mock.mock_open(file_mock, self.data)
        file_handler_mock = open_mock.return_value

        with mock.patch('builtins.open', open_mock):
            state_ = state.State.load(file_mock, self.offset)
            steps.add_round_key(state_, self.key.schedule, current_round=2)

            state_.dump(file_mock, self.offset)

        self.assertEqual(2, open_mock.call_count)
        open_mock.assert_any_call(file_mock, 'rb')
        open_mock.assert_any_call(file_mock, 'rb+')
        self.assertEqual(2, file_handler_mock.seek.call_count)
        file_handler_mock.seek.assert_any_call(self.offset)
        file_handler_mock.read.assert_called_once_with(self.size)
        self.assertEqual(4, file_handler_mock.write.call_count)
        file_handler_mock.write.assert_any_call(bytes(c[0] for c in state_))
        file_handler_mock.write.assert_any_call(bytes(c[1] for c in state_))
        file_handler_mock.write.assert_any_call(bytes(c[2] for c in state_))
        file_handler_mock.write.assert_any_call(bytes(c[3] for c in state_))

    def test_state_dump_to_non_bytes(self):
        """Tests dumping State to non-bytes."""
        state_ = state.State.load(bytearray(self.data), self.offset)

        self.assertRaises(NotImplementedError, state_.dump, 42, self.offset)

    def test_state_load_after_bytes_end(self):
        """Tests loading State after the end of bytes."""
        data = bytearray(self.data)

        self.assertIsNone(state.State.load(data, self.size))

    def test_state_load_after_file_end(self):
        """Tests loading State after the end of file."""
        file_mock = mock.MagicMock(spec=pathlib.Path)
        open_mock = mock.mock_open(file_mock, b'')
        file_handler_mock = open_mock.return_value

        with mock.patch('builtins.open', open_mock):
            self.assertIsNone(
                state.State.load(file_mock, self.offset))

        open_mock.assert_called_once_with(file_mock, 'rb')
        file_handler_mock.seek.assert_called_once_with(self.offset)
        file_handler_mock.read.assert_called_once_with(self.size)

    def test_state_load_from_bytes(self):
        """Tests loading State from bytes."""
        data = bytearray(self.data)

        self.assertEqual(
            state.State(data), state.State.load(data, self.offset))

    def test_state_load_from_file(self):
        """Tests loading State from file."""
        file_mock = mock.MagicMock(spec=pathlib.Path)
        open_mock = mock.mock_open(file_mock, self.data)
        file_handler_mock = open_mock.return_value

        with mock.patch('builtins.open', open_mock):
            state_ = state.State.load(file_mock, self.offset)

        self.assertEqual(state.State(bytearray(self.data)), state_)
        open_mock.assert_called_once_with(file_mock, 'rb')
        file_handler_mock.seek.assert_called_once_with(self.offset)
        file_handler_mock.read.assert_called_once_with(self.size)

    def test_state_load_from_non_bytes(self):
        """Tests loading State from non-bytes."""
        self.assertRaises(
            NotImplementedError, state.State.load, 42, self.offset)

    def test_state_not_allowed_sizes(self):
        """Tests initializing State of not allowed sizes."""
        sizes = self._generate_sizes(
            range(self.size << 1), self.tests, exclude={self.size})
        for size in sizes:
            data = bytearray(self._generate_data(size))
            with self.subTest(size=size):
                self.assertRaises(errors.StateSizeError, state.State, data)


if __name__ == '__main__':
    unittest.main()
