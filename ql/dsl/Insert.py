'''
Created on Mar 14, 2017

@author: qs
'''


from ql.parse.ASTNode import Node
from ql.parse.parser import TK
from ql.dsl import parse_object,parse_tok_table_name,parse_value



def parse_insert_columns(tree: Node):
    retval = []
    for e in tree.get_children():
        if e.get_type() == TK.TOK_VALUE:
            retval.append(parse_value(e))
    return retval
    
def parse_insert_row(tree: Node):
    retval = []
    for e in tree.get_children():
        if e.get_type() == TK.TOK_VALUE:
            retval.append(parse_value(e))
        elif e.get_type() in (TK.TOK_DICT,TK.TOK_LIST):
            retval.append(parse_object(e))
    return retval
    
    
class Insert(object):
    
    __slots__ = ('_index','_type','insert_columns','insert_row')
    def __init__(self,tree: Node):
        self.insert_columns = []
        self.insert_row = []
        for element in tree.get_children():
            if element.get_type() == TK.TOK_TABLE_NAME:
                (self._index,self._type) = parse_tok_table_name(element)
            elif element.get_type() == TK.TOK_INSERT_COLUMNS:
                self.insert_columns = parse_insert_columns(element)
            elif element.get_type() == TK.TOK_INSERT_ROW:
                self.insert_row = parse_insert_row(element)
            
        print(self._index,self._type)
        print(self.insert_columns)
        print(self.insert_row)  
              
    def dsl(self):
        dsl_body = {}
        if len(self.insert_columns) != len(self.insert_row):
            return dsl_body
        for i in range(0,len(self.insert_columns)):
            dsl_body[self.insert_columns[i]] = self.insert_row[i]
        return dsl_body
    
    