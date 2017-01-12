from typing import List
from parser import TK, Node, Element, TableName
from parser.utility import *


class SelectField(Element):
    __slots__ = ('name', 'type', 'params')

    def __init__(self, tree: Node):
        self.name = tree.sub(0).value
        self.type = tree.sub(0).type
        if tree.sub(0).type == TK.TOK_FUNCTION:
            self.params = []
            for item in tree.sub(0).children:
                self.params.append(item.value)

    def dsl(self):
        properties = {}
        return properties


class SelectFields(List[SelectField]):

    def __init__(self, objects):
        for item in objects:
            self.append(SelectField(item))

    def dsl(self):
        properties = {}
        for item in self:
            properties[item.name] = item.dsl()
        return properties


class GroupByFields(list):

    def __init__(self, objects):
        for item in objects:
            self.append(item.value)

    def dsl(self):
        properties = {}
        for item in self:
            properties[item] = {'terms': {'field': item, 'size': 4096}}
        return properties


class Compare(Element):
    __slots__ = ('operate', 'left', 'right')

    def __init__(self, tree: Node):
        self.operate = tree.value
        self.left = tree.sub(0).value
        self.right = tree.sub(1).value

    def dsl(self):
        ret = {}
        if self.operate == '=':
            ret['query_string'] = {self.left: self.right}
        if self.operate == 'like':
            ret['wildcard'] = {self.left: self.right}
        return ret


def gen_function_dsl(rst):
    ret = {}
    if rst.name == 'between':
        ret['range'] = {rst.params[0]: {'gte': rst.params[1], 'lte': rst.params[2]}}
    return ret


class Function(Element):
    __slots__ = ('name', 'params')

    def __init__(self, tree: Node):
        self.name = tree.value
        self.params = []
        for item in tree.children:
            self.params.append(item.value)

    def dsl(self):
        return gen_function_dsl(self)


def gen_complex_child(tree):
    if tree.type == TK.TOK_COMPLEX:
        return Complex(tree)
    elif tree.type == TK.TOK_FUNCTION:
        return Function(tree)
    else:
        return Compare(tree)


class Complex(Element):
    __slots__ = ('operate', 'left', 'right')

    def __init__(self, tree: Node):
        self.operate = tree.value
        self.left = gen_complex_child(tree.sub(0))
        self.right = gen_complex_child(tree.sub(1))

    def dsl(self):
        ret = {'bool': {}}
        key = 'must'
        if self.operate == 'or':
            key = 'should'
        ret['bool'][key] = [self.left.dsl(), self.right.dsl()]
        return ret


class DataSelect(Element):
    """ Data Query (Select)
    """
    __slots__ = ('table', 'select', 'where', 'group_by')
    
    mapping = TK.TOK_QUERY

    def __init__(self, tree: Node):
        for child in tree.children:
            if child.type == TK.TOK_SELECT:
                self.select = SelectFields(child.children)
            elif child.type == TK.TOK_FROM:
                self.table = TableName(child.sub_token(TK.TOK_TABLE_NAME).children)
            elif child.type == TK.TOK_GROUPBY:
                self.group_by = GroupByFields(child.children)
            elif child.type == TK.TOK_WHERE:
                self.where = Complex(child.sub(0))

    def dsl(self):
        ret = {'index': self.table.index_name,
               'doc_type': self.table.doc_type,
               '_source': []}
        for item in self.select:
            if item.type == TK.TOK_VALUE:
                ret['_source'].append(item.name)
        if hasattr(self, 'where'):
            ret['query'] = self.where.dsl()
        if hasattr(self, 'group_by'):
            ret['aggs'] = self.group_by.dsl()
        return ret
