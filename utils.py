import typing
from timeit import default_timer
from functools import wraps
from string import ascii_lowercase
from collections import Counter
import random
import matplotlib.pyplot as plt


"""
Utility functions
"""


DICT_PATH = "./dictionary.txt"


def set_dict_path(new_path: str) -> None:
    global DICT_PATH

    DICT_PATH = new_path


def timed(f: typing.Callable):
    """
    :param f: Callable to be timed
    :return: Returns a wrapper around f printing the time it took to execute f
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        start = default_timer()
        _res = f(*args, **kwargs)
        print(f"{f.__name__} took {default_timer() - start}s")
        return _res

    return wrapper


def gen_random_char() -> str:
    """
    :return: Returns a random lowercase ASCII character
    """
    return random.choice(ascii_lowercase)


def gen_random_char_matrix(row_size: int = None, col_size: int = None):
    """
    :param row_size: Row size (= len(matrix)
    :param col_size: Column size (= len(matrix[i]) for any i within bounds)
    :return: Returns a matrix with the given dimensions containing only random characters
    """
    return [[gen_random_char() for _ in range(col_size)] for _ in range(row_size)]


def gen_random_dimensions(lower_bound: int, upper_bound: int, n: int = 2) -> tuple[int, ...]:
    """
    :param lower_bound: Lower bound for the dimensions
    :param upper_bound: Upper bound for the dimensions
    :param n: The dimensionality. For instance, n = 2 -> (r1, r2); n = 5 -> (r1, r2, r3, r4, r5)
    :return: A tuple containing randomly generated dimensions
    """
    return tuple(random.randint(lower_bound, upper_bound) for _ in range(n))


def load_words_dictionary() -> set:
    global DICT_PATH

    with open(DICT_PATH, "r") as file:
        content = set(file.read().split())
    return content


def load_words_dictionary_as_freq_map() -> list[tuple[Counter, str]]:
    global DICT_PATH

    with open(DICT_PATH, "r") as file:
        content = [(Counter(word), word) for word in file.read().split()]
    return content


def load_len_sorted_dictionary_freq_map() -> list[tuple[Counter, str]]:
    return sorted(load_words_dictionary_as_freq_map(), key=lambda t: len(t[1]), reverse=True)


def load_dictionary_freq_map_len_limited(len_limit: int, ) -> list[tuple[Counter, str]]:
    global DICT_PATH

    with open(DICT_PATH, "r") as file:
        content = [(Counter(word), word) for word in file.read().split() if len(word) <= len_limit]
    return content


def get_max_len_from_freq_map(freq_map: list[tuple[Counter, str]]):
    return max(freq[0].total() for freq in freq_map)


def sort_freq_map(freq_map: list[tuple[Counter, str]]) -> list[tuple[Counter, str]]:
    return sorted(freq_map, key=lambda t: len(t[1]), reverse=True)


def matrix_pprint(matrix: list[list[str]]) -> None:
    for i, row in enumerate(matrix):
        if i == 0:
            print(f"[{row}")
        elif i == len(matrix) - 1:
            print(f" {row}]")
        else:
            print(f" {row}")


def shift_index_path(path: tuple[tuple[int, int], ...]) -> tuple[tuple[int, int], ...]:
    return tuple((i + 1, j + 1) for i, j in path)


def visualize_matrix_with_path(matrix: list[list[str]], path: list[tuple[int, int], ...], linewidth: int = 10,
                               alpha: float = 0.25,
                               color: str = "green", start_color: str = "red", starting_thickness: int = 250,
                               start_alpha: float = 0.8, word: str = "", forces_on_foreground: bool = True):
    fig, ax = plt.subplots()
    for i, row in enumerate(matrix):
        for j, char in enumerate(row):
            ax.text(j, i, char, ha='center', va='center')

    x_coords, y_coords = zip(*path)
    
    ax.plot(y_coords, x_coords, color=color, linewidth=linewidth, alpha=alpha)
    ax.scatter(y_coords[0], x_coords[0], color=start_color, s=starting_thickness, alpha=start_alpha)

    ax.set_xticks(range(len(matrix[0])))
    ax.set_yticks(range(len(matrix)))
    ax.set_xticklabels(range(len(matrix[0])))
    ax.set_yticklabels(range(len(matrix)))

    ax.set_xlabel('Column')
    ax.set_ylabel('Row')
    ax.set_title(word)

    plt.grid(False)
    
    if forces_on_foreground:
        fig.canvas.manager.window.attributes('-topmost', 1)
    
    plt.show()


def scan_string_to_matrix(s: str, dim: tuple[int, int]) -> list[list[str]]:
    return [[s[i * dim[1] + j] for j in range(dim[1])] for i in range(dim[0])]


def find_valid_dimensions(s: str) -> list[tuple[int, int]]:
    string_length = len(s)
    possible_dimensions = []

    for rows in range(1, string_length + 1):
        if string_length % rows == 0:
            columns = string_length // rows
            possible_dimensions.append((rows, columns))

    return possible_dimensions


def pick_dimensions(valid_dimensions: list[tuple[int, int]]):
    closest_to_perfect = min(valid_dimensions, key=lambda dim: abs(dim[0] - dim[1]))
    return closest_to_perfect


def reconstruct_word_from_path(matrix: list[list[str]], path: tuple[tuple[int, int]]) -> str:
    return "".join([matrix[i][j] for i, j in path])


def next_link(row_idx: int, col_idx: int, row_bounds: int, col_bounds: int,
              already_visited: typing.Iterable[tuple[int, int]] = None) -> list[tuple[int, int]]:
    """
    :param row_idx: Current element row index
    :param col_idx: Current element column index
    :param row_bounds: Upper row bounds (=len(matrix))
    :param col_bounds: Upper column bounds (=len(matrix[0]))
    :param already_visited: A list containing tuples containing every index combination already visited as (i, j)
    :return: The indices for all possible characters that could be visited next
    """
    if already_visited is None:
        already_visited = []
    return [(i, j) for i in (row_idx, row_idx + 1, row_idx - 1) for j in (col_idx, col_idx + 1, col_idx - 1)
            if (i != row_idx or j != col_idx)
            and -1 < i < row_bounds
            and -1 < j < col_bounds
            and (i, j) not in already_visited]


class InvalidInputError(Exception):
    pass

