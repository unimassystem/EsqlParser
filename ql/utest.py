'''
Created on Dec 23, 2016

@author: qs
'''
# -*- coding: utf-8 -*- 




from ql.parse import lexer
from ql.parse import parser
from ply.lex import  lex
from ply.yacc import yacc
from ql.parse.parser import TK


from ql.dsl.Insert import Insert
from ql.dsl.Query import Query
from ql.dsl.Response import response
from ql.dsl.Create import Create
import sys
import json




def exec_query(stmt):
    
    my_lexer=lex(module=lexer,optimize=True,debug=True)
       
    my_parser=yacc(debug=True,module=parser)
    
    val = my_parser.parse(lexer=my_lexer.clone(),debug=False,input=sql)
    from elasticsearch import Elasticsearch
      
    es = Elasticsearch([{'host':"10.68.23.81","port":9201}])
    if val.get_type() == TK.TOK_QUERY:
        
        query = Query(val)
              
        res = es.search(index=query._index, doc_type = query._type, body=query.dsl(), request_timeout=100)
      
        stmt_res = response(res)
      
        print(json.dumps(stmt_res,indent=4))
        
    elif val.get_type() == TK.TOK_CREATE_TABLE:
        
        stmt = Create(val)
        
        res = es.indices.create(index=stmt._index,body = stmt._options,request_timeout=100,ignore= 400)
    
        res = es.indices.put_mapping(index = stmt._index, doc_type = stmt._type, body = stmt.dsl(), request_timeout=100)
    
        print(json.dumps(res,indent=4))
        
    elif val.get_type() == TK.TOK_INSERT_INTO:
        
        val.debug()
        
        stmt = Insert(val)
      
        res = es.index(stmt._index, stmt._type, body = stmt.dsl())
        
        print(json.dumps(res,indent=4))
        





if __name__ == "__main__":
    


    if len(sys.argv) < 2:
        sqls = [
            
#         '''create table my_tb.base (
#             a text,
#             b integer, 
#             c object as (
#                 raw string (index=yes),
#                 obj object as (
#                     ddd string (index=yes)
#                 )
#             )
#         ) with meta (
#             _parent (type='people')
#         ) with option (
#             index.number_of_shars=10,
#             index.flush_inteval='10s'
#         );''',
        
        '''create table my_index03.ccx (
            name string (analyzer = ik),
            timestamp date,
            age long
        ) with option (
            index.number_of_shards=10,
            index.number_of_replicas = 1,
            index.flush_inteval='10s'
        );''',
        
        
        '''create table my_tb.ccx (
            a string (index=no),
            c object as (
                raw string (index=not_analyzed,doc_values=false),
                obj object as (
                    ddd string (index=no)
                )
            )
        ) with meta (
            _parent (type='people'),
            _source (includes = [a,'*c'])
        ) with option (
            index.number_of_shards=10,
            index.number_of_replicas = 1,
            index.flush_inteval='10s'
        );''',
  
        '''select * from my_index limit 1,1;''', 
        
        '''select count(*) as c,count(*) as cc ,sum(dd) as dd,moving_avg({buckets_path=c,window=30,model=simple}), moving_avg({buckets_path=dd,window=30,model=simple})  
        from my_index02 
        group by name,date_histogram({field=ts,interval='1h'});''',
#        '''select * from my_index where a = hello;''',
#         '''select * from my_index where city is not null and city = '\\'my_hello\\'hello'  and city between 3717 and 3718 order by city group by 
#         data_range(a,{format='MM-yyyy'},{ranges=[{to = 'now-10M/M' },{from =  'now-10M/M'}]}),b limit 1000;''',
        
        '''select count(*) from my_index02 group by date_range({field=ts,ranges=[{to='now-10M/M',from=now},{to='now',from='now-10M/M'}]});''',
      
#        '''select * from my_index group by date_range({field=timestamp,'ranges'=[{'to'='now+10M'},{'from'='now'}]});''',

        
#        '''select sum(a) as tt from  my_index@beijing group by date_histogram({field=timestamp},{interval=day});''',

        
#        '''select sum(a) as tt,derivative({buckets_path=tt}) as the_derivative  from  my_index group by date_histogram({field=timestamp},{from=day});''',
        
#          '''select sum.a(id) as sum,a as b from test.info group by a,date_histogram(my_date,{interval='1d'},['test','ttt'],'hello world',10);''',
#   
#   

        '''insert into my_index (name,age,address,message) values ('zhangsan',24,{address='zhejiang',postCode='330010'},['sms001','sms002']);''',
        
        
        
        
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
            exec_query(sql)
                
    else: 
        sql = sys.argv[1]
        exec_query(sql)
        
        
