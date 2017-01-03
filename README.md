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

    insert into my_index.index (name,age,address,message) values ('zhangsan',24,{address='zhejiang',postCode='330010'},['sms:001','sms:002'])


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

    python -m ql.parse.utest "select * from my_index;"


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
    )











  

