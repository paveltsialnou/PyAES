"""Module for testing AES decrypt/encrypt."""

import unittest

from unittest import mock

import aes

from aes import constants
from aes import key
from aes.state import State

import base


class TestAES(base.BaseTestCase):
    """Tests for AES decrypt/encrypt."""

    def setUp(self):
        self.state = State.load(
            bytearray(self._generate_data(self.size)), self.offset)

    @mock.patch('aes.steps.sub_bytes')
    @mock.patch('aes.steps.shift_rows')
    @mock.patch('aes.steps.mix_columns')
    @mock.patch('aes.steps.add_round_key')
    def test_decrypt(
            self,
            add_round_key_mock,
            mix_columns_mock,
            shift_rows_mock,
            sub_bytes_mock
    ):
        """Tests decrypting State."""
        for size in constants.ALLOWED_KEY_SIZES:
            rounds = constants.ROUNDS[size]
            key_ = key.Key(self._generate_data(size >> 3))

            with self.subTest(size=size):
                add_round_key_mock.reset_mock()
                mix_columns_mock.reset_mock()
                shift_rows_mock.reset_mock()
                sub_bytes_mock.reset_mock()

                aes.decrypt(self.state, key_)

                self.assertEqual(rounds + 1, add_round_key_mock.call_count)
                self.assertEqual(rounds - 1, mix_columns_mock.call_count)
                self.assertEqual(rounds, shift_rows_mock.call_count)
                self.assertEqual(rounds, sub_bytes_mock.call_count)

    @mock.patch('aes.steps.sub_bytes')
    @mock.patch('aes.steps.shift_rows')
    @mock.patch('aes.steps.mix_columns')
    @mock.patch('aes.steps.add_round_key')
    def test_encrypt(
            self,
            add_round_key_mock,
            mix_columns_mock,
            shift_rows_mock,
            sub_bytes_mock
    ):
        """Tests encrypting State."""
        for size in constants.ALLOWED_KEY_SIZES:
            rounds = constants.ROUNDS[size]
            key_ = key.Key(self._generate_data(size >> 3))

            with self.subTest(size=size):
                add_round_key_mock.reset_mock()
                mix_columns_mock.reset_mock()
                shift_rows_mock.reset_mock()
                sub_bytes_mock.reset_mock()

                aes.encrypt(self.state, key_)

                self.assertEqual(rounds + 1, add_round_key_mock.call_count)
                self.assertEqual(rounds - 1, mix_columns_mock.call_count)
                self.assertEqual(rounds, shift_rows_mock.call_count)
                self.assertEqual(rounds, sub_bytes_mock.call_count)


if __name__ == '__main__':
    unittest.main()
