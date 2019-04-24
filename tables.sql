-- users table
CREATE TABLE users  
( name varchar2(35) NOT NULL,  
  username varchar2(20) NOT NULL,  
  password varchar2(100)  NOT NULL
);  

CREATE TABLE products  
( category varchar2(15) NOT NULL,  
  name varchar2(50) NOT NULL,
  code varchar2(20) NOT NULL,
  type varchar2(15) NOT NULL,
  color varchar2(15) NOT NULL,
  sizee varchar2(15) ,
  price number NOT NULL,
  quantity number NOT NULL,  
  description varchar2(100)  NOT NULL,
  uploaddate timestamp default systimestamp,
  pic1 varchar2(70)  NOT NULL,
  pic2 varchar2(70)  ,
  pic3 varchar2(70)  
);

INSERT INTO products(category , name , code , type, color,
         sizee , price , quantity , description , pic1 , pic2 , pic3 ) 
         VALUES('category' , 'name' , 'code' , 'type', 'color',
         'sizee' , 40 , 10 , 'description', 'pic1' , 'pic2' , 'pic3')
