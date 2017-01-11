import os
import cson
import pkgutil
from importlib import import_module


def recursive_import(package):
    """ Recursive import python package
    """
    for importer, modname, is_pkg in pkgutil.iter_modules(package.__path__):
        sub_package = import_module('%s.%s' % (package.__package__ or package.__name__, modname))
        if is_pkg:
            recursive_import(sub_package)
