""" Example module to uni-test, see test/test_example
"""

import os


def example_func(txt="beau texte"):
    """Print txt message and return it.
    """
    print(txt)

    return txt


class ExampleClass(object):
    """Example class to show typical behaviour.
    """

    def __init__(self):
        self._txt = "texte encore plus beau"

    def txt(self):
        return self._txt


def main():
    ex = ExampleClass()
    print(ex.txt())
    print(os.getcwd())
