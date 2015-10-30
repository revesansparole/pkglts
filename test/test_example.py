from nose import with_setup

from pkglts import example as ex


def setup_module():
    """ Some code executed before launching functions in this module.
    """
    print("setup module")


def teardown_module():
    """ Some code executed after parsing all functions in this module.
    """
    print("teardown module")


def setup_func():
    """ Set up test fixtures.
    """
    print("setup func")


def teardown_func():
    """ Tear down test fixtures.
    """
    print("tear down func")


@with_setup(setup_func, teardown_func)
def test_main():
    """ test ...
    """
    ex.main()


def test_example_func_default_to_beau_texte():
    assert ex.example_func() == "beau texte"


def test_example_func_default_return_given_txt():
    assert ex.example_func("random") == "random"


def test_example_class_creation():
    eg = ex.ExampleClass()
    assert eg.txt() == "texte encore plus beau"


class TestExampleClass(object):
    def __init__(self):
        self.eg = None

    def setup(self):
        """setup called when instance is created."""
        print("setup object")
        self.eg = ex.ExampleClass()

    def teardown(self):
        """function called when instance is destroyed."""
        print("teardown object")
        self.eg = None

    def test_method(self):
        print("test method")
        assert self.eg.txt() == "texte encore plus beau"
