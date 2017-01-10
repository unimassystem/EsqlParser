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


def load_cson(file_path, prefix=os.curdir):
    if prefix:
        file_path = os.path.join(prefix, file_path)
    if not os.path.exists(file_path):
        raise Exception('cson file [%s] not exists.', file_path)
    f = open(file_path, 'r', encoding='utf-8')
    data = cson.load(f)
    f.close()
    return data
