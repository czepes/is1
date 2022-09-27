"""Cipher Module"""

import numpy as np

from math import sqrt, ceil
from magic_square import create_square

NO_SYMBOL = '_'
DELIMITER = '/'


def encrypt(
        text: str,
        empty: str = NO_SYMBOL,
        delimiter: str = DELIMITER
) -> tuple[str, str]:
    """
    Encrypts text
    :param text: Text to encrypt
    :param empty: Symbol that represents absence of symbol (default = '_')
    :param delimiter: Delimiter for values of key (default = '/')
    :return: Key and ciphertext
    """
    # 1D encryption
    text_len = len(text)
    layout = create_square(ceil(sqrt(text_len))).flatten()
    cipher = np.full(shape=layout.size, fill_value='', dtype=str)

    for i in range(layout.size):
        if layout[i] <= text_len:
            cipher[i] = text[layout[i] - 1]
        else:
            cipher[i] = empty

    # Convert to string
    key = delimiter.join([str(i) for i in layout])

    return key, ''.join(cipher)


def decrypt(
        text: str,
        key: str,
        empty: str = NO_SYMBOL,
        delimiter: str = DELIMITER
) -> tuple[bool, str]:
    """
    Encrypts text
    :param text: Text to decrypt
    :param key: Decryption key
    :param empty: Symbol that represents absence of symbol (default = '_')
    :param delimiter: Delimiter for values of key (default = '/')
    :return: Operation status, plaintext or error message
    """
    # Check key is str and not empty
    if key is None or len(key) == 0:
        return False, "Wrong key length"

    # Try to convert key to numpy array
    try:
        # Convert from string
        layout = np.array(
            [int(i) for i in key.split(delimiter)],
            dtype=int
        )
    except ValueError:
        return False, "Wrong key format"

    # Check that array has an even number of elements
    if isinstance(sqrt(layout.size), int):
        return False, "Wrong key shape"

    # Check that text and array has the same amount of elements
    if len(text) != layout.size:
        return False, "Wrong key size"

    # Check that array consists of a sequence
    if len(np.unique(layout)) != layout.size:
        return False, "Wrong key contents"

    # Decryption
    plaintext = np.full(shape=layout.size, fill_value='', dtype=str)
    layout = layout.flatten()
    for i in range(layout.size):
        plaintext[layout[i] - 1] = text[i]
    plaintext = ''.join(plaintext).replace(empty, '')
    return True, plaintext
