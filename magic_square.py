"""Magic Square Module"""
from copy import deepcopy

import numpy as np

from random import randint

START_VALUE = 1
DEFAULT_OPS_AMOUNT = 5


def create_square(size: int) -> np.ndarray:
    """
    Create Magic Square of odd, even or doubly even order based on size argument

    :param size: Order of Magic Square
    :return: Magic Square as numpy 2D array
    """
    # Adjust size to acceptable value
    while True:
        if size < 3:
            pass
        elif size % 2 != 0:
            return create_odd_square(size)
        elif size % 4 == 0:
            return create_double_even_square(size)
        size += 1


def create_odd_square(size: int) -> np.ndarray:
    """
    Create Magic Square of odd order using Siamese method

    :param size: Order of Magic Square
    :return: Magic Square as numpy 2D array
    """
    # Only magic squares of odd order
    while size <= 2 or size % 2 == 0:
        size += 1

    # Create empty square
    square = np.zeros(shape=(size, size), dtype=int)

    # Count - counts values put in Magic Square
    # Row & col - cursor to array value
    count, row, col = 1, 0, size // 2

    # Cycle ends after every value is set
    while count <= size ** 2:
        if square[row, col] == 0:
            # Set the 'count' value and increase count
            square[row, col] = count
            count += 1
            # Move cursor to right and top
            row = (row - 1) % size
            col = (col + 1) % size
        else:
            # Return cursor at last position + move cursor down
            row = (row + 2) % size
            col = (col - 1) % size

    return square


def create_double_even_square(size: int) -> np.ndarray:
    """
    Create Magic Square of doubly even order using Generic pattern

    :param size: Order of Magic Square
    :return: Magic Square as numpy 2D array
    """
    # Only magic squares of double even order
    while size % 4 != 0:
        size += 1

    # Starting value
    start = 1
    # Ending value
    stop = start + size ** 2

    # Create array with elements in a sequence
    square = np.arange(start=start, stop=stop, dtype=int)
    square = square.reshape((size, size))

    # Create array with elements in a reverse sequence
    reverse_square = np.arange(start=stop - 1, stop=start - 1, step=-1, dtype=int)
    reverse_square = reverse_square.reshape((size, size))

    # Get amount of quarters (4x4) in one row
    quarters = size // 4

    # Traverse through every quarter of square
    for qrt_row in range(quarters):
        for qrt_col in range(quarters):
            # Get row and column indexes for this quarter
            first_row, first_col = qrt_row * 4, qrt_col * 4
            last_row, last_col = first_row + 3, first_col + 3
            # Change x elements from square to x elements from reverse square
            # [ ] [x] [x] [ ]
            # [x] [ ] [ ] [x]
            # [x] [ ] [ ] [x]
            # [ ] [x] [x] [ ]
            for i in (1, 2):
                square[first_row, first_col + i] = \
                    reverse_square[first_row, first_col + i]
                square[last_row, first_col + i] = \
                    reverse_square[last_row, first_col + i]
                square[first_row + i, first_col] = \
                    reverse_square[first_row + i, first_col]
                square[first_row + i, last_col] = \
                    reverse_square[first_row + i, last_col]

    return square


def create_even_square(size: int) -> np.ndarray:
    """
    Create Magic Square of even order using Narayana-De la Hire's method

    :param size: Order of Magic Square
    :return: Magic Square as numpy 2D array
    """
    # Only magic squares of even order
    while size % 2 != 0:
        size += 1
    # Create empty squares, their alphabets and replacement dictionary
    square_a = np.full(fill_value=-1, shape=(size, size), dtype=int)
    square_b = np.zeros_like(square_a)
    alphabet_a = range(0, size**2, size)
    alphabet_b = range(1, size + 1)
    replace = dict([(alphabet_a[i], alphabet_b[i]) for i in range(size)])

    # Fill main and skew diagonals
    for i in range(size):
        square_a[i, i] = alphabet_a[i]
        square_a[size - i - 1, i] = alphabet_a[i]

    # Fill empty places
    # The rule is that every alphabet symbol
    # can occur only in the column with the opposite symbol n // 2 times
    for i in range(size):
        symbol, reverse_symbol = alphabet_a[i], alphabet_a[size - i - 1]
        for col in (i, size - i - 1):
            for row in range(size):
                if np.count_nonzero(square_a[:, col] == symbol) != size // 2 and \
                        symbol not in square_a[row, :] and \
                        square_a[row, col] == -1:
                    square_a[row, col] = symbol
                    continue

    # Fill second square based on counterclockwise rotated first square
    # square_a = np.rot90(square_a)
    for symbol_a, symbol_b in replace.items():
        square_b[square_a == symbol_a] = symbol_b
    square_b = np.rot90(square_b)

    # Resulting square is sum of both squares values
    return square_a + square_b


def transform_magic_square(
        square: np.ndarray,
        amount: int = DEFAULT_OPS_AMOUNT
) -> np.ndarray:
    """
    Randomly transform Magic Square rows and columns

    If passed amount of transformations is < 0,
    then amount of operations is equal to order of the square

    :param square: 2D NxN numpy array
    :param amount: Amount of transformation operations (default = 5)
    :return: Transformed Magic Square
    """
    # Check if given array is magic square
    if not check_square_magic(square):
        return square

    square = deepcopy(square)
    order = square.shape[0]

    if amount < 0:
        amount = order

    # Operations 3 and 4 cannot be performed for squares of even order or order 3!
    operations = 2 if order == 3 or (order % 4 != 0 and order % 2 == 0) else 4

    for _ in range(amount):
        # Randomly get operation number
        operation = randint(0, operations)

        # Rotate square counterclockwise
        if operation == 0:
            square = np.rot90(square, axes=(0, 1))

        # Rotate square clockwise
        elif operation == 1:
            square = np.rot90(square, axes=(1, 0))

        # Swap row i and its opposite, column i and its opposite
        # For (0 <= i <= order - 1)
        elif operation == 2:
            i = randint(0, order - 1)
            i_op = order - i - 1
            square[i, :], square[i_op, :] = square[i_op, :], square[i, :].copy()
            square[:, i], square[:, i_op] = square[:, i_op], square[:, i].copy()

        # Operation 3 - swap rows i, j and their opposites
        # Operation 4 - swap columns i, j and their opposites
        # For i, j in (i < j < (order - 2) // 2)
        elif operation in (3, 4):
            # For squares of order 4 and 5, i and j can take only one possible value
            if order in (4, 5):
                i, j = 0, 1
            else:
                i = randint(0, order // 4)
                j = randint(i + 1, (order - 2) // 2)

            # i, j opposite values
            i_op, j_op = order - i - 1, order - j - 1

            # Swap rows i, j and their opposites
            if operation == 3:
                square[i, :], square[j, :] = \
                    square[j, :], square[i, :].copy()
                square[i_op, :], square[j_op, :] = \
                    square[j_op, :], square[i_op, :].copy()

            # Swap columns i, j and their opposites
            elif operation == 4:
                square[:, i], square[:, j] = \
                    square[:, j], square[:, i].copy()
                square[:, i_op], square[:, j_op] = \
                    square[:, j_op],  square[:, i_op].copy()

    return square


def check_square_magic(square: np.ndarray) -> bool:
    """
    Check magic properties of the square

    :param square: 2D NxN numpy array
    :return: Boolean result
    """
    # Check square has NxN shape
    # if not isinstance(square, np.ndarray) or square.shape[0] != square.shape[1]:
    if square.shape[0] != square.shape[1]:
        return False

    # Square order
    order = square.shape[0]

    # Magic constant
    # Magic square's rows, cols and diagonals sums must be equal to magic constant
    magic_const = order * (order ** 2 + 1) // 2

    # Main diagonals sum
    lr_diagonal_sum = 0
    rl_diagonal_sum = 0

    for i in range(order):
        # Check row sum
        if sum(square[i, :]) != magic_const:
            return False
        # Check col sum
        if sum(square[:, i]) != magic_const:
            return False
        # Sum diagonal values
        lr_diagonal_sum += square[i, i]
        rl_diagonal_sum += square[i, order - i - 1]

    # Check diagonal sums
    if sum(np.diag(square)) != magic_const:
        return False
    if sum(np.diag(np.fliplr(square))) != magic_const:
        return False

    return True


def check_magic_square_symmetry(square: np.ndarray) -> bool:
    """
    Check symmetry properties of the Magic Square

    :param square: 2D NxN numpy array
    :return: Boolean result
    """
    # Check square has NxN shape
    if square.shape[0] != square.shape[1]:
        return False

    # Square order
    order = square.shape[0]

    # Sum of two equidistant values must be equal to this value
    sum_const = order ** 2 + 1

    # Cyclic traversal of first half of rows and columns
    for row in range(order // 2):
        for col in range(order // 2):
            # Check sum of equidistant values
            if square[row, col] + square[order - row - 1, order - col - 1] != sum_const:
                return False

    return True
