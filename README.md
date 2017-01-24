#Esql

Features include
----------------

Familiar SQL syntax::

    select * from my_index.my_type;
    select count(*) from my_index.my_table group by age;
    create table my_index.my_table (
         id string,
         name string,
         birthday date
    );

Support structured data::

    create table my_index.my_table (
         id string,
         name string,
         obj object as (
             first_name string,
             second_name string
         )
    );
    
    Insert into my_index.index (id,name,obj)  (1001,'unimas',{address='zhejiang',postCode='330010'});
    
    Insert into my_index.index (id,name,list)  (1001,'unimas',['message 1','message 2']);


Support Upsert::

    upsert into my_index (_id,name,age,address,message) values (330001,'zhangsan',24,{address='zhejiang',postCode='330010'},['sms:001','sms:002']);



##Create table::

syntax:

    create table [my_index]<.my_table> (
         [column] [type] [(option = value)] [AS] (
             [column] [type] [(option = value)] 
         ),
         ...
    );


example:

    create table my_index.my_table (
         id string,
         name string (analyzer=ik),
         birthday date (doc_values=true)
    );


structured data:

    create table my_index.my_table (
         id string,
         name string,
         obj object as (
             first_name string,
             second_name string
         )
    );


##Query

syntax:

    SELECT selexpr FROM [my_index]<.my_table> [WHERE EXPRESSION] [LIMIT from,size] [ORDER BY column desc/asc] 

example:

    select * from my_table;	
    select * from my_table.my_idex order by timestamp limit 100,10;
    select * from my_table.my_index where name like 'john *' and age between 20 and 30 and (hotel = 'hanting' or flight = 'MH4510');


##Aggregations
    SELECT Metrices_FUN FROM [my_index]<.my_table> [WHERE EXPRESSION]  [GROUP BY Buckets]

example:

    select * from my_table.my_index group by code;
    select * from my_table.my_index group by range(age,{to=10},{from=10,to=20},{from=20});
    select * from my_table.my_index group by date_histogram(timestamp,{interval=12h});


##Insert
	INSERT INTO [my_index]<.my_table> [colums] VALUES [row values]

example:

    insert into my_index.index (name,age,address,message) values ('zhangsan',24,{address='zhejiang',postCode='330010'},['sms:001','sms:002']);


##Update
	UPDATE [my_index]<.my_table>  SET [column=value,...] WHERE [_id = xxxx] and < _route/_parent = xxxx >

example:

    update my_index set name = 'lisi' ,age = 30,address={address='shanghai',postCode='330010'} where _id = 330111111;
    
    
##Upsert
    Upsert INTO [my_index]<.my_table> [colums] VALUES [row values]; #_id is not null

example:

    upsert into my_index (_id,name,age,address,message) values (330001,'zhangsan',24,{address='zhejiang',postCode='330010'},['sms:001','sms:002']);
        

#Getting Started

Requirement python3.5,Install Yacc/Lex first:

     pip install ply
     
or:
     
     wget http://www.dabeaz.com/ply/ply-3.9.tar.gz
     tar ply-3.9.tar.gz
     cd ply-3.9
     python setup.py install
     
##Test Sql Parse

Console:

    python -m python -m ql.utest "select * from my_index where age >= 20;"


	(TOK_QUERY
		(TOK_SELECT
			(TOK_SELEXPR
				(TOK_VALUE
					*
				)
			)
		)
		(TOK_FROM
			(TOK_TABLE_NAME
				(TOK_VALUE
					my_index
				)
			)
		)
		(TOK_WHERE
			(TOK_COMPARE
				>=
				(TOK_EXPRESSION_LEFT
					(TOK_VALUE
						age
					)
				)
				(TOK_EXPRESSION_RIGHT
					(TOK_VALUE
						20
					)
				)
			)
		)
	)
	-----------------------华丽分割----------------------------------
	{
	    "query": {
	        "bool": {
	            "must": [
	                {
	                    "range": {
	                        "age": {
	                            "gte": "20"
	                        }
	                    }
	                }
	            ]
	        }
	    },
	    "_source": [
	        "*"
	    ]
	}












  

