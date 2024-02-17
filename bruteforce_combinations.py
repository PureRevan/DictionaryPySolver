from queue import Queue
from utils import next_link


"""
An extremely slow bruteforce approach
"""


def get_combinations(matrix: list[list[str]]) -> dict:
    """ Note: This performs extremely poorly for larger input matrices
    :param matrix: Matrix
    :return: All combinations in a nested tree like structure
    """
    starting = {(char, (i, j), ((i, j),)): {} for i, row in enumerate(matrix) for j, char in enumerate(row)}
    queue = Queue()
    queue.put(starting)

    row_bounds = len(matrix)
    col_bounds = len(matrix[0])

    while not queue.empty():
        current_element = queue.get()
        to_be_queued = []

        for (char, (row_idx, col_idx), used_indices), continuations in current_element.items():
            new_elements = {(matrix[i][j], (i, j), used_indices + ((i, j),)): {}
                            for i, j in next_link(row_idx, col_idx, row_bounds, col_bounds, used_indices)}

            if new_elements:
                continuations.update(new_elements)
                to_be_queued.append(continuations)

        if to_be_queued:
            for item in to_be_queued:
                queue.put(item)

    return starting
