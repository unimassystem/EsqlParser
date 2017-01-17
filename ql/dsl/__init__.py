

from ql.parse.ASTNode import Node
from ql.parse.parser import TK


def parse_value(tree: Node) -> str:
    if tree.get_type() == TK.TOK_DOT:
        retval = parse_value(tree.get_child(0))
        retval += '.'
        retval += parse_value(tree.get_child(1))
        return retval
    elif tree.get_type() == TK.TOK_VALUE:
        return tree.get_value()
    else:
        pass


def parse_left_values(tree: Node) -> list:
    retval = []
    for e in tree:
        retval.append(parse_value(e))
    return retval
    

def parse_right_values(tree: Node):
    retval = []
    for e in tree:
        retval.append(parse_value(e))
    return retval


def parse_table_name(tree: Node):
    if tree.get_type() == TK.TOK_DOT:
        _index = parse_value(tree.get_child(0))
        _type = parse_value(tree.get_child(1))
    elif tree.get_type() == TK.TOK_VALUE:
        _index = tree.get_value()
        _type = 'base'
    return (_index,_type)


