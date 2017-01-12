from typing import List
from parser import TK, Node, Element, AttributeList, TableName


class FieldDefine(Element):
    __slots__ = ('name', 'type', 'options', 'fields')

    def __init__(self, tree: Node):
        if tree.type == TK.TOK_COLUMN_DEFINE:
            self.name = tree.value
            self.type = tree.sub(0).value
            if self.type == 'object':
                cols = tree.sub_token(TK.TOK_TABLE_COLUMNS)
                if cols and cols.children:
                    self.fields = FieldsDefine(cols.children)
            opts = tree.sub_token(TK.TOK_COLUMN_OPTIONS)
            if opts:
                self.options = AttributeList(opts.sub(0).children)

    def dsl(self):
        field = {'type': self.type}
        if hasattr(self, 'options'):
            for option in self.options:
                field[option.key] = option.value
        if hasattr(self, 'fields'):
            field['properties'] = self.fields.dsl()
        return field


class FieldsDefine(List[FieldDefine]):

    def __init__(self, fields):
        for field in fields:
            self.append(FieldDefine(field))

    def dsl(self):
        properties = {}
        for field in self:
            properties[field.name] = field.dsl()
        return properties


class TableCreate(Element):
    """ Create Table
    """
    __slots__ = ('table', 'fields')

    mapping = TK.TOK_CREATE_TABLE

    def __init__(self, tree: Node = None):
        for child in tree.children:
            if child.type == TK.TOK_TABLE_NAME:
                self.table = TableName(child.children)
            elif child.type == TK.TOK_TABLE_COLUMNS:
                self.fields = FieldsDefine(child.children)

    def dsl(self):
        ret = {'index': self.table.index_name,
               'doc_type': self.table.doc_type,
               'body': {self.table.doc_type: {}}}
        ret['body'][self.table.doc_type]['properties'] = self.fields.dsl()
        return ret


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
        properties = {'aaa':1}
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


class DataSelect(Element):
    """ Data Query (Select)
    """
    __slots__ = ('table', 'select', 'group_by')
    
    mapping = TK.TOK_QUERY

    def __init__(self, tree: Node):
        for child in tree.children:
            if child.type == TK.TOK_SELECT:
                self.select = SelectFields(child.children)
            elif child.type == TK.TOK_FROM:
                self.table = TableName(child.sub_token(TK.TOK_TABLE_NAME).children)
            elif child.type == TK.TOK_GROUPBY:
                self.group_by = GroupByFields(child.children)

    def dsl(self):
        ret = {'index': self.table.index_name,
               'doc_type': self.table.doc_type,
               '_source': []}
        for item in self.select:
            if item.type == TK.TOK_VALUE:
                ret['_source'].append(item.name)
        if hasattr(self, 'group_by'):
            ret['aggs'] = self.group_by.dsl()
        return ret
