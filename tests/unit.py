from tests import check_consistency


def test_check_consistency():
    assert check_consistency({}, []) is not None        # type is not consistent
    assert check_consistency(1, []) is not None         # type is not consistent
    assert check_consistency(1, '1') is not None        # type is not consistent
    assert check_consistency(('1',), '1') is not None   # type is not consistent
    assert check_consistency([{}, 2, [], 4, ('a',)], [{}, 2, [], 4, ('a',)]) is None
    assert check_consistency([{}, 2, [], 4, ('a',)], [{}, 2, '...', ('a',)]) is None            # omit the middle
    assert check_consistency([{}, 2, [], 4, ('a',)], [{}, 2, [], '...', ('a',)]) is None        # omit the middle
    assert check_consistency([{}, 2, [], 4, ('a',)], [{}, 2, [], '...', 4, ('a',)]) is None     # omit the middle
    assert check_consistency([{}, 2, [], 4, ('a',)], ['...', [], 4, ('a',)]) is None            # omit the beginning
    assert check_consistency([{}, 2, [], 4, ('a',)], ['...', 2, [], 4, ('a',)]) is None         # omit the beginning
    assert check_consistency([{}, 2, [], 4, ('a',)], ['...', {}, 2, [], 4, ('a',)]) is None     # omit the beginning
    assert check_consistency([{}, 2, [], 4, ('a',)], [{}, 2, [], '...']) is None                # omit the ending
    assert check_consistency([{}, 2, [], 4, ('a',)], [{}, 2, [], 4, '...']) is None             # omit the ending
    assert check_consistency([{}, 2, [], 4, ('a',)], [{}, 2, [], 4, ('a',), '...']) is None     # omit the ending
    assert check_consistency([{}, 2, [], 4, ('a',), 6, 7, 8], ['...', [], 4, ('a',), '...', 8]) is None  # multiple omit
    assert check_consistency([{}, 2, [], 4, ('a',), 6, 7, 8], [{}, '...', 4, ('a',), '...', 8]) is None  # multiple omit
    assert check_consistency([{}, 2, [], 4, ('a',), 6, 7, 8], [{}, '...', 4, ('a',), '...']) is None     # multiple omit
    assert check_consistency([{}, 2, [], 4, ('a',), 6, 7, 8], ['...', 4, ('a',), '...']) is None         # multiple omit
    assert check_consistency([('a',)], [{}]) is not None            # type is not consistent
    assert check_consistency([1], [{}]) is not None                 # type is not consistent
    assert check_consistency([[]], [3]) is not None                 # type is not consistent
    assert check_consistency([{}, 2, [], 4, ('a',)], [4, ('a',)]) is not None               # lack in beginning
    assert check_consistency([{}, 2, [], 4, ('a',)], [2, [], 4, ('a',)]) is not None        # lack in beginning
    assert check_consistency([{}, 2, [], 4, ('a',)], [3]) is not None                       # lack in both sides
    assert check_consistency([{}, 2, [], 4, ('a',)], [2, [], 4]) is not None                # lack in both sides
    assert check_consistency([{}, 2, [], 4, ('a',)], [{}, 2]) is not None                   # lack in ending
    assert check_consistency([{}, 2, [], 4, ('a',)], [{}, 2, [], 4]) is not None            # lack in ending
    assert check_consistency({'a': {}, 'b': (2,), 'c': []}, {'a': {}, 'c': [], 'b': (2,)}) is None
    assert check_consistency({'a': {}, 'b': (2,), 'c': []}, {'...': True, 'b': (2,)}) is None           # multiple omit
    assert check_consistency({'a': {}, 'b': (2,), 'c': []}, {'c': [], 'b': (2,), '...': True}) is None  # multiple omit
    assert check_consistency({'a': {}, 'b': (2,), 'c': []}, {'a': {}, 'c': []}) is not None     # lack one
    assert check_consistency({'a': {}, 'b': (2,), 'c': []}, {'b': (2,)}) is not None            # lack multiple
    assert check_consistency({'a': {}}, {'a': []}) is not None      # type is not consistent
    assert check_consistency({'a': 2}, {'a': (2,)}) is not None     # type is not consistent
    assert check_consistency({'a': []}, {'a': 1}) is not None       # type is not consistent
