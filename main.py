from __future__ import annotations

import unittest


class Node:
    """
    Class for Node of the Prefix Tree Class
    Holding the value for the node (letter) and pointers to subsequent children
    """

    def __init__(self, letter: str):
        self._letter = letter
        self._is_word_end = False
        self._children = {}

    def add_child(self, letter: str):
        # only if no such child exists, otherwise could override existing value
        if letter not in self._children.keys():
            self._children[letter] = Node(letter)

    def get_child(self, letter: str) -> Node:
        if letter not in self._children.keys():
            raise ValueError("No such letter in children!!!")
        return self._children[letter]

    def set_word_end(self):
        self._is_word_end = True

    def set_word_end_false(self):
        self._is_word_end = False

    def is_word_end(self) -> bool:
        return self._is_word_end


# make sure that word is from the alphabet
def isalpha(word: str):
    return word.isalpha()


def is_input_of_alphabet(func):
    def wrapper(*kwds):
        if not isalpha(kwds[1]):
            raise ValueError("The Input Must Be Alphabetic!")
        res = func(*kwds)
        return res

    return wrapper


class PrefixTree:
    """
    Class for the Prefix Tree
    Holding the root, and implementing all functionalities (insert, contains)
    """

    def __init__(self):
        self.root = Node(letter='')

    @is_input_of_alphabet
    def insert(self, word: str):
        current_node = self.root
        # iterating the word _letter-by-_letter
        for i, letter in enumerate(word):
            # add child to current node
            current_node.add_child(letter)
            # continue iterating the next node
            current_node = current_node.get_child(letter)
        current_node.set_word_end()

    @is_input_of_alphabet
    def contains(self, word: str) -> bool:
        current_node = self.root
        # iterating the word _letter-by-_letter
        for letter in word:
            try:
                current_node = current_node.get_child(letter)
            # There isn't a path containing these subsequent letters
            except ValueError:
                return False

        # if went over all the _letter, then such path exists from root to child
        # return True only if it is a leaf node, otherwise False
        if current_node.is_word_end():
            return True
        return False

    @is_input_of_alphabet
    def remove(self, word: str):
        current_node = self.root
        # iterating the word _letter-by-_letter
        for i, letter in enumerate(word):
            try:
                # get the child of current node
                current_node = current_node.get_child(letter)
            except ValueError:
                return False
        current_node.set_word_end_false()


class TestTree(unittest.TestCase):

    def test_insert_and_contains(self):
        prefix_tree = PrefixTree()
        prefix_tree.insert('a')
        prefix_tree.insert('abc')
        prefix_tree.insert('abcd')
        self.assertTrue(prefix_tree.contains("a"))
        self.assertFalse(prefix_tree.contains("ab"))
        self.assertTrue(prefix_tree.contains("abc"))
        self.assertTrue(prefix_tree.contains("abcd"))
        self.assertFalse(prefix_tree.contains("abba"))

    def test_empty(self):
        prefix_tree = PrefixTree()
        self.assertFalse(prefix_tree.contains("where"))
        self.assertFalse(prefix_tree.contains("homework"))

    def test_alphabetic_only(self):
        prefix_tree = PrefixTree()
        with self.assertRaises(ValueError):
            prefix_tree.insert("where!!")
        with self.assertRaises(ValueError):
            prefix_tree.insert("homework@@")


if __name__ == '__main__':
    unittest.main()
