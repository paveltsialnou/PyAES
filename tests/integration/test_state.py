"""Module for testing state."""

import pathlib
import tempfile
import unittest

from aes import constants
from aes import steps
from aes.key import Key
from aes.state import State
from tool import actions

import base


class TestState(base.BaseTestCase):
    """Tests for state."""

    def setUp(self):
        self.data = self._generate_data(self.size * self.tests)
        self.file = pathlib.Path(tempfile.NamedTemporaryFile().name)
        self.key = pathlib.Path(tempfile.NamedTemporaryFile().name)

        self._write_data(self.file, self.data)
        actions.generate(self.key, constants.DEFAULT_KEY_SIZE)

    def test_load(self):
        """Tests loading state from file."""
        for test in range(self.tests):
            offset = test * self.size

            with self.subTest(offset=offset):
                state = State.load(self.file, offset)

                self.assertEqual(
                    State.load(bytearray(self.data), offset), state)

    def test_dump(self):
        """Tests dumping state to file."""
        key = Key.load(self.key)

        for test in range(self.tests):
            offset = test * self.size
            state = State.load(self.file, offset)
            steps.add_round_key(state, key.schedule, current_round=2)

            with self.subTest(offset=offset):
                state.dump(self.file, offset)

                self.assertNotEqual(state, State.load(self.file, offset))


if __name__ == "__main__":
    unittest.main()
