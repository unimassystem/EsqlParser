'''
Created on Jan 17, 2017

@author: unimas
'''

from ql.parse.ASTNode import Node
from ql.parse.parser import TK
from ql.dsl.QueryBody import QueryBody
from ql.dsl import parse_table_name,parse_value,parse_right_values
from ql.dsl.Aggregation import AggBuckets


class FunctionXpr(object):
    __slots__ = ('function_name','function_parms')
    def __init__(self,tree: Node):
        self.function_name = tree.get_value()
        self.function_parms = parse_right_values(tree.get_children())


class Selexpr(object):
    __slots__ = ('selexpr','alias')
    def __init__(self,tree: Node):
        if tree.get_child(0).get_type() == TK.TOK_FUNCTION:
            self.selexpr = FunctionXpr(tree.get_child(0))
        else:
            self.selexpr = parse_value(tree.get_child(0))
        if tree.get_children_count() == 2:
            self.alias = parse_value(tree.get_child(1))



def parse_tok_from(tree : Node):
    if tree.get_type() == TK.TOK_TABLE_NAME:
        return  parse_table_name(tree.get_child(0))
    else:
        pass


def parse_tok_limit(tree : Node):
    _from = 0
    _size = 0

    if tree.get_children_count() == 2:
        _from = tree.get_child(0).get_value()
        _size=  tree.get_child(1).get_value()
    else:
        _from = 0
        _size = tree.get_child(0).get_value()
    return (_from,_size)


def parse_tok_sorts(tree : Node):
    sorts = {}
    for sort in tree.get_children():
        if sort.get_type() == TK.TOK_SORT:
            order = 'asc'
            if sort.get_children_count() == 2:
                order = sort.get_child(1).get_value()
            sorts[sort.get_child(0).get_value()] = {'order':order}
    return sorts



def parse_tok_selexpr(tree : Node):
    retval = []
    for e in tree.get_children():
        retval.append(Selexpr(e))
    return retval


def get_source(selexprs):
    retval = []
    for e in selexprs:
        if type(e.selexpr) == str:
            retval.append(e.selexpr)
    return retval
            



class Query(object):
    
    __slots__ = ('_index','_type','query_body','_from','_size','sorts','selexpr','groupby')
    def __init__(self,tree: Node):
        
        #do query
        for element in tree.get_children():
            if element.get_type() == TK.TOK_FROM:
                (self._index,self._type) = parse_tok_from(element.get_child(0))
                
            if element.get_type() == TK.TOK_SELECT:
                self.selexpr = parse_tok_selexpr(element)
                
            if element.get_type() == TK.TOK_WHERE:
                self.query_body = QueryBody(element.get_child(0))
                
            if element.get_type() == TK.TOK_LIMIT:
                (self._from,self._size) = parse_tok_limit(element)
                
            if element.get_type() == TK.TOK_ORDERBY:
                self.sorts = parse_tok_sorts(element)
        
        #do aggregations
        for element in tree.get_children():
            if element.get_type() == TK.TOK_GROUPBY:
                agg_size = -1
                print(hasattr(self, '_size'))
                if hasattr(self, '_size'):
                    agg_size = self._size
                print(agg_size)
                self.groupby = AggBuckets(element,agg_size)

    def dsl(self):
        dsl_body = {}
        if hasattr(self, 'query_body'):
            dsl_body['query'] = self.query_body.dsl()
        else:
            dsl_body['query'] = {'match_all':{}}
        if hasattr(self, '_from'):
            dsl_body['from'] = self._from
        if hasattr(self, '_size'):
            dsl_body['size'] = self._size
        if hasattr(self, 'sorts'):
            dsl_body['sort'] = self.sorts
        if hasattr(self, 'selexpr'):
            dsl_body['_source'] = get_source(self.selexpr)
        if hasattr(self, 'groupby'):
            dsl_body.update((self.groupby.dsl(self.selexpr)))
            dsl_body['size'] = 0
        return dsl_body
    
    
    
    
    