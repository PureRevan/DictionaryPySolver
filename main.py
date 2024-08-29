from utils import load_len_sorted_dictionary_freq_map, scan_string_to_matrix, visualize_matrix_with_path
from utils import matrix_pprint, find_valid_dimensions, pick_dimensions, timed, InvalidInputError
from frequency_search import frequency_path_search_validating

"""
Performs a loop asking the user to manually input the matrix as a string and guesses the dimensions such that they
are as close as possible to perfect ones (e.g. 7x7, 8x8, 9x9, ... -> n x n)

It then solves it using frequency_path_search_validating and also displays a visual representation of the solution
"""


def main():
    preloaded_dict = load_len_sorted_dictionary_freq_map()

    while True:
        inpt = ""
        while not inpt:
            try:
                inpt = input("Matrix: ").lower()

                if not (inpt.isascii() and inpt.isalpha()):
                    raise InvalidInputError("Only alphabetical ASCII characters allowed (english alphabet)")

                valid_dims = find_valid_dimensions(inpt)
                if valid_dims:
                    inpt = scan_string_to_matrix(inpt, pick_dimensions(valid_dims))
                    break

                raise InvalidInputError("No valid dimensions found")
            except InvalidInputError as e:
                print(f"Invalid input: {e}")
                inpt = []

        matrix_pprint(inpt)
        print("\n")

        word, path = timed(frequency_path_search_validating)(inpt[::-1], preloaded_dict,
                                                             pre_loaded_is_len_sorted_desc=True)
        print(f"Longest found word: {word}")

        visualize_matrix_with_path(inpt[::-1], path, word=word)


if __name__ == '__main__':
    main()
