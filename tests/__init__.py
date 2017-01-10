import os
import cson
import pathlib
from collections import OrderedDict

from parser import init
from parser.utility import load_cson

init(False, False)
tests_data_path = os.path.realpath(os.path.join(__file__, '..', 'data'))


def get_test_cases(dir_name):
    unit_test_cases = dict()
    path_obj = pathlib.Path(os.path.join(tests_data_path, dir_name))
    for cson_file in path_obj.iterdir():
        if cson_file.name.endswith('.cson'):
            test_cases = load_cson(str(cson_file))
            unit_test_cases[str(cson_file)] = test_cases or []
    return unit_test_cases


def show_object(ast, title=None):
    if title:
        print('%s%s %s %s' % (os.linesep, '-' * 50, title, os.linesep))
    _ast = ast.cson() if hasattr(ast, 'cson') else cson.dumps(ast, indent=4)
    print('        ' + _ast.replace('\n', '\n        '))


def show_difference(sql, source, target, _type, difference):
    print('%s------------ SQL: %s%s' % (os.linesep, '-' * 60, os.linesep))
    print(sql)
    show_object(source, '[%s]' % _type)
    show_object(target, '[tc] ')
    if difference:
        source_diff, target_diff = difference
        if source_diff is not target_diff:
            show_object(source_diff, 'diff [%s]' % _type)
            show_object(target_diff, 'diff [tc]')


def show_error(sql, message):
    print('%s    sql: %s%s' % (os.linesep, '-' * 60, os.linesep))
    print(sql)
    print('%s  error: %s%s' % (os.linesep, '-' * 60, os.linesep))
    print(message)


def clear_empty_item(dictionary, need_clear_items):
    for item in need_clear_items:
        if item in dictionary and dictionary[item] in (None, '', [], {}):
            dictionary.pop(item)


def check_consistency(source, target, ignores=None, can_ellipsis=False):
    if type(source) in (int, float, str, bool):
        if source != target:
            return source, target
        return
    elif type(source) in (list, tuple) and type(target) in (list, tuple):
        return check_consistency_list(source, target, ignores)
    elif type(source) in (dict, OrderedDict) and type(target) in (dict, OrderedDict):
        source, target = dict(source), dict(target)
        return check_consistency_dict(source, target, ignores, can_ellipsis=can_ellipsis)
    elif source is target:
        return
    return source, target


def check_consistency_list(source, target, ignores=None):
    source_index = 0
    for target_index in range(0, len(target)):
        if source_index == len(source):
            # source complete traverse, but target not end
            if target[target_index] == '...' and target_index == len(target) - 1:
                return  # although target not complete traverse, but only the ellipsis.
            else:
                return source, target
        target_item = target[target_index]
        source_item = source[source_index]
        if target_item != '...':
            difference = check_consistency(source_item, target_item, ignores)
            if difference:
                return difference
            source_index += 1
        else:
            if target_index == len(target) - 1:
                return  # omit the ending

            target_next = target[target_index + 1]
            while source_index < len(source):
                if source_item == target_next:      # 'list', 'tuple', 'dict' also support '=='
                    break
                else:
                    source_index += 1
                    if source_index == len(source):
                        return source, target       # source complete traverse, but target not end
                    source_item = source[source_index]
            if source_item != target_next:
                return source, target
    # target complete traverse, but source not end
    if source_index < len(source):
        return source, target


def check_consistency_dict(source, target, ignores=None, can_ellipsis=False):
    if (not source and target) or (not target and source):
        return source, target
    if ignores:
        for ignore in ignores:
            source.pop(ignore, None)
            target.pop(ignore, None)
    allow_empty_items = ('groups', 'limits', 'highlights', 'conditions', 'scores', 'orders', 'alias', 'object', 'range')
    clear_empty_item(source, allow_empty_items)
    clear_empty_item(target, allow_empty_items)
    if can_ellipsis:
        for key in source.keys():
            if key not in target:
                source.pop(key)
    allow_omit = '...' in target    # omit some definition
    source_keys = source.keys()
    target_keys = target.keys()
    if not allow_omit:
        if set(source_keys).symmetric_difference(set(target_keys)):
            return source, target
    for source_key, source_value in source.items():
        if allow_omit and source_key not in target:
            continue
        difference = check_consistency(source_value, target[source_key], ignores)
        if difference:
            return difference
