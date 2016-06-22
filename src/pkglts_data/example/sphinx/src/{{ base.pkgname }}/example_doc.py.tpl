""" Module documentation
"""


modattribute = "myvalue"


class MyObj(object):
    """Object documentation
    """

    def __init__(self):
        """Constructor doc
        """
        pass

    def method(self):
        """Method doc
        """
        pass

    def _private_method(self):
        """Private method
        """
        pass

    @staticmethod
    def staticmethod(a):
        """static method doc

        Args:
            a (int): first argument

        Returns:
            (bool) something
        """
        return False


def myfunc(a):
    """Myfunc documentation

    Args:
        a (str): argument doc

    Returns:
        (str)
    """
    return a + "toto"
