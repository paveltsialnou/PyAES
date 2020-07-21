"""AES errors."""


class AESError(BaseException):
    """Base class for AES errors."""


class KeySizeError(AESError):
    """Key size is wrong error."""


class StateSizeError(AESError):
    """State size is wring error."""
