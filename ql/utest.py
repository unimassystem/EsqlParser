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
from ql.dsl.Query import Query
import json

if __name__ == "__main__":

    lexer=lex(module=lexer,optimize=True,debug=True)
       
    parser=yacc(debug=True,module=parser)
     
    if len(sys.argv) < 2:
        sqls = [
#         '''create table my_tb (
#             a text,b integer, 
#             c object as (
#                 raw string (index=yes,ppp=yes),
#                 obj object as (
#                     ddd string (index=yes,ppp=yes)
#                 )
#             )
#         ) with meta (
#             _parent (type='people')
#         ) with option (
#             index.number_of_shars=10,
#             index.flush_inteval='10s'
#         );''',
#          
#          
#        '''select strcat(a,b),c.raw from test.info where a = hello or b between 10 and 20 and ( b = 20 or c = 10) and length(a.raw) > 10 and strcat(f.raw,b) limit 0,10 order by a asc,b,c desc;''',
#        '''select * from my_index where a = hello;''',
        '''select * from my_index where city is not null and city = '3717'  and city between 3717 and 3718 limit 1,2 order by city group by data_histogram(a,{interval=10});''',
        
#   
#          '''select sum.a(id) as sum,a as b from test.info group by a,date_histogram(my_date,{interval='1d'},['test','ttt'],'hello world',10);''',
#   
#   
#         '''insert into my_index (name,age,address,message) values ('zhangsan',24,{address='zhejiang',postCode='330010'},['sms:001','sms:002']);''',
#   
#         '''bulk into my_index(name,age,address,message) values 
#             [('zhangsan',24,{address='zhejiang',postCode='330010'},['sms:001','sms:002']),
#             ('zhangsan',25,{address='zhejiang',postCode='330010'},['sms:001','sms:002'])];''',
#   
#         '''update my_index set name = 'lisi' ,age = 30,address={address='shanghai',postCode='330010'} where _id = 330111111;''',
#           
#         '''upsert into my_index (_id,name,age,address,message) values (330001,'zhangsan',24,{address='zhejiang',postCode='330010'},['sms:001','sms:002']);''',
#           
#         '''delete from my_test.info where _id = 330111111;''',
#         
#         
#         '''explain create table my_tb (
#             a text,b integer, 
#             c object as (
#                 raw string (index=yes,ppp=yes),
#                 obj object as (
#                     ddd string (index=yes,ppp=yes)
#                 )
#             )
#         ) with meta (
#             _parent (type='people')
#         ) with option (
#             index.number_of_shars=10,
#             index.flush_inteval='10s'
#         );''',
        ]

        for sql in sqls:
            val = parser.parse(lexer=lexer.clone(),debug=False,input=sql)
            val.debug()
            print('-----------------------华丽分割----------------------------------')
            query = Query(val)

            print(json.dumps(query.dsl(),indent=4))
                
    else: 
        val = parser.parse(lexer=lexer.clone(),debug=False,input=sys.argv[1])
        val.debug()
        print('-----------------------华丽分割----------------------------------')
        query = Query(val)
        print(json.dumps(query.dsl(),indent=4))
