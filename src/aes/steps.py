"""AES methods."""

from aes import utils


def add_round_key(state, key_schedule, *, current_round):
    """The AddRoundKey step."""
    start, stop = 4 * current_round, 4 * (current_round + 1)

    for row_idx, row in enumerate(state):
        state[row_idx] = utils.xor_vectors(
            row,
            key_schedule[row_idx][start:stop]
        )


def mix_columns(state, *, inverse=False):
    """The MixColumns step."""
    for column_idx, column in enumerate(zip(*state)):
        new_column = utils.galois_mul(column, inverse=inverse)
        for row_idx, elem in enumerate(new_column):
            state[row_idx][column_idx] = elem


def shift_rows(state, *, inverse=False):
    """The ShiftRows step."""
    for row_idx, row in enumerate(state):
        state[row_idx] = utils.rot_word(row, inverse=inverse, times=row_idx)


def sub_bytes(state, *, inverse=False):
    """The SubBytes step."""
    for row_idx, row in enumerate(state):
        state[row_idx] = utils.sub_word(row, inverse=inverse)
