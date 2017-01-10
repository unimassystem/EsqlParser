from parser import parse
from tests import get_test_cases, tests_data_path, check_consistency, show_difference


def test_cases():
    use_case_group = get_test_cases('ast_dsl')
    print()
    for case_file, use_case in use_case_group.items():
        print('    ' + case_file[len(tests_data_path) + 1:] + ' ...')
        if not use_case:
            continue
        for sql, _tc in use_case.items():
            if 'ast' not in _tc:
                continue
            rst = parse(sql)
            source = rst.dict()
            target = _tc['ast']
            difference = check_consistency(source, target)
            if difference:
                show_difference(sql, source, target, 'ast', difference)
                assert False
