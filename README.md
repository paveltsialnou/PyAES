# Pure Python AES realisation (with CLI) ![][0]

### Installation
```shell script
$ python setup.py install
```
### Available commands
##### Generate key file (by default creates 128-bit key)
```shell script
$ python -m pyaes.tool generate test.key
```
###### Using key size option
```shell script
$ python -m pyaes.tool generate -s 128 test.128.key
$ python -m pyaes.tool generate -s 192 test.192.key
$ python -m pyaes.tool generate -s 256 test.256.key
```
##### Encrypt file
```shell script
$ md5 test.file
MD5 (test.file) = 13a943bcb5a61cd5b8ecd3163dce1191
$ python -m pyaes.tool encrypt test.file test.key
$ md5 test.file
MD5 (test.file) = 5b44db80ee253a0f881ec0c5dc9ab9d5
```
##### Decrypt file
```shell script
$ md5 test.file
MD5 (test.file) = 5b44db80ee253a0f881ec0c5dc9ab9d5
$ python -m pyaes.tool decrypt test.file test.key
$ md5 test.file
MD5 (test.file) = 13a943bcb5a61cd5b8ecd3163dce1191
```
### Used materials
  * [AES on Wikipedia][1]
  * [FIPS PUB 197][2]

[0]: https://github.com/paveltsialnou/PyAES/workflows/CI/badge.svg?branch=master
[1]: https://en.wikipedia.org/wiki/Advanced_Encryption_Standard
[2]: https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.197.pdf