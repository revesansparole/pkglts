""" Examples of plugins definitions
"""


def myfunc(a, b):
    """ Simply add both arguments together
    """
    res = a + b
    return res

myfunc.__plugin__ = 'oa.core'


def cli_service():
    """ Example of a command ligne script
    """
    import sys
    print "ARGV", sys.argv

cli_service.__plugin__ = 'console_scripts'


class MyPlugin(object):
    __plugin__ = 'oa.core'

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __call__(self):
        res = self.a + self.b
        return res
