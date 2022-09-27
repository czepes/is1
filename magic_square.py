"""Magic Square Module"""

import numpy as np

START_VALUE = 1


def create_square(size: int, start: int = START_VALUE) -> np.array:
    """
    Creates an odd or doubly even sized magic square based on size argument
    :param: size Edge size of magic square
    :param: start Starting value (default = 1)
    :return: Magic square as numpy 2D array:return:
    """
    while True:
        if size < 3:
            pass
        elif size % 2 != 0:
            return create_siam_square(size, start)
        elif size % 4 == 0:
            return create_doubly_even_square(size, start)
        size += 1


def create_siam_square(size: int, start: int = START_VALUE) -> np.array:
    """
    Creates an odd sized magic square using Siamese method
    :param: size Edge size of magic square
    :param: start Starting value (default = 1)
    :return: Magic square as numpy 2D array
    """
    # Only odd sized magic squares
    while size <= 2 or size % 2 == 0:
        size += 1
    square = np.zeros(shape=(size, size), dtype=int)
    # Count - counts values put in Magic Square
    # Row & col - cursor to array value
    count, row, col = START_VALUE, 0, size // 2
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


def create_doubly_even_square(size: int, start: int = START_VALUE) -> np.array:
    """
    Creates doubly even sized magic squares using Generic pattern
    :param: size Edge size of magic square
    :param: start Starting value (default = 1)
    :return: Magic square as numpy 2D array
    """
    # Only double even sized magic squares
    while size % 4 != 0:
        size += 1
    stop = start + size ** 2
    square = np.arange(start=start, stop=stop, dtype=int)
    square = square.reshape((size, size))
    reverse_square = np.arange(start=stop - 1, stop=start - 1, step=-1, dtype=int)
    reverse_square = reverse_square.reshape((size, size))
    quarters = size // 4
    for quarter_row in range(quarters):
        for quarter_col in range(quarters):
            first_row = quarter_row * 4
            last_row = first_row + 3
            first_col = quarter_col * 4
            last_col = first_col + 3
            for row in range(quarter_row * 4, (quarter_row + 1) * 4):
                for col in range(quarter_col * 4, (quarter_col + 1) * 4):
                    if (row == first_row and col not in (first_col, last_col)) or \
                            (row == last_row and col not in (first_col, last_col)) or \
                            (col == first_col and row not in (first_row, last_row)) or \
                            (col == last_col and row not in (first_row, last_row)):
                        square[row, col] = reverse_square[row, col]
    return square
