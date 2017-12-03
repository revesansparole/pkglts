Register on Coveralls.io
========================

As always, you need to register on Coveralls_io_. This process is made easy since
you can used you GitHub_ id to sign up.

You must arrive on the main page of Coveralls_io_ with a small set of instructions
to add a repository.

Add your project
----------------

Registering a project is easy and you just need to click on the 'add repos' button.

.. image:: coveralls_main_page.png

You must see a list of repositories you collaborate with. If yours is not visible
maybe hit the 're-sync repos' button (you may also have to refresh your browser
at some point to see the changes).

.. image:: coveralls_add_repo_list.png

Flip the switch for your project and click on the details button.

Coveralls_io_ use Travis-CI_ to gather information on your project, so you need
to trigger a new build if you want to see some result, either::

    $ git push

or manually click the rebuild button on Travis-CI_. After the build has finished
and coveralls had time to gather information, if you refresh the 'coveralls' web
page you must see the statistics on your code.

.. image:: coveralls_report.png

Final remark
------------

If everything is successful, you must now have a coverage-100% green badge that
show on top of your readme in the homepage of your project on github (hit refresh
if you see nothing, you may also have to click on the badge urls button on landscape).

If you want more statistics you can always look at the details of the latest build
on landscape but they are mostly the same information available with a local
call to 'coverage' :)


.. _Coveralls_io: https://coveralls.io/
.. _GitHub: https://github.com/
.. _Travis-CI: http://travis-ci.org/

