"""Setup script."""

import sys

from distutils import core


if sys.version_info < (3, 8):
    sys.exit('Sorry, only Python >= 3.8 is supported.')

core.setup(
    name='aes',
    version='0.1',
    description='Python AES implementation and Utility',
    author='Pavel Tsialnou',
    author_email='paveltsialnou@icloud.com',
    url='https://github.com/paveltsialnou/PyAES',
    packages=['pyaes', 'pyaes.aes', 'pyaes.tool'],
    package_dir={
        'pyaes': 'src/', 'pyaes.aes': 'src/aes/', 'pyaes.tool': 'src/tool/'},
)
