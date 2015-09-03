requirementsfinder
==================

A simple script to show requirements that are actually being imported.
Essentially the same thing as "pip freeze" but minus all those package you
installed and forgot about.

============
Installation
============

You probably shouldn't right now, but if you really want to, you can use pip, but it's not on pypi yet::

    pip install git+https://github.com/dec0dedab0de/requirementsfinder.git

=====
Usage
=====

Running requirements finder will give the same out put as pip freeze, but
only with packages in use in the current directory (recursively)::

    myprompt$ requirementsfinder
    pip==6.1.1
    Flask==0.10.1
    requests==2.7.0


You can also specify a path::

    myprompt$ requirementsfinder example/
    Flask==0.10.1
    requests==2.7.0

==================
Gotchas, and TODOS
==================

- Will currently ignore any packages it can't find
    - should at least warn that these imports couldn't find a package
- There is some very specific data that it is currently ignoring, but I forget what it is.
- Can not specify a specific virtualenv
- Probably only works on python 2.7
- Relies heavily on pip
    - add support for packages installed by yum
    - add support for packages installed by apt
    - figure out other ways people install packages
- Only works with .py files in a directory
    - maybe allow specifying a single file, or list of files, or list of paths
    - it would be nice to handle other filetypes, like ipynb, or others.
- Add an option to specify a depth for recurssing directories.

===========
Wacky Ideas
===========

- Run a test script, and slowly build up imports based on failures.
- scour github, and bitbucket, or a list of package locations for stuff not in pypi
- build other install scripts besides requirements.txt