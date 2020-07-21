"""AES keys."""

import collections
import functools
import pathlib

from aes import constants
from aes import errors
from aes import utils


class Key:
    """Represents a secret key."""

    def __init__(self, data):
        self.__data = data
        self.__schedule = None
        self.__size = None
        self.__words = None

        if self.size not in constants.ALLOWED_KEY_SIZES:
            raise errors.KeySizeError()

    def __eq__(self, other):
        return self.data == other.data

    @property
    def data(self):
        """Key's data."""
        return self.__data

    @property
    def schedule(self):
        """Key schedule."""
        if self.__schedule is None:
            self.__schedule = KeySchedule(self)

        return self.__schedule

    @property
    def size(self):
        """Key size in bits."""
        if self.__size is None:
            self.__size = len(self.data) << 3

        return self.__size

    @property
    def words(self):
        """Key size in 32-bit words."""
        if self.__words is None:
            self.__words = self.size >> 5

        return self.__words

    @functools.singledispatchmethod
    @classmethod
    def load(cls, data):
        """Creates key from data."""
        raise NotImplementedError()

    @load.register(bytes)
    @classmethod
    def _(cls, key_data):
        return cls(key_data)

    @load.register(pathlib.Path)
    @classmethod
    def _(cls, key_file):
        with open(key_file, 'rb') as file:
            return cls(file.read())


class KeySchedule(collections.UserList):
    """Represents key schedule."""

    def __init__(self, key):
        """Creates key schedule from key."""
        super().__init__(bytearray(key.data[i::4]) for i in range(4))

        for row_idx in range(4, 4 * (constants.ROUNDS[key.size] + 1)):
            word = utils.next_word(self.data, row_idx, n_words=key.words)
            for column_idx in range(4):
                self.data[column_idx].append(word[column_idx])
