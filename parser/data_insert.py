from parser import TK, Node, Element, AttributeDict, ItemList, TableName


class DataInsert(Element):
    """ Data Insert (INSERT INTO)
    """
    __slots__ = ('table', 'fields', 'values')

    mapping = TK.TOK_INSERT_INTO

    def __init__(self, tree: Node):
        self.table = TableName(tree.sub(0).sub(0))
        self.fields = ItemList(tree.sub(1).children)
        self.values = ItemList(tree.sub(2).children)
        self.field_count = len(self.fields)

    def dsl(self):
        ret = {'index': self.table.index_name,
               'doc_type': self.table.doc_type,
               'body': {}}
        for index in range(0, self.field_count):
            value = self.values[index]
            if type(value) == AttributeDict:
                ret['body'][self.fields[index]] = value.dsl()
            else:
                ret['body'][self.fields[index]] = value
        return ret
