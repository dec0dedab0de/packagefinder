requirementsfinder
==================

A simple script to show requirements that are actually in use, in the same format as pip --freeze

============
Installation
============

You probably shouldn't right now, but if you must,
create a symlink in your path to requirementsfinder.py and mark it as executable::
    sudo ln -s /usr/bin/requirementsfinder /path/to/requirementsfinder.py
    sudo chmod +x /usr/bin/requirementsfinder

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

* Will currently ignore any packages it can't find
    * should atleast warn that these imports couldn't find a package
* There is some very specific data that it is currently ignoring, but I forget what it is.
* Can not specify a specific virtualenv
* Probably only works on python 2.7
* Relies heavily on pip
    * add support for packages installed by yum
    * add support for packages installed by apt
    * figure out other ways people install packages
* Only works with .py files in a directory
    * maybe allow specifying a single file, or list of files, or list of paths
    * it would be nice to handle other filetypes, like ipynb, or others.
* Add an option to specify a depth for recurssing directories.

===========
Wacky Ideas
===========

* Run a test script, and slowly build up imports based on failures.
* scour github, and bitbucket, or a list of package locations for stuff not in pypi
* build other install scripts besides requirements.txt