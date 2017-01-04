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
     
    if len(sys.argv) <= 2:
        
         
#         val = parser.parse(lexer=lexer.clone(),debug=False,input="create table my_tb (a text,b integer, c object as (raw string (index=yes,ppp=yes))) with meta (_parent (type='people')) with option (index.number_of_shars=10,index.flush_inteval='10s');")
#  
#         val.toStringTree()
#         
#         val = parser.parse(lexer=lexer.clone(),debug=False,input="select strcat(a,b),c.raw from test.info where a = 10 or b between 10 and 20 and ( b = 20 or c = 10) and length(a.raw) > 10 and strcat(f.raw,b) limit 0,10 order by a asc,b,c desc;")
#         
#         val.toStringTree()
#        
#         val = parser.parse(lexer=lexer.clone(),debug=False,input="select sum.a(id) as sum,a as b from test.info group by a,date_histogram(my_date,{interval='1d'},['test','ttt'],'hello world',10);")
#              
#         val.toStringTree()
#          
#                  
#         val = parser.parse(lexer=lexer.clone(),debug=False,input="select sum(id) from test.info group by range(my_age,{from=10,to=20},{from=20});")
#                  
#         val.toStringTree()
#                       
#         val = parser.parse(lexer=lexer.clone(),debug=False,input="insert into my_index (name,age,address,message) values ('zhangsan',24,{address='zhejiang',postCode='330010'},['sms:001','sms:002']);")
#            
#         val.toStringTree()
#          
#         
#         val = parser.parse(lexer=lexer.clone(),debug=False,input="bulk into my_index(name,age,address,message) values [('zhangsan',24,{address='zhejiang',postCode='330010'},['sms:001','sms:002']),('zhangsan',25,{address='zhejiang',postCode='330010'},['sms:001','sms:002'])] ;")
#                 
#         val.toStringTree()        
#          
        
        val = parser.parse(lexer=lexer.clone(),debug=False,input="update my_index set name = 'lisi' ,age = 30,address={address='shanghai',postCode='330010'} where _id = 330111111;")
                 
        val.toStringTree()  


        val = parser.parse(lexer=lexer.clone(),debug=False,input="upsert into my_index (_id,name,age,address,message) values (330001,'zhangsan',24,{address='zhejiang',postCode='330010'},['sms:001','sms:002']);")
                 
        val.toStringTree()     
    else: 
        val = parser.parse(lexer=lexer.clone(),debug=False,input=sys.argv[1])
        val.toStringTree()
