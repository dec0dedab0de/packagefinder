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
