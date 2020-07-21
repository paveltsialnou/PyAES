"""Module for testing AES utils."""

import random
import unittest

from unittest import mock

from aes import constants
from aes import utils

import base


class TestAESUtils(base.BaseTestCase):
    """Tests for AES utils."""

    def setUp(self):
        self.input_vectors = (
            [219, 19, 83, 69],
            [242, 10, 34, 92],
            [1, 1, 1, 1],
            [198, 198, 198, 198],
            [212, 212, 212, 213],
            [45, 38, 49, 76]
        )
        self.input_words = [
            [96, 21, 43, 133, 31, 59, 45, 9],
            [61, 202, 115, 125, 53, 97, 152, 20],
            [235, 113, 174, 119, 44, 8, 16, 223],
            [16, 190, 240, 129, 7, 215, 163, 244]
        ]
        self.output_vectors = [
            [142, 77, 161, 188],
            [159, 220, 88, 157],
            [1, 1, 1, 1],
            [198, 198, 198, 198],
            [213, 213, 215, 214],
            [77, 126, 189, 248]
        ]
        self.word = random.choices(range(256), k=4)

    def test_galois_mul(self):
        """Tests multiplication in Galois Field."""
        for vector, expected in zip(self.input_vectors, self.output_vectors):
            with self.subTest(vector=vector):
                self.assertEqual(expected, utils.galois_mul(vector))

    def test_galois_mul_inverse(self):
        """Tests multiplication in Galois Field inverse."""
        for vector, expected in zip(self.output_vectors, self.input_vectors):
            with self.subTest(vector=vector):
                self.assertEqual(
                    expected, utils.galois_mul(vector, inverse=True))

    @mock.patch('aes.utils.xor_vectors')
    def test_next_word(self, xor_vectors_mock):
        """Tests getting next word."""
        for size in constants.ALLOWED_KEY_SIZES:
            idx = 1
            n_words = size >> 5
            words = [word[:n_words] for word in self.input_words]

            with self.subTest(size=size):
                utils.next_word(words, idx, n_words=n_words)

                xor_vectors_mock.assert_called_with(
                    [w[idx] for w in words], [w[idx - 1] for w in words])

    @mock.patch('aes.utils.sub_word')
    @mock.patch('aes.utils.xor_vectors')
    def test_next_word_id_is_dividable_by_n_words(
            self, xor_vectors_mock, sub_word_mock):
        """Tests getting next word for id dividable by key words."""
        sub_word_mock.return_value = 42

        for size in constants.ALLOWED_KEY_SIZES:
            idx = n_words = size >> 5
            words = [word[:n_words] for word in self.input_words]

            with self.subTest(size=size):
                utils.next_word(words, idx, n_words=n_words)

                xor_vectors_mock.assert_called_with(
                    [w[idx - n_words] for w in words],
                    42,
                    [r[idx // n_words - 1] for r in constants.RCON]
                )

    @mock.patch('aes.utils.sub_word')
    @mock.patch('aes.utils.xor_vectors')
    def test_next_word_id_is_4_n_words_8(
            self, xor_vectors_mock, sub_word_mock):
        """Tests getting next word for id=4 and max key size."""
        sub_word_mock.return_value = 42

        idx = 4
        size = max(constants.ALLOWED_KEY_SIZES)
        n_words = size >> 5

        words = [word[:n_words] for word in self.input_words]

        with self.subTest(size=size):
            utils.next_word(words, idx, n_words=n_words)

            xor_vectors_mock.assert_called_with([w[idx] for w in words], 42)

    def test_rot_word(self):
        """Tests rotating word."""
        for times in range(4):
            expected = [*self.word[times:], *self.word[:times]]
            with self.subTest(times=times):
                self.assertEqual(
                    expected, utils.rot_word(self.word, times=times))

    def test_rot_word_inverse(self):
        """Tests rotating word inverse."""
        for times in range(4):
            expected = [*self.word[-times:], *self.word[:-times]]
            with self.subTest(times=times):
                actual = utils.rot_word(self.word, inverse=True, times=times)

                self.assertEqual(expected, actual)

    def test_sub_word(self):
        """Tests substituting word."""
        expected = [constants.FORWARD_SBOX[b] for b in self.word]

        self.assertListEqual(expected, utils.sub_word(self.word))

    def test_sub_word_inverse(self):
        """Tests substituting word inverse."""
        expected = [constants.INVERSE_SBOX[b] for b in self.word]

        self.assertListEqual(expected, utils.sub_word(self.word, inverse=True))

    def test_xor_vectors(self):
        """Tests XORing vectors."""
        vectors = [
            random.choices(range(256), k=4), random.choices(range(256), k=4)]

        self.assertListEqual(
            [e1 ^ e2 for e1, e2 in zip(*vectors)], utils.xor_vectors(*vectors))

    def test_xor_vectors_empty(self):
        """Tests XORing no vectors."""
        self.assertListEqual([], utils.xor_vectors())


if __name__ == '__main__':
    unittest.main()
