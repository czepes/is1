"""Cipher Module"""

import numpy as np

from math import sqrt, ceil
from magic_square import create_square, transform_magic_square

NO_SYMBOL = '_'
DELIMITER = '\''


def encrypt(
        text: str,
        transform: bool = False,
        empty: str = NO_SYMBOL,
        delimiter: str = DELIMITER
) -> tuple[str, str]:
    """
    Encrypts text using Magic Squares
    :param text: Text to encrypt
    :param transform: Flag to enable Magic Square's random transformations
    :param empty: Symbol that represents absence of symbol (default = '_')
    :param delimiter: Delimiter for values of key (default = '/')
    :return: Key and ciphertext
    """
    text_len = len(text)
    layout = create_square(ceil(sqrt(text_len)))

    # Magic square transformation
    if transform:
        layout = transform_magic_square(layout)

    # Reducing unnecessary 2D
    layout = layout.flatten()

    # Encryption
    ciphertext = np.full(shape=layout.size, fill_value='', dtype=str)
    for i in range(layout.size):
        if layout[i] <= text_len:
            ciphertext[i] = text[layout[i] - 1]
        else:
            ciphertext[i] = empty

    # Convert to string
    key = delimiter.join([str(i) for i in layout])

    return key, ''.join(ciphertext)


def decrypt(
        text: str,
        key: str,
        empty: str = NO_SYMBOL,
        delimiter: str = DELIMITER
) -> tuple[bool, str]:
    """
    Decrypts text using Magic Square's encryption key
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
        ).flatten()
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
    for i in range(layout.size):
        plaintext[layout[i] - 1] = text[i]

    return True, ''.join(plaintext).replace(empty, '')
