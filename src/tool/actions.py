"""Main action functions."""

import secrets

import aes
import padding

from aes import constants
from aes import errors
from aes.key import Key
from aes.state import State


def decrypt(file_path, key):
    """Decrypts data with given key."""
    key = Key.load(key)

    offset = 0
    while True:
        state = State.load(file_path, offset)
        if state is None:
            break

        aes.decrypt(state, key)
        state.dump(file_path, offset)

        offset += 4 * constants.NB

    padding.remove(file_path)


def encrypt(file_path, key_file):
    """Encrypts data with given key."""
    padding.add(file_path, 4 * constants.NB)

    key = Key.load(key_file)

    offset = 0
    while True:
        state = State.load(file_path, offset)
        if state is None:
            break

        aes.encrypt(state, key)
        state.dump(file_path, offset)

        offset += 4 * constants.NB


def generate(key_file, key_size):
    """Generates key for further usage."""
    if key_size not in constants.ALLOWED_KEY_SIZES:
        raise errors.KeySizeError()

    with open(key_file, 'wb') as file:
        file.write(secrets.token_bytes(key_size >> 3))
