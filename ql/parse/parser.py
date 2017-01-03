'''
Created on Dec 15, 2016

@author: qs
'''

from ql.parse import lexer
from ql.parse import ASTNode
from enum import Enum



TOKEN = Enum('TOKEN', ['TOK_IDENTIFIER','TOK_VALUE','TOK_DOT','TOK_CORE_TYPE','TOK_SORT_MODE',
                           'TOK_LIST','TOK_DICT',
                           'TOK_EXPRESSION',
                           'TOK_COLUMN_DEFINE','TOK_META_DEFINE','TOK_TABLE_COLUMNS','TOK_TABLE_NAME','TOK_TABLE_METAS','TOK_TABLE_OPTIONS',
                           'TOK_CREATE_TABLE','TOK_QUERY',
                           'TOK_FUNCTION',
                           'TOK_KEY_VALUE',
                           'TOK_COMPARE','TOK_REVERSED','TOK_COMPLEX',
                           'TOK_SELECT','TOK_FROM','TOK_WHERE','TOK_LIMIT','TOK_ORDERBY','TOK_GROUPBY','TOK_SELEXPR','TOK_SORT',
                           'TOK_INSERT_INTO','TOK_INSERT_ROW','TOK_INSERT_COLUMNS'])


tokens = lexer.tokens

precedence = (
              ('left','OR'),
              ('left','AND'),
              ('left','NOT')
              )


def token_list(plist):
    retval = []
    if len(plist) == 2:
        retval = [plist[1]]
    else:
        if isinstance(plist[3],list):
            retval = [plist[1]] + plist[3]
        else:
            retval = [plist[1],plist[3]]    
    return retval


def p_STATEMENT(p):
    '''TOK_FUNCTION_EXPR : TOK_CREATE_TABLE END_QUERY
    | TOK_QUERY END_QUERY
    | TOK_INSERT_INTO END_QUERY'''
    p[0] = p[1]



'''======================================base define========================================================'''


def p_TOK_OPTIONS_OBJECT(p):
    '''TOK_OPTIONS_OBJECT : "(" KV_ELEMENTS_EXPR ")"'''
    p[0] = ASTNode.ASTNode(TOKEN.TOK_DICT,None,p[2])


def p_TOK_DICT_OBJECT(p):
    '''TOK_DICT_OBJECT : "{" KV_ELEMENTS_EXPR "}"'''
    p[0] = ASTNode.ASTNode(TOKEN.TOK_DICT,None,p[2])


def p_TOK_LIST_OBJECT(p):
    '''TOK_LIST_OBJECT : "[" VALUES_EXPR "]"'''
    p[0] = ASTNode.ASTNode(TOKEN.TOK_LIST,None,p[2])
    

def p_KV_ELEMENTS_EXPR(p):
    '''KV_ELEMENTS_EXPR : TOK_KEY_VALUE
    | TOK_KEY_VALUE COMMA TOK_KEY_VALUE
    | TOK_KEY_VALUE COMMA KV_ELEMENTS_EXPR'''
    p[0] = token_list(p)                 


def p_VALUES_EXPR(p):
    '''VALUES_EXPR : VALUE_EXPR
    | VALUE_EXPR COMMA VALUE_EXPR
    | VALUE_EXPR COMMA VALUES_EXPR'''
    p[0] = token_list(p)
            
            


def p_TOK_KEY_VALUE(p):
    '''TOK_KEY_VALUE : TOK_EXPRESSION'''
    if p[1].getTokValue() != '=':
        pass
    else:
        p[0] = p[1]
    p[0].setTokType(TOKEN.TOK_KEY_VALUE)



def p_LEFT_RESERVED_VALUES_EXPR(p):
    '''LEFT_RESERVED_VALUES_EXPR :  FROM
    | TO'''
    p[0] = ASTNode.ASTNode(TOKEN.TOK_VALUE,p[1],None)


 
def p_LEFT_VALUE_EXPR(p):
    '''LEFT_VALUE_EXPR :  VALUE_EXPR
    | TOK_FUNCTION_EXPR
    | LEFT_RESERVED_VALUES_EXPR'''
    p[0] = p[1]

def p_LEFT_VALUES_EXPR(p):
    '''LEFT_VALUES_EXPR :  LEFT_VALUE_EXPR
    | LEFT_VALUE_EXPR COMMA LEFT_VALUE_EXPR
    | LEFT_VALUE_EXPR COMMA LEFT_VALUES_EXPR'''
    p[0] = token_list(p)
         
   
def p_RIGHT_VALUE_EXPR(p):
    '''RIGHT_VALUE_EXPR :  VALUE_EXPR'''
    p[0] = p[1]    


def p_RIGHT_VALUES_EXPR(p):
    '''RIGHT_VALUES_EXPR :  VALUE_EXPR
    | RIGHT_VALUE_EXPR COMMA RIGHT_VALUE_EXPR
    | RIGHT_VALUE_EXPR COMMA RIGHT_VALUES_EXPR'''
    p[0] = token_list(p)
    
    

def p_VALUE_EXPR(p):
    '''VALUE_EXPR :  TOK_DOT
    | TOK_VALUE
    | TOK_DICT_OBJECT
    | TOK_LIST_OBJECT'''
    p[0] = p[1]


def p_TOK_DOT(p):
    '''TOK_DOT : TOK_VALUE "." TOK_VALUE
    | TOK_VALUE "." TOK_DOT'''
    p[0] = ASTNode.ASTNode(TOKEN.TOK_DOT,p[2],[p[1],(p[3])])
       
       
def p_TOK_VALUE(p):
    '''TOK_VALUE : WORD
    | QUOTE_STRING
    | NUMBER
    | DQUOTE_STRING
    | "*"'''
    p[0] = ASTNode.ASTNode(TOKEN.TOK_VALUE,p[1],None)
    
'''=======================================operator define=============================================='''

 
def p_EXPRESSIONS_REVERSED_EXPR(p):
    '''EXPRESSION_EXPR : NOT EXPRESSION_EXPR'''
    p[0] = ASTNode.ASTNode(TOKEN.TOK_REVERSED,p[1].lower(),[p[2]])
    

def p_EXPRESSIONS_GROUP_EXPR(p):
    '''EXPRESSION_EXPR : "(" EXPRESSION_EXPR ")"'''
    p[0] = p[2]


def p_EXPRESSION_OPERATOR_EXPR(p):
    '''EXPRESSION_EXPR :  EXPRESSION_EXPR OR EXPRESSION_EXPR
    | EXPRESSION_EXPR AND EXPRESSION_EXPR'''
    p[0] = ASTNode.ASTNode(TOKEN.TOK_COMPLEX,p[2].lower(),[p[1],p[3]])



def p_EXPRESSION_EXPR(p):
    '''EXPRESSION_EXPR : TOK_EXPRESSION
    | TOK_FUNCTION_EXPR'''
    p[0] = p[1]
    
    
def p_TOK_EXPRESSION(p):
    '''TOK_EXPRESSION : LEFT_VALUE_EXPR COMPARE_TYPE_EXPR RIGHT_VALUE_EXPR'''
    if p[2] == '!=':
        expression = ASTNode.ASTNode(TOKEN.TOK_COMPARE,'=',[p[1],p[3]])
        p[0] = ASTNode.ASTNode(TOKEN.TOK_REVERSED,'NOT'.lower(),[expression])
    else:
        p[0] = ASTNode.ASTNode(TOKEN.TOK_COMPARE,p[2],[p[1],p[3]])


def p_COMPARE_TYPE_EXPR(p):
    '''COMPARE_TYPE_EXPR : COMPARE_TYPE
    | LIKE'''
    p[0] = p[1]
    

def p_TOK_FUNCTION_EXPR(p):
    '''TOK_FUNCTION_EXPR : TOK_FUNCTION
    | TOK_BEWTEEN'''
    p[0] = p[1]
    
       
def p_TOK_FUNCTION(p):
    '''TOK_FUNCTION : WORD "(" FUNCTION_PARMS_EXPR ")"'''
    p[0] = ASTNode.ASTNode(TOKEN.TOK_FUNCTION,p[1],p[3])
    
       
def p_TOK_BEWTEEN(p):
    '''TOK_BEWTEEN : LEFT_VALUE_EXPR BETWEEN RIGHT_VALUE_EXPR AND RIGHT_VALUE_EXPR'''
    p[0] = ASTNode.ASTNode(TOKEN.TOK_FUNCTION,p[2],[p[1],(p[3]),p[5]])


def p_FUNCTION_PARMS_EXPR(p):
    '''FUNCTION_PARMS_EXPR :  VALUE_EXPR
    | VALUE_EXPR COMMA VALUE_EXPR
    | VALUE_EXPR COMMA FUNCTION_PARMS_EXPR'''
    p[0] = token_list(p)
    
        

'''==========================================table define===========================================

CREATE TABLE my_index.my_type (
    id STRING (index = no),
    name INTEGER,
    log OBJECT AS (
        raw string (index=not_analyzed,doc_values=false),
        ik string (analyzer=ik)
        )
    ) with meta (
        _parent (type='people')
    ) with option (
        index.number_of_shars=10,
        index.flush_interval='10s'
    )
'''


def p_TOK_CREATE_TABLE_WITH_OPTIONS(p):
    '''TOK_CREATE_TABLE : TOK_CREATE_TABLE WITH OPTION TOK_TABLE_OPTIONS'''
    p[0] = p[1]
    p[0].appendChildren(p[4])
    

def p_TOK_CREATE_TABLE_WITH_META(p):
    '''TOK_CREATE_TABLE : TOK_CREATE_TABLE WITH META TOK_TABLE_METAS'''
    p[0] = p[1]
    p[0].appendChildren(p[4])
    
    
def p_TOK_CREATE_TABLE(p):
    '''TOK_CREATE_TABLE : CREATE TABLE TOK_TABLE_NAME TOK_TABLE_COLS'''
    p[0] = ASTNode.ASTNode(TOKEN.TOK_CREATE_TABLE,None,[p[3],p[4]])
    
        
    
def p_TOK_META_DEFINE(p):
    '''TOK_META_DEF : WORD TOK_OPTIONS_OBJECT'''
    p[0] = ASTNode.ASTNode(TOKEN.TOK_META_DEFINE,p[1],[p[2]])


def p_TOK_METAS_DEFINE(p):
    '''TOK_METAS_DEF : TOK_META_DEF
    | TOK_META_DEF COMMA TOK_META_DEF
    | TOK_META_DEF COMMA TOK_METAS_DEF'''
    p[0] = token_list(p)
                    

def p_TOK_TABLE_METAS(p):
    '''TOK_TABLE_METAS : "(" ")"
    | "(" TOK_METAS_DEF ")"'''
    if len(p) == 3:
        p[0] = ASTNode.ASTNode(TOKEN.TOK_TABLE_METAS,None,None)
    else:  
        p[0] = ASTNode.ASTNode(TOKEN.TOK_TABLE_METAS,None,p[2])
        
def p_TOK_TABLE_OPTIONS(p):
    '''TOK_TABLE_OPTIONS : TOK_OPTIONS_OBJECT'''
    p[0] = ASTNode.ASTNode(TOKEN.TOK_TABLE_OPTIONS,None,[p[1]])


def p_TOK_TABLE_NAME(p):
    '''TOK_TABLE_NAME : LEFT_VALUE_EXPR'''
    p[0] = ASTNode.ASTNode(TOKEN.TOK_TABLE_NAME,None,[p[1]])



def p_TOK_TABLE_COLS(p):
    '''TOK_TABLE_COLS : "(" ")"
    | "(" TOK_COLUMNS_DEFINE ")"'''
    if len(p) == 3:
        p[0] = ASTNode.ASTNode(TOKEN.TOK_TABLE_COLUMNS,None,None)
    else:  
        p[0] = ASTNode.ASTNode(TOKEN.TOK_TABLE_COLUMNS,None,p[2])
            

def p_TOK_COLUMNS_DEFINE(p):
    '''TOK_COLUMNS_DEFINE : TOK_COLUMN_DEFINE
    | TOK_COLUMN_DEFINE COMMA TOK_COLUMN_DEFINE
    | TOK_COLUMN_DEFINE COMMA TOK_COLUMNS_DEFINE'''
    p[0] = token_list(p)


def p_COLUMN_TYPE(p):
    '''COLUMN_TYPE : STRING
    | INTEGER
    | LONG
    | DATE
    | OBJECT'''
    p[0] = ASTNode.ASTNode(TOKEN.TOK_CORE_TYPE,p[1],None)
 
 
def p_TOK_COLUMN_OBJECT_DEFINE(p):
    '''TOK_COLUMN_DEFINE : TOK_COLUMN_DEFINE AS TOK_TABLE_COLS'''
    p[0] = p[1]
    p[0].appendChildren(p[3])    
    

def p_TOK_COLUMN_DEFINE(p):
    '''TOK_COLUMN_DEFINE : WORD COLUMN_TYPE
    | WORD COLUMN_TYPE TOK_OPTIONS_OBJECT'''
    if len(p) == 3:
        p[0] = ASTNode.ASTNode(TOKEN.TOK_COLUMN_DEFINE,p[1],[p[2]])
    else:
        p[0] = ASTNode.ASTNode(TOKEN.TOK_COLUMN_DEFINE,p[1],[p[2],p[3]])     
        
      
      
                 

'''=================================query define========================================'''

def p_TOK_QUERY_WITH_ORDERBY(p):
    '''TOK_QUERY : TOK_QUERY ORDER BY TOK_ORDERBY'''
    p[0] = p[1]
    p[0].appendChildren(p[4])
    

def p_TOK_QUERY_WITH_EXPRESSIONS(p):
    '''TOK_QUERY : TOK_QUERY WHERE TOK_WHERE'''
    p[0] = p[1]
    p[0].appendChildren(p[3])

def p_TOK_QUERY_WITH_LIMITS(p):
    '''TOK_QUERY : TOK_QUERY LIMIT TOK_LIMIT'''
    p[0] = p[1]
    p[0].appendChildren(p[3])
        
        
def p_TOK_QUERY(p):
    '''TOK_QUERY : SELECT TOK_SELECT FROM TOK_FROM'''
    p[0] = ASTNode.ASTNode(TOKEN.TOK_QUERY,None,[p[2],p[4]])
    
    
def p_TOK_FROM(p):
    '''TOK_FROM : TOK_TABLE_NAME'''
    p[0] = ASTNode.ASTNode(TOKEN.TOK_FROM,None,[p[1]])

    
def p_TOK_WHRER(p):
    '''TOK_WHERE : EXPRESSION_EXPR'''
    p[0] = ASTNode.ASTNode(TOKEN.TOK_WHERE,None,[p[1]])
               
        
def p_TOK_SELECT(p):
    '''TOK_SELECT : TOK_SELEXPRS'''
    p[0] = ASTNode.ASTNode(TOKEN.TOK_SELECT,None,p[1])        


def p_TOK_SELEXPR(p):
    '''TOK_SELEXPR : LEFT_VALUE_EXPR'''
    p[0] = ASTNode.ASTNode(TOKEN.TOK_SELEXPR,None,[p[1]])


def p_TOK_SELEXPRS(p):
    '''TOK_SELEXPRS : TOK_SELEXPR
    | TOK_SELEXPR COMMA TOK_SELEXPR
    | TOK_SELEXPR COMMA TOK_SELEXPRS'''
    p[0] = token_list(p)


def p_TOK_LIMIT(p):
    '''TOK_LIMIT : LIMITS_EXPR'''
    p[0] = ASTNode.ASTNode(TOKEN.TOK_LIMIT,None,p[1])
    
    
def p_LIMIT_EXPR(p):
    '''LIMIT_EXPR : NUMBER'''
    p[0] = ASTNode.ASTNode(TOKEN.TOK_VALUE,p[1],None)
 
 
def p_LIMITS_EXPR(p):
    '''LIMITS_EXPR : LIMIT_EXPR
    | LIMIT_EXPR COMMA LIMIT_EXPR'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1],p[3]]
        
        
def p_TOK_ORDERBY(p):
    '''TOK_ORDERBY : TOK_SORTS'''
    p[0] = ASTNode.ASTNode(TOKEN.TOK_ORDERBY,None,p[1])        


def p_TOK_SORTS(p):
    '''TOK_SORTS : TOK_SORT
    | TOK_SORT COMMA TOK_SORT
    | TOK_SORT COMMA TOK_SORTS'''
    p[0] = token_list(p)
   

def p_SORT_MODE(p):
    '''SORT_MODE : ASC
    | DESC'''
    p[0] = ASTNode.ASTNode(TOKEN.TOK_SORT_MODE,p[1],None)     
    
    
def p_TOK_SORT(p):
    '''TOK_SORT : LEFT_VALUE_EXPR
    | LEFT_VALUE_EXPR SORT_MODE'''
    if len(p) == 2: 
        p[0] = ASTNode.ASTNode(TOKEN.TOK_SORT,None,[p[1]])   
    else:
        p[0] = ASTNode.ASTNode(TOKEN.TOK_SORT,None,[p[1],p[2]])  
    
    
    
    
'''=================================Aggregations define========================================'''
        
def p_TOK_QUERY_WITH_GROUPBY(p):
    '''TOK_QUERY : TOK_QUERY GROUP BY TOK_GROUPBY'''
    p[0] = p[1]
    p[0].appendChildren(p[4])
            
        
def p_TOK_GROUPBY(p):
    '''TOK_GROUPBY : LEFT_VALUES_EXPR'''
    p[0] = ASTNode.ASTNode(TOKEN.TOK_GROUPBY,None,p[1])    
    
    
    
'''=================================Insert define========================================'''    

def p_TOK_INSERT_INTO(p):
    '''TOK_INSERT_INTO : INSERT INTO TOK_TABLE_NAME TOK_INSERT_COLUMNS VALUES TOK_VALUE_ROWS'''
    p[3].toStringTree()
    p[0] = ASTNode.ASTNode(TOKEN.TOK_INSERT_INTO,None,[p[3]] + [p[4]] + [p[6]])
    
    
    
def p_TOK_INSERT_COLUMNS(p):
    '''TOK_INSERT_COLUMNS : "(" LEFT_VALUES_EXPR ")" '''
    p[0] = ASTNode.ASTNode(TOKEN.TOK_INSERT_ROW,None,p[2])      
      
    
def p_TOK_INSERT_VALUES(p):
    '''TOK_VALUE_ROWS : "(" RIGHT_VALUES_EXPR ")" '''
    p[0] = ASTNode.ASTNode(TOKEN.TOK_INSERT_COLUMNS,None,p[2])  



