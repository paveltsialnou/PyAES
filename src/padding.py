"""
Functions that helps working with padding similar to bit padding as
described in
https://en.wikipedia.org/wiki/Padding_(cryptography)#Bit_padding.
"""

import functools
import pathlib


@functools.singledispatch
def add(data, size):
    """Adds padding."""
    raise NotImplementedError()


@add.register(bytearray)
def _(data, size):
    data += b'\x01'
    data += b'\x00' * (size - len(data) % size)


@add.register(pathlib.Path)
def _(file_path, size):
    with open(file_path, 'ab') as file:
        file.write(b'\x01')
        file.write(b'\x00' * (size - file.tell() % size))


@functools.singledispatch
def remove(data):
    """Removes padding."""
    raise NotImplementedError()


@remove.register(bytearray)
def _(data):
    while not data.pop():
        continue


@remove.register(pathlib.Path)
def _(file_path):
    with open(file_path, 'ab+') as file:
        file.seek(-1, 1)
        while file.read(1) != b'\x01':
            file.seek(-2, 1)

        file.truncate(file.tell() - 1)
