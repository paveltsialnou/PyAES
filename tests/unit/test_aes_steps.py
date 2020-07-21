"""Module for testing AES steps."""

import copy
import random
import unittest

from unittest import mock

from aes import constants
from aes import steps
from aes.key import Key
from aes.state import State

import base


class TestSteps(base.BaseTestCase):
    """Tests for AES steps."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.key = Key.load(cls._generate_data(cls.size))

    def setUp(self):
        self.state = State.load(
            bytearray(self._generate_data(self.size)), self.offset)

    def test_add_round_key(self):
        """Tests adding current_round keys."""
        previous = copy.deepcopy(self.state)
        current_round = random.randrange(constants.ROUNDS[self.key.size])

        steps.add_round_key(
            self.state, self.key.schedule, current_round=current_round)

        for row_id, row in enumerate(previous):
            for col_id, elem in enumerate(row):
                key_schedule_col_id = 4 * current_round + col_id

                with self.subTest(ids=(row_id, col_id)):
                    self.assertEqual(
                        elem ^ self.key.schedule[row_id][key_schedule_col_id],
                        self.state[row_id][col_id]
                    )

    @mock.patch('aes.utils.galois_mul')
    def test_mix_columns(self, multiply_matrix_by_vector_mock):
        """Tests mixing columns."""
        new_columns = [
            random.choices(range(255), k=4),
            random.choices(range(255), k=4),
            random.choices(range(255), k=4),
            random.choices(range(255), k=4)
        ]
        multiply_matrix_by_vector_mock.side_effect = new_columns * 2

        for inverse in False, True:
            with self.subTest(inverse=inverse):
                steps.mix_columns(self.state, inverse=inverse)

                self.assertEqual(
                    [bytearray(column) for column in zip(*new_columns)],
                    self.state
                )

    def test_shift_rows(self):
        """Tests shifting rows."""
        previous = copy.deepcopy(self.state)

        steps.shift_rows(self.state)

        for row_id in range(4):
            with self.subTest(row_id=row_id):
                self.assertEqual(
                    [*previous[row_id][row_id:], *previous[row_id][:row_id]],
                    self.state[row_id]
                )

    def test_shift_rows_inverse(self):
        """Tests shifting rows inverse."""
        previous = copy.deepcopy(self.state)

        steps.shift_rows(self.state, inverse=True)

        for row_id in range(4):
            with self.subTest(row_id=row_id):
                self.assertEqual(
                    [*previous[row_id][-row_id:], *previous[row_id][:-row_id]],
                    self.state[row_id]
                )

    @mock.patch('aes.utils.sub_word')
    def test_sub_bytes(self, sub_word_mock):
        """Tests substituting bytes."""
        new_words = [
            random.choices(range(255), k=4),
            random.choices(range(255), k=4),
            random.choices(range(255), k=4),
            random.choices(range(255), k=4)
        ]
        sub_word_mock.side_effect = new_words * 2

        for inverse in False, True:
            steps.sub_bytes(self.state, inverse=inverse)

            with self.subTest(inverse=inverse):
                self.assertEqual(new_words, self.state)


if __name__ == '__main__':
    unittest.main()
