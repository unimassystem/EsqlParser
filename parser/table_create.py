from typing import List
from parser import TK, Node, Element, Attributes, TableName


class FieldDefine(Element):
    __slots__ = ('name', 'type', 'options', 'fields')

    def __init__(self, tree: Node = None):
        if tree.type == TK.TOK_COLUMN_DEFINE:
            self.name = tree.value
            self.type = tree.sub(0).value
            if self.type == 'object':
                cols = tree.sub_token(TK.TOK_TABLE_COLUMNS)
                if cols and cols.children:
                    self.fields = FieldsDefine(cols.children)
            opts = tree.sub_token(TK.TOK_COLUMN_OPTIONS)
            if opts:
                self.options = Attributes(opts.sub(0).children)

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

    def __init__(self, tree: Node, table: TableName = None, fields: List[FieldDefine] = None):
        self.table = table
        self.fields = fields or []

        for child in tree.children:
            if child.type == TK.TOK_TABLE_NAME:
                self.table = TableName(child.children)
            elif child.type == TK.TOK_TABLE_COLUMNS:
                self.fields = FieldsDefine(child.children)

    def dsl(self):
        dsl = {'index': self.table.index_name,
               'doc_type': self.table.doc_type,
               'body': {self.table.doc_type: {}}}
        dsl['body'][self.table.doc_type]['properties'] = self.fields.dsl()
        return dsl
