"""State objects."""

import collections
import functools
import pathlib

from itertools import chain

from aes import constants
from aes import errors


class State(collections.UserList):
    """Represents state to act over."""

    def __init__(self, data):
        if len(data) != 4 * constants.NB:
            raise errors.StateSizeError()

        super().__init__(bytearray(data[i::4]) for i in range(4))

    @functools.singledispatchmethod
    def dump(self, data, offset):
        """Writes state to data."""
        raise NotImplementedError()

    @dump.register(bytearray)
    def _(self, data, offset):
        data[offset:offset + 4 * constants.NB] = chain.from_iterable(
            zip(*self.data))

    @dump.register(pathlib.Path)
    def _(self, file_path, offset):
        """Writes state to file."""
        with open(file_path, 'rb+') as file:
            file.seek(offset)

            for column in zip(*self.data):
                file.write(bytes(column))

    @functools.singledispatchmethod
    @classmethod
    def load(cls, data, offset):
        """Loads state from data."""
        raise NotImplementedError()

    @load.register(bytearray)
    @classmethod
    def _(cls, data, offset=0):
        data = data[offset:offset + 16]
        if data:
            return State(data)

        return None

    @load.register(pathlib.Path)
    @classmethod
    def _(cls, file_path, offset=0):
        with open(file_path, 'rb') as file:
            file.seek(offset)

            data = file.read(16)
            if data:
                return State(data)

        return None
