#!/usr/bin/env python

import os
from os import path
import contextlib
import pip
from pip import get_installed_distributions
import sys
from cStringIO import StringIO
from ast import parse, Import, ImportFrom


@contextlib.contextmanager
def capture():
    """for capturing stdout,  stolen from http://stackoverflow.com/a/10743550"""
    
    
    oldout,olderr = sys.stdout, sys.stderr
    try:
        out=[StringIO(), StringIO()]
        sys.stdout,sys.stderr = out
        yield out
    finally:
        sys.stdout,sys.stderr = oldout, olderr
        out[0] = out[0].getvalue()
        out[1] = out[1].getvalue()


def get_top_levels():
    '''returns a dict with the keys from all of the top_level.txt entries, and the freeze name as the value'''
    output = {}

    for d in get_installed_distributions():
        freeze_name = '=='.join(str(d).split())
        top_level = path.join(d.egg_info, 'top_level.txt')
        if path.exists(top_level):
            with open(top_level) as f:
                a = f.read()
            for line in a.splitlines():
                output[line.strip()] = freeze_name
    return output



def get_freeze():
    with capture() as out:
        pip.main(['freeze'])
    if not out[1]:
        return out[0].splitlines()

def get_py_files(project_path = None):
    if not project_path:
        project_path = os.getcwd()
    project_path = os.path.join(os.getcwd(), project_path)

    for current_directory, directory_names, file_names in os.walk(project_path):
        for file_name in file_names:
            if file_name.split('.')[-1] == 'py':
                yield os.path.join(current_directory,file_name) 



def get_imported_modules(py_file):
    """Takes a python file and yields all the modules imoprted
    currently swallows all parsing errors, such as invalid syntax. """
    with open(py_file) as f:
        text = f.read()
    try:
        tree = parse(text,filename = 'parseerrors.txt')
        for c in tree.body:
            if type(c) == Import:
                for alias in c.names:
                    yield alias.name
            elif type(c) == ImportFrom:
                if c.module != None:
                    yield c.module
    except:
        pass  #put specific parsing errors here

def get_imported_top_levels(project_path):
    """takes a path, yields all the top level modules that are imported in all the python files"""
    imported_top_levels = set()
    for py_file in get_py_files(project_path):
        this_itl = set(module.split('.')[0] for module in get_imported_modules(py_file))
        new = this_itl.difference(imported_top_levels)
        imported_top_levels.update(new)
        for itl in new:
            yield itl

def make_freeze(project_path):
    tld = get_top_levels()
    for itl in get_imported_top_levels(project_path):

        if tld.get(itl):
            yield tld.get(itl)
def freeze(project_path):
    for r in make_freeze(project_path):
        print(r)
def main():
    freeze(project_path = None)


if __name__ == '__main__':
    main()