'''
Created on Dec 23, 2016

@author: qs
'''
# -*- coding: utf-8 -*- 




from ql.parse import lexer
from ql.parse import parser
from ply.lex import  lex
from ply.yacc import yacc
import sys

if __name__ == "__main__":

    lexer=lex(module=lexer,optimize=True,debug=True)
       
    parser=yacc(debug=True,module=parser)
     
#     val = parser.parse(lexer=lexer.clone(),debug=False,input="create table my_tb.info (a string,b integer, c object as (raw string (index=yes,ppp=yes))) with meta (_parent (type='people')) with option (index.number_of_shars=10,index.flush_inteval='10s');")
#     val.toStringTree()
#   
#     val = parser.parse(lexer=lexer.clone(),debug=False,input="select strcat(a,b),c.raw from test.info where a = 10 or b between 10 and 20 and ( b = 20 or c = 10) and length(a.raw) > 10 and strcat(f.raw,b) limit 0,10 order by a asc,b,c desc;")
#     val.toStringTree()
#   
#     val = parser.parse(lexer=lexer.clone(),debug=False,input="select sum(id) from test.info where a = \"10\" group by a,date_histogram(my_date,{interval='1d'},['test','ttt'],'hello world',10);")
#     val.toStringTree()
  
    val = parser.parse(lexer=lexer.clone(),debug=False,input=sys.argv[1])
    val.toStringTree()
