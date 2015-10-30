""" Examples of plugins definitions
"""


def sub_myfunc(a, b):
    """ Simply add both arguments together
    """
    res = a + b
    return res

sub_myfunc.__plugin__ = 'oa.sub.core'


def sub_cli_service():
    """ Example of a command ligne script
    """
    import sys
    print "sub ARGV", sys.argv

sub_cli_service.__plugin__ = 'console_scripts'
