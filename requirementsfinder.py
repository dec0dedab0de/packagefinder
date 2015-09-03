#!/usr/bin/env python
"""A simple script for showing requirements actually in use in the same format as pip freeze"""
import os
from os import path
from pip import get_installed_distributions
from ast import parse, Import, ImportFrom
import argparse

def get_top_levels():
    '''returns a dict with the keys from all of the top_level.txt entries, and the freeze name as the value'''
    #if we make a class this could be a cached property
    output = {}

    for d in get_installed_distributions():
        freeze_name = '=='.join(str(d).split())
        if d.egg_info:
            top_level = path.join(d.egg_info, 'top_level.txt')
            if path.exists(top_level):
                with open(top_level) as f:
                    a = f.read()
                for line in a.splitlines():
                    output[line.strip()] = freeze_name
    return output

def get_py_files(project_path, depth = None, *args, **kwargs):
    """
    Takes a path, yields a list of py files in that path.

    :param project_path: path to start at
    :return: a list of paths to python files
    """
    if os.path.isfile(project_path) and project_path.split('.')[-1] == 'py':
        yield project_path
    else:
        for current_directory, directory_names, file_names in os.walk(project_path):
            if not depth or (depth and path_distance(project_path, current_directory) <= depth):
                for file_name in file_names:
                    if file_name.split('.')[-1] == 'py':
                        yield os.path.join(current_directory,file_name)

def get_imported_modules(py_file):
    """Takes a python file and yields all the modules imoprted
    currently swallows all parsing errors, such as invalid syntax. """
    with open(py_file) as f:
        text = f.read()
    try:
        tree = parse(text)
        for c in tree.body:
            if type(c) == Import:
                for alias in c.names:
                    yield alias.name
            elif type(c) == ImportFrom:
                if c.module != None:
                    yield c.module
    except:
        pass  #put specific parsing errors here

def get_imported_top_levels(project_path,*args, **kwargs):
    """takes a path, yields all the top level modules that are imported in all the python files"""
    imported_top_levels = set()
    for py_file in get_py_files(project_path,*args, **kwargs):
        this_itl = set(module.split('.')[0] for module in get_imported_modules(py_file))
        new = this_itl.difference(imported_top_levels)
        imported_top_levels.update(new)
        for itl in new:
            yield itl

def make_freeze(project_path, *args, **kwargs):
    tld = get_top_levels()
    for itl in get_imported_top_levels(project_path,*args, **kwargs):

        if tld.get(itl):
            yield tld.get(itl)
def freeze(project_path, *args, **kwargs):
    for r in make_freeze(project_path, *args, **kwargs):
        print(r)

def path_distance(path1, path2):
    """takes 2 paths, returns the difference between them.
    raises an error if the first one isn't a parent of the second
    I think there should be a more pythonic way of doing this. """

    path1list = [a for a in path1.split(os.path.sep) if a]
    path2list = [a for a in path2.split(os.path.sep) if a]
    for i, directory in enumerate(path1list):
        if path2list[i] != directory:
            raise Exception('{0} is not a parent of {1}'.format(path1,path2))
    return len(path2list) - len(path1list)

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("project_path",
                        type=DirectoryOrPyFile,
                        nargs='?',
                        default=os.getcwd(),
                        help="path of python project or file, defaults to current path ")
    parser.add_argument("-v", "--virtualenv",
                        type = str,
                        help="specify virtualenv, (not implemented yet)")
    parser.add_argument("-d", "--depth",
                        type = int,
                        help="How many levels deep to recurse 0 is 1 path")
    args = parser.parse_args()
    return vars(args)
class DirectoryOrPyFile(str):
    def __new__(self, content):
        project_path = os.path.join(os.getcwd(), content)
        if os.path.isdir(project_path) or (os.path.isfile(project_path) and project_path.split('.')[-1] == 'py'):
            return str.__new__(self, project_path)
        else:
            raise ValueError('{0} is not a valid path'.format(project_path))
def main():
    args = get_arguments()
    freeze(**args)



if __name__ == '__main__':
    main()