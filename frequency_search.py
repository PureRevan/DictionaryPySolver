from queue import Queue
from collections import Counter

from utils import load_words_dictionary_as_freq_map, load_dictionary_freq_map_len_limited, sort_freq_map, next_link


"""
Includes 3 implementations of a search utilizing the collections.Counter object as a frequency map for comparisons
This is generally the fastest approach out of all available in these files

All 3 require a matrix of characters and support a preloaded frequency map. Otherwise they load one automatically.

frequency_search simply outputs the longest word, which can be formed taking characters from the matrix in any order and from any position
It also supports both a sorted and unsorted frequency map, while former generally outperforms the latter, even if for the sorting is accounted

frequency_search_validating also outputs just the longest word but takes characters from the matrix following certain rules.
Those rules are: 
    From any starting character you may only take characters exactly 1 space away from your current character.
    This translates to shifting the current indices in the matrix (i, j) either both or only one of those by +1 or -1
    The implementation of generating the next indices, also based on the already visited ones, is the utils.next_link function
It also no longer supports unsorted searches due to them being largely inferior to sorted ones, such that it even 
overshadows the time it takes to sort an unsorted dictionary

frequency_path_search_validating functions just like the above frequency_search_validating but it also returns the path taken
in index notation. For instance, the matrix [['s'], ['e'], ['e']] produces the output ('see', ((0, 0), (1, 0), (2, 0)))

"""


def frequency_search(matrix: list[list[str]], pre_loaded_freq_map: list[tuple[Counter, str]] = None,
                     pre_loaded_is_len_sorted_desc: bool = False, ignores_len_loading_optimizations: bool = False,
                     max_freq_map_len: int = 34, force_unsorted_search: bool = False) -> str:
    """
    :param matrix: Matrix consisting of only characters
    :param pre_loaded_freq_map: Frequency map of available words, if one is already loaded (otherwise one will be loaded)
    :param pre_loaded_is_len_sorted_desc: Whether the preloaded map (if even passed as an argument) is sorted by length
    :param ignores_len_loading_optimizations: If False it does not load words into the frequency map (if it is loaded) that are longer than the flattened matrix (and therefore cant be formed)
    :param max_freq_map_len: Length of the longest word in the frequency map
    :param force_unsorted_search: Unsorted search will be used instead of sorting the freq_map first (which normally is more efficient according to testing)
    :return: The longest word that can be formed (in the case of a tie, a basically random word with that length)
    """

    def unsorted_freq_search(freq_map: list[tuple[Counter, str]], available_chars: Counter) -> str:
        longest = ""
        for freq in freq_map:
            if all(freq[0][char] <= available_chars[char] for char in freq[0]):
                if len(freq[1]) > len(longest):
                    longest = freq[1]

        return longest

    def sorted_frequency_search(freq_map: list[tuple[Counter, str]], available_chars: Counter) -> str:
        for freq in freq_map:
            if all(freq[0][char] <= available_chars[char] for char in freq[0]):
                return freq[1]
        return ""

    chars = Counter(char for row in matrix for char in row)

    if pre_loaded_freq_map:
        if pre_loaded_is_len_sorted_desc:
            return sorted_frequency_search(pre_loaded_freq_map, chars)
        elif not force_unsorted_search:
            return sorted_frequency_search(sort_freq_map(pre_loaded_freq_map), chars)
        return unsorted_freq_search(pre_loaded_freq_map, chars)

    # Max len of a word in the current dictionary file is 34
    freq_map = load_words_dictionary_as_freq_map() if ignores_len_loading_optimizations or chars.total() >= max_freq_map_len \
        else load_dictionary_freq_map_len_limited(chars.total())

    return unsorted_freq_search(freq_map, chars) if force_unsorted_search \
        else sorted_frequency_search(sort_freq_map(freq_map), chars)


def frequency_search_validating(matrix: list[list[str]], pre_loaded_freq_map: list[tuple[Counter, str]] = None,
                                pre_loaded_is_len_sorted_desc: bool = False,
                                ignores_len_loading_optimizations: bool = False,
                                max_freq_map_len: int = 34) -> str:
    """
    :param matrix: Matrix consisting of only characters
    :param pre_loaded_freq_map: Frequency map of available words, if one is already loaded (otherwise one will be loaded)
    :param pre_loaded_is_len_sorted_desc: Whether the preloaded map (if even passed as an argument) is sorted by length
    :param ignores_len_loading_optimizations: If False it does not load words into the frequency map (if it is loaded) that are longer than the flattened matrix (and therefore cant be formed)
    :param max_freq_map_len: Length of the longest word in the frequency map
    :return: The longest word that can be formed (in the case of a tie, a basically random word with that length) including character position validation
    """

    if not matrix:
        return ""
    elif len(matrix) == 1 and len(matrix[0]) == 1:
        return (matrix[0][0] if Counter(matrix[0][0]) in [freq[0] for freq in pre_loaded_freq_map if freq[0].total() == 1]
                else "")

    def can_form_word(word: str) -> bool:
        q = Queue()

        row_bounds, col_bounds = len(matrix), len(matrix[0])

        # Starting values
        for i, row in enumerate(matrix):
            for j, char in enumerate(row):
                if char == word[0]:
                    q.put((i, j, 0, ((i, j),)))

        while not q.empty():
            i, j, w_idx, visited = q.get()
            w_idx += 1

            for pi, pj in next_link(i, j, row_bounds, col_bounds, visited):
                if matrix[pi][pj] == word[w_idx]:
                    if w_idx + 1 == len(word):
                        return True
                    q.put((pi, pj, w_idx, visited + ((pi, pj),)))

        return False

    def sorted_frequency_search(_freq_map: list[tuple[Counter, str]], available_chars: Counter) -> str:
        for freq in _freq_map:
            if all(freq[0][char] <= available_chars[char] for char in freq[0]) and can_form_word(freq[1]):
                return freq[1]
        return ""

    chars = Counter(char for row in matrix for char in row)

    if pre_loaded_freq_map:
        return sorted_frequency_search(pre_loaded_freq_map if pre_loaded_is_len_sorted_desc
                                       else sort_freq_map(pre_loaded_freq_map), chars)

    # Max len of a word in the current dictionary file is 34
    freq_map = load_words_dictionary_as_freq_map() if ignores_len_loading_optimizations or chars.total() >= max_freq_map_len \
        else load_dictionary_freq_map_len_limited(chars.total())

    return sorted_frequency_search(sort_freq_map(freq_map), chars)


def frequency_path_search_validating(matrix: list[list[str]], pre_loaded_freq_map: list[tuple[Counter, str]] = None,
                                     pre_loaded_is_len_sorted_desc: bool = False,
                                     ignores_len_loading_optimizations: bool = False,
                                     max_freq_map_len: int = 34):
    """
    :param matrix: Matrix consisting of only characters
    :param pre_loaded_freq_map: Frequency map of available words, if one is already loaded (otherwise one will be loaded)
    :param pre_loaded_is_len_sorted_desc: Whether the preloaded map (if even passed as an argument) is sorted by length
    :param ignores_len_loading_optimizations: If False it does not load words into the frequency map (if it is loaded) that are longer than the flattened matrix (and therefore cant be formed)
    :param max_freq_map_len: Length of the longest word in the frequency map
    :return: The longest word that can be formed (in the case of a tie, a basically random word with that length) including character position validation
    """

    if not matrix:
        return "", tuple()
    elif len(matrix) == 1 and len(matrix[0]) == 1:
        return (matrix[0][0], ((0, 0),)) if Counter(matrix[0][0]) in [freq[0] for freq in pre_loaded_freq_map if freq[0].total() == 1]\
            else ("", tuple())

    def can_form_word(word: str) -> tuple[int]:
        q = Queue()

        row_bounds, col_bounds = len(matrix), len(matrix[0])

        # Starting values
        for i, row in enumerate(matrix):
            for j, char in enumerate(row):
                if char == word[0]:
                    q.put((i, j, 0, ((i, j),)))

        while not q.empty():
            i, j, w_idx, visited = q.get()
            w_idx += 1

            for pi, pj in next_link(i, j, row_bounds, col_bounds, visited):
                if matrix[pi][pj] == word[w_idx]:
                    if w_idx + 1 == len(word):
                        return visited + ((pi, pj),)
                    q.put((pi, pj, w_idx, visited + ((pi, pj),)))

        return tuple()

    def sorted_frequency_search(_freq_map: list[tuple[Counter, str]], available_chars: Counter):

        for freq in _freq_map:
            if all(freq[0][char] <= available_chars[char] for char in freq[0]):
                formed_via = can_form_word(freq[1])
                if formed_via:
                    return freq[1], formed_via
        return "", tuple()

    chars = Counter(char for row in matrix for char in row)

    if pre_loaded_freq_map:
        return sorted_frequency_search(pre_loaded_freq_map if pre_loaded_is_len_sorted_desc
                                       else sort_freq_map(pre_loaded_freq_map), chars)

    # Max len of a word in the current dictionary file is 34
    freq_map = load_words_dictionary_as_freq_map() if ignores_len_loading_optimizations or chars.total() >= max_freq_map_len \
        else load_dictionary_freq_map_len_limited(chars.total())

    return sorted_frequency_search(sort_freq_map(freq_map), chars)
