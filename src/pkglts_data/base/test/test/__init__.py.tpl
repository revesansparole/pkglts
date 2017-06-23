{% if 'test' is available %}
{% if test.suite_name == 'nose' %}
def setup_package():
    """Some code executed once when test are loaded.
    """
    print("setup package")


def teardown_package():
    """Some code executed once after tests have been played.
    """
    print("teardown")
{% endif %}
{% endif %}