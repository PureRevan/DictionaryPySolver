from utils import DICT_PATH, next_link
from queue import Queue

"""
A quite fast approach using Nodes, also known as a "Trie"
It still generally is just about 1-2 seconds slower than the frequency_search
"""


class Node:
    def __init__(self, word: str):
        if not word:
            self.next = {}
            self.is_word = True
        else:
            self.next = {word[0]: Node(word[1:])}
            self.is_word = False

    def update(self, word: str):
        if not word:
            self.is_word = True
            return

        try:
            self.next[word[0]].update(word[1:])
        except KeyError:
            self.next.update({word[0]: Node(word[1:])})


class Root(Node):
    def __init__(self, dict_path: str = DICT_PATH):
        super().__init__("")

        with open(dict_path, "r") as file:
            for line in file.read().split():
                self.update(line)

    def contains(self, word: str):
        cdict: Node = self

        for char in word:
            try:
                cdict = cdict.next[char]
            except KeyError:
                return False

        return cdict.is_word

    def search(self, matrix: list[list[str]]) -> int:
        q = Queue()

        row_bounds = len(matrix)
        col_bounds = len(matrix[0])
        longest = ()

        for i, row in enumerate(matrix):
            for j, char in enumerate(row):
                try:
                    q.put((self.next[char], [(i, j)]))
                except KeyError:
                    continue

        while not q.empty():
            next_node, visited = q.get()

            for i, j in next_link(*visited[-1], col_bounds=col_bounds, row_bounds=row_bounds, already_visited=visited):
                if len(visited) > len(longest):
                    longest = visited

                try:
                    q.put((next_node.next[matrix[i][j]], visited + [(i, j)]))
                except KeyError:
                    pass

        return longest


if __name__ == '__main__':
    from test import create_root, root_contains, root_search

    root = create_root()

    root_contains(root)
    root_search(root)

