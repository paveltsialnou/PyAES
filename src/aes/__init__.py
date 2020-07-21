"""AES decrypt/encrypt functions."""

from aes import constants
from aes import steps


def decrypt(state, key):
    """Decrypts state."""
    rounds = constants.ROUNDS[key.size]
    steps.add_round_key(state, key.schedule, current_round=rounds)

    for current_round in range(rounds - 1, 0, -1):
        steps.shift_rows(state, inverse=True)
        steps.sub_bytes(state, inverse=True)
        steps.add_round_key(state, key.schedule, current_round=current_round)
        steps.mix_columns(state, inverse=True)

    steps.shift_rows(state, inverse=True)
    steps.sub_bytes(state, inverse=True)
    steps.add_round_key(state, key.schedule, current_round=0)


def encrypt(state, key):
    """Encrypts state."""
    rounds = constants.ROUNDS[key.size]

    steps.add_round_key(state, key.schedule, current_round=0)

    for current_round in range(1, rounds):
        steps.sub_bytes(state)
        steps.shift_rows(state)
        steps.mix_columns(state)
        steps.add_round_key(state, key.schedule, current_round=current_round)

    steps.sub_bytes(state)
    steps.shift_rows(state)
    steps.add_round_key(state, key.schedule, current_round=rounds)


__all__ = ('decrypt', 'encrypt')
