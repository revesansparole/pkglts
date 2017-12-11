============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

{% if 'github' is available or 'gitlab' is available %}
You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at issues_.

If you are reporting a bug, please include:

  * Your operating system name and version.
  * Any details about your local setup that might be helpful in troubleshooting.
  * Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the {% if 'github' is available %}GitHub{% elif 'gitlab' is available %}Gitlab{% endif %} issues for bugs.
Anything tagged with "bug" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the {% if 'github' is available %}GitHub{% elif 'gitlab' is available %}Gitlab{% endif %} issues for
features. Anything tagged with "feature" is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

**{{ base.pkg_full_name }}** could always use more documentation, whether as
part of the official **{{ base.pkg_full_name }}** docs, in docstrings, or even
on the web in blog posts, articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at issues_.

If you are proposing a feature:

  * Explain in detail how it would work.
  * Keep the scope as narrow as possible, to make it easier to implement.
  * Remember that this is a volunteer-driven project, and that contributions
    are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `{{ base.pkgname }}` for local
development.

1. Fork the `{{ base.pkgname }}` repo on {% if 'github' is available %}GitHub{% elif 'gitlab' is available %}
{{ gitlab.server }}{% endif %}.
2. Clone your fork locally::

    {% if 'github' is available %}$ git clone git@github.com:your_name_here/{{ base.pkgname }}.git
    {% elif 'gitlab' is available %}$ git clone git@{{ gitlab.server }}:your_name_here/{{ base.pkgname }}.git
    {% endif %}
3. Install your local copy into a virtualenv. Assuming you have virtualenv_
installed, this is how you set up your fork for local development::

    $ virtualenv dvlpt
    $ dvlpt/script/activate
    (dvlpt)$ python setup.py develop

4. Create a branch for local development (wip stands for work in progress)::

    (dvlpt)$ git checkout -b wip_name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass flake8 and the
tests, including testing other Python versions with tox::

    (dvlpt)$ cd {{ base.pkgname }}
    (dvlpt) {{ base.pkgname }}$ flake8
    {% if 'test' is available -%}
    (dvlpt) {{ base.pkgname }}$ {% if test.suite_name == 'nose' %}nosetests{% else %}pytest{% endif %}
    {% endif %}
    (dvlpt) {{ base.pkgname }}$ tox

   To get flake8 and tox, just pip install them into your virtualenv.

6. Commit your changes and push your branch to {% if 'github' is available %}GitHub
{% elif 'gitlab' is available %}Gitlab{% endif %}::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin wip_name-of-your-bugfix-or-feature

7. Submit a pull request through the {% if 'github' is available %}GitHub{% elif 'gitlab' is available %}Gitlab{% endif %} website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

  1. The pull request should include tests.
  2. If the pull request adds functionality, the docs should be updated. Put
     your new functionality into a function with a docstring, and add the
     feature to the list in README.rst.
{%- if 'pysetup' is available %}
  3. The pull request should work for Python {{ pysetup.intended_versions|join(", ") }}.
     {% if 'github' is available -%}
     Check `Travis <https://travis-ci.org/{{ github.owner }}/{{ github.project }}/pull_requests>`_
     and make sure that the tests pass for all supported Python versions.
     {% endif %}
{% endif %}
Tips
----

{% if 'test' is available %}
To run a subset of tests::
{% if test.suite_name == 'nose' %}
    $ nosetests test/test_XXX
{% else %}
    $ pytest test/test_XXX
{% endif %}

{% endif %}
{% if 'github' is available %}
.. _issues: {{ github.url }}/issues
{% elif  'gitlab' is available %}
.. _issues: {{ gitlab.url }}/issues
{% endif %}
.. _virtualenv: https://pypi.python.org/pypi/virtualenv
{% endif %}