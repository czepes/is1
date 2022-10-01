"""Cipher Module"""

import numpy as np

from math import sqrt, ceil
from random import randint
from magic_square import create_square, transform_magic_square

NO_SYMBOL = '_'
DELIMITER = '\''
DEFAULT_TRANSFORMATIONS = 0
MIN_BITS = 4


def encrypt(
        text: str,
        transformations: int = DEFAULT_TRANSFORMATIONS,
        empty: str = NO_SYMBOL,
        delimiter: str = DELIMITER
) -> tuple[str, str]:
    """
    Encrypt text using Magic Squares

    :param text: Text to encrypt
    :param transformations: Amount of transformations (default = 0)
    :param empty: Symbol that represents absence of symbol (default = '_')
    :param delimiter: Delimiter for values of key (default = '/')
    :return: Key and ciphertext
    """
    text_len = len(text)

    # Magic square creation & transformation
    layout = transform_magic_square(
        create_square(ceil(sqrt(text_len))),
        transformations
    )

    # Reducing unnecessary 2D
    layout = layout.flatten()

    # Encryption
    ciphertext = np.full(shape=layout.size, fill_value='', dtype=str)
    for i in range(layout.size):
        if layout[i] <= text_len:
            ciphertext[i] = text[layout[i] - 1]
        else:
            ciphertext[i] = empty

    # Convert to binary
    # Adjust bits for binary values
    max_val = np.amax(layout)
    bits = MIN_BITS
    while max_val >= 2 ** bits:
        bits *= 2

    # Create key
    key = ''.join([f"{i:0{bits}b}" for i in layout])
    # Add bits to the key
    key = f"{bits:b}{delimiter}{key}"

    return key, ''.join(ciphertext)


def decrypt(
        text: str,
        key: str,
        empty: str = NO_SYMBOL,
        delimiter: str = DELIMITER
) -> tuple[bool, str]:
    """
    Decrypt text using encryption key

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
        # Convert from binary
        bits, key = key.split(delimiter)
        bits = int(bits, 2)
        layout = np.array(
            [int(key[i:i + bits], 2) for i in range(0, len(key), bits)],
            dtype=int
        )
    except ValueError:
        return False, "Wrong key format"

    # Check converted layout
    status, message = check_layout(layout, text)
    if not status:
        return status, message

    # Decryption
    plaintext = np.full(shape=layout.size, fill_value='', dtype=str)
    for i in range(layout.size):
        plaintext[layout[i] - 1] = text[i]

    return True, ''.join(plaintext).replace(empty, '')


def encrypt_enhanced(
        text: str,
        transformations: int = DEFAULT_TRANSFORMATIONS,
        empty: str = NO_SYMBOL,
        delimiter: str = DELIMITER
) -> tuple[str, str]:
    """
    Encrypt text using Magic Squares, performs a modulo 2 additions with an offset

    :param text: Text to encrypt
    :param transformations: Amount of transformations (default = 0)
    :param empty: Symbol that represents absence of symbol (default = '_')
    :param delimiter: Delimiter for values of key (default = '/')
    :return: Key and ciphertext
    """
    text_len = len(text)

    # Magic square creation & transformation
    layout = transform_magic_square(
        create_square(ceil(sqrt(text_len))),
        transformations
    )

    # Reducing unnecessary 2D
    layout = layout.flatten()

    # Encryption

    # Additional encryption step
    offset = randint(0, layout.shape[0])
    # Make sure that offset won't make extra 'empty' characters in ciphertext
    unchecked = True
    while unchecked:
        for i in range(len(text)):
            # if ord(text[i]) ^ layout[i] ^ offset == ord(empty):
            # if ord(text[i]) ^ offset == ord(empty):
            if ord(text[i]) ^ layout[i] == ord(empty):
                # offset += 1
                empty = chr(ord(empty) + 1)
                break
        else:
            unchecked = False
    ciphertext = np.full(shape=layout.size, fill_value='', dtype=str)
    for i in range(layout.size):
        if layout[i] <= text_len:
            # Additional encryption using XOR with magic square and offset
            ciphertext[i] = \
                chr(ord(text[layout[i] - 1]) ^ offset)
        else:
            ciphertext[i] = empty

    # Convert to binary
    # Adjust bits for binary values
    max_val = np.amax(layout)
    bits = MIN_BITS
    while max_val >= 2 ** bits:
        bits *= 2

    # Create key
    key = ''.join([f"{i:0{bits}b}" for i in layout])
    # Add binary values length to the key
    key = f"{bits:b}{delimiter}{offset:b}{delimiter}{key}"
    # key = f"{bits:b}{delimiter}{offset:b}{delimiter}{key}"

    return key, ''.join(ciphertext)


def decrypt_enhanced(
        text: str,
        key: str,
        empty: str = NO_SYMBOL,
        delimiter: str = DELIMITER
) -> tuple[bool, str]:
    """
    Decrypt text using enhanced encryption key

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
        # Convert from binary
        bits, offset, key = key.split(delimiter)
        offset = int(offset, 2)
        bits = int(bits, 2)
        layout = np.array(
            [int(key[i:i + bits], 2) for i in range(0, len(key), bits)],
            dtype=int
        )
    except ValueError:
        return False, "Wrong key format"

    # Check converted layout
    status, message = check_layout(layout, text)
    if not status:
        return status, message

    # Decryption
    plaintext = np.full(shape=layout.size, fill_value='', dtype=str)
    for i in range(layout.size):
        plaintext[layout[i] - 1] = \
            chr(ord(text[i]) ^ offset) if text[i] != empty else ''

    return True, ''.join(plaintext)


def check_layout(layout: np.ndarray, text: str) -> tuple[bool, str]:
    """
    Check layout properties before decryption

    :param layout: Magic Square layout
    :param text: Text to decrypt
    :return: Check status, check message
    """
    # Check that array has an even number of elements
    if isinstance(sqrt(layout.size), int):
        return False, "Wrong key shape"

    # Check that text and array has the same amount of elements
    if len(text) != layout.size:
        return False, "Wrong key size"

    # Check that array consists of a sequence
    if len(np.unique(layout)) != layout.size:
        return False, "Wrong key contents"

    return True, "The key is right"
