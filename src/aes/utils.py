"""Helper utils."""

from aes import constants


def _xtime(number):
    """Base multiplication function."""
    if number >> 7:
        result = (number << 1) ^ 0x1B
    else:
        result = number << 1

    return result % 0x100


def _mul_by_03(number):
    """Helper function to multiply number by 0x03."""
    return _xtime(number) ^ number


def _mul_by_09(number):
    """Helper function to multiply number by 0x09."""
    return _xtime(_xtime(_xtime(number))) ^ number


def _mul_by_0b(number):
    """Helper function to multiply number by 0x0B."""
    return _xtime(_xtime(_xtime(number))) ^ _xtime(number) ^ number


def _mul_by_0d(number):
    """Helper function to multiply number by 0x0D."""
    return _xtime(_xtime(_xtime(number))) ^ _xtime(_xtime(number)) ^ number


def _mul_by_0e(number):
    """Helper function to multiply number by 0x0E."""
    return _xtime(_xtime(_xtime(number))) ^ _xtime(_xtime(number)) ^ _xtime(
        number)


_MUL_OPS_MAPPING = {
    0x01: lambda number: number,
    0x02: _xtime,
    0x03: _mul_by_03,
    0x09: _mul_by_09,
    0x0B: _mul_by_0b,
    0x0D: _mul_by_0d,
    0x0E: _mul_by_0e
}


def galois_mul(vector, *, inverse=False):
    """Multiplies matrix by vector in Galois Field (256)."""
    if inverse:
        matrix = constants.INVERSE_MIX_COLUMNS
    else:
        matrix = constants.FORWARD_MIX_COLUMNS

    result = []

    for row in matrix:
        number = 0x00
        for elem, multiplier in zip(vector, row):
            number ^= _MUL_OPS_MAPPING[multiplier](elem)
        result.append(number)

    return result


def next_word(words, idx, *, n_words):
    """Returns next word for key expansion."""
    if not idx % n_words:
        vectors = (
            [word[idx - n_words] for word in words],
            sub_word(rot_word([word[idx - 1] for word in words])),
            [r[idx // n_words - 1] for r in constants.RCON],
        )
    elif n_words > 6 and idx % n_words == 4:
        vectors = (
            [word[idx - n_words] for word in words],
            sub_word([word[idx - 1] for word in words]),
        )
    else:
        vectors = (
            [word[idx - n_words] for word in words],
            [word[idx - 1] for word in words],
        )
    return xor_vectors(*vectors)


def rot_word(word, *, inverse=False, times=1):
    """Helper function to rotate the word."""
    if inverse:
        direction = -1
    else:
        direction = 1

    split = times * direction
    return [*word[split:], *word[:split]]


def sub_word(word, *, inverse=False):
    """Helper function to substitute bytes in the word."""
    if inverse:
        sbox = constants.INVERSE_SBOX
    else:
        sbox = constants.FORWARD_SBOX

    return [sbox[b] for b in word]


def xor_vectors(*vectors):
    """Helper function to xor vectors."""
    if not vectors:
        return []

    result = vectors[0]
    for vector in vectors[1:]:
        result = [e1 ^ e2 for e1, e2 in zip(result, vector)]

    return result
