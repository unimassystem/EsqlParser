'''
Created on Mar 15, 2017

@author: qs
'''

from ql.parse.ASTNode import Node
from ql.parse.parser import TK
from ql.dsl.Query import Query
# from ql.dsl.Create import Create
# from ql.dsl.Insert import Insert




class Explain(object):
    
    
    def __init__(self,tree: Node):
        
        exec_node = tree.get_child(0)
        
        stmt = None
        self.dsl_body = {}
        self.curl_str = ''
        
        es_url = 'http://localhost:9200/'
        
        if exec_node.get_type() == TK.TOK_QUERY:
            stmt = Query(exec_node)
            self.curl_str = 'curl -XPOST ' + es_url + stmt._index + '/' + stmt._type + '/_search'
            self.dsl_body = stmt.dsl()
            

#         if exec_node.get_type() == TK.TOK_CREATE_TABLE:
#             stmt = Create(exec_node)
#             self.curl_str = 'curl -XPOST ' + es_url + stmt._index
#             self.dsl_body['mappings'] = {stmt._type:stmt.dsl()}
#             self.dsl_body['settings'] = stmt._options
#         if exec_node.get_type() == TK.TOK_QUERY:
#             stmt = Query(exec_node)
#             self.curl_str = 'curl -XPOST ' + es_url + stmt._index + '/' + stmt._type + '/_search'
#             self.dsl_body = stmt.dsl()
                
#         if exec_node.get_type() == TK.TOK_INSERT_INTO:
#             parms = ''
#             stmt = Insert(exec_node)
#             self.curl_str = 'curl -XPOST ' + es_url + stmt._index + '/' + stmt._type 
#             if 'id' in stmt.metas.keys():
#                 self.curl_str =  self.curl_str + '/' + str(stmt.metas['id'])
#             if 'routing' in  stmt.metas.keys():
#                 if len(parms) == 0:
#                     parms = '?'
#                 parms = parms + 'routing' + '=' +  str(stmt.metas['routing'])
#             if 'parent' in  stmt.metas.keys():
#                 if len(parms) == 0:
#                     parms = '?'
#                 parms = parms + 'parent' + '=' +  str(stmt.metas['parent'])
#             if len(parms) > 0:
#                 self.curl_str = self.curl_str + parms
#             self.dsl_body = stmt.dsl()

                
    def dsl(self):
        return self.dsl_body
        
    
    