Register on Github
==================

First step, you need to create yourself an account on GitHub_.

.. _GitHub: https://github.com/

In the following I will assume that you now have a login and that you are logged on.

Personal package
----------------

On your personal web page 'https://github.com/your_login_here', on the 'repository'
tab there is a button 'New'.

.. image:: github_new_repo.png

Click it and enter the name of the project (same name used when adding the 'github'
option, you can always edit the option again to change it if you want).

You can leave the description blank and we suggest to keep it public.

Don't initialize this repository with a README since we already have one to commit.
Leave the 'add .gitignore' and 'add license' to None. And just click 'create repository'.

.. image:: github_create_repo.png

Felicitations, you just created the package on GitHub. Take a mental note of the
url they provide since it will be used later.

.. image:: github_remote_url.png

To populate it you'll need to use the 'git' tool as explained briefly in `Quick Git Tutorial`_.

Organization package
--------------------

May mess up with current information storage

.. warning:: TODO


Quick Git Tutorial
------------------

If you are not familiar with Git, now is the time to read some tutorials_. The
following will assume you have a basic understanding of Git and will just explained
what needs to be done to first push your package on the newly created project.

In the root directory of your project::

    $ git init
    $ git status

If you have added the github option already and regenerated the package, a '.gitignore'
has been created so the 'status' command should not show any temporary files like
'build', '.coverage', '.tox' for example. Therefore you can safely add all::

    $ git add --all

and make your first commit::

    $ git commit -m"initial commit :)"

You then need to create a remote to push your code on the github repository::

    $ git remote add origin url_provided_on_github

The url to provide is the one provided once you successfully created your project.

.. image:: github_remote_url.png

Now you can push your local copy on the master branch on github::

    $ git push --set-upstream origin master

You'll be prompted for your github credential and upon success you can check on
the github page of your project that there is some sources.

Git usage
---------

The github option is responsible for maintaining a proper '.gitignore'. Therefore
you can safely assume that no unwanted files will be covered when you 'add --all'
which makes one life easier to add new modules in a package.

.. _tutorials: https://fr.atlassian.com/git/
