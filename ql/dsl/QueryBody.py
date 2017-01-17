'''
Created on Jan 13, 2017

@author: qs
'''

from ql.dsl import *

def query_string_query(left_val,right_val):
    return {
        'query_string':{
            'default_operator': 'AND',
            'query': right_val,
            'fields': left_val
        }
    }
    
    
def range_query(compare,left_val,right_val):
    if compare == '>':
        compare = 'gt'
    elif compare == '<':
        compare = 'lt'
    elif compare == '>=':
        compare = 'gte'
    elif compare == '<=':
        compare = 'lte'
    return {
        'range': {
            left_val[0]:{
                 compare:right_val
            }
        }
    }


def wildcard_query(left_val,right_val):
    return {'wildcard': {left_val[0]:right_val}}




def between_query(parms):
    return {
        'range': {
            parms[0]:{
                'gte':parms[1],
                'lte':parms[2],               
            }
        }
    }  


def query_missing(left_val):
    return {
        'constant_score': {
            'filter': {
                'missing': { 
                    'field': left_val[0]
                }
            }
        }
    }



def function_expression_dsl(name, parms):
    if name.lower() == 'between':
        return between_query(parms)
    if name.lower() == 'isnull':
        return query_missing(parms)
    


def compare_expression_dsl(compare,left_val,right_val):
    if compare == '=':
        return query_string_query(left_val,right_val)
    elif compare in ['>','>=','<','<=']:
        return range_query(compare,left_val,right_val)
    elif compare.lower() == 'like':
        return wildcard_query(left_val,right_val)
    

    
    
class FunctionExpression(object):
    __slots__ = ('function_name','function_parms')
    def __init__(self,tree: Node):
        self.function_name = tree.get_value()
        self.function_parms = parse_right_values(tree.get_children())
    def dsl(self):
        return function_expression_dsl(self.function_name,self.function_parms)



def query_expression(tree: Node):
    if tree.get_type() == TK.TOK_COMPARE:
        return CompareExpression(tree)
    if tree.get_type() == TK.TOK_FUNCTION:
        return FunctionExpression(tree)
    
       
class CompareExpression(object):
    
    __slots__ = ('compare','left_values','right_value')
    
    def __init__(self,tree: Node):
        self.compare = tree.get_value().lower()
        if tree.get_child(0).get_type() == TK.TOK_EXPRESSION_LEFT:      
            self.left_values = parse_left_values(tree.get_child(0).get_children())
        if tree.get_child(1).get_type() == TK.TOK_EXPRESSION_RIGHT:
            self.right_value = parse_value(tree.get_child(1).get_child(0))
    def dsl(self):
        return compare_expression_dsl(self.compare,self.left_values,self.right_value)
    
  

class QueryBody(object):
    
    __slots__ = ('combine','root','reversed','lchild','rchild')
    
    def __init__(self,tree: Node,root=True):
        
        if tree.get_type() == TK.TOK_REVERSED:
            tree = tree.get_child(0)
            self.reversed = True

        self.root = root;
        self.combine = 'must'
        if tree.get_type() == TK.TOK_COMPOUND:
            self.combine = tree.get_value()      
            self.lchild = QueryBody(tree.get_child(0),False)
            self.rchild = QueryBody(tree.get_child(1),False)
        else:
            self.lchild = query_expression(tree)


    def dsl(self):
        ret = {}
        
        if self.combine  == 'and':
            self.combine = 'must'
        if self.combine  == 'or':
            self.combine = 'should'
        if self.root:
            ret = {'bool': {}}
            ret['bool'][self.combine] = [self.lchild.dsl()]
            if hasattr(self, 'rchild'):
                ret['bool'][self.combine].append(self.rchild.dsl())     
        else:
            if hasattr(self, 'rchild'):
                ret = {'bool': {}}
                ret['bool'][self.combine] = [self.lchild.dsl()] + [self.rchild.dsl()]
            else:
                ret = self.lchild.dsl()
        if hasattr(self, 'reversed') and self.reversed == True:
            rev = {'bool': {}}
            rev['bool']['must_not'] = [ret]
            ret = rev
        return ret
            
       
        

