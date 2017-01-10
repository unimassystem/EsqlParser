from parser import Processor
from tests import get_test_cases, tests_data_path, check_consistency, show_difference


def test_cases():
    use_case_group = get_test_cases('ast_dsl')
    print()
    for case_file, use_case in use_case_group.items():
        print('    ' + case_file[len(tests_data_path) + 1:] + ' ...')
        if not use_case:
            continue
        for sql, _tc in use_case.items():
            if 'dsl' not in _tc:
                continue
            source = Processor.execute(sql)
            target = _tc['dsl']
            difference = check_consistency(source, target)
            if difference:
                show_difference(sql, source, target, 'dsl', difference)
                assert False
