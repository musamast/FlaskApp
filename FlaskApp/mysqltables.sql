-- users table
CREATE TABLE admins  
( id INT(11) AUTO_INCREMENT PRIMARY KEY,
    name varchar(30) NOT NULL,  
  username varchar(30) NOT NULL,
  email varchar(30) NOT NULL,  
  password varchar(100)  NOT NULL
);  

CREATE TABLE products  
( category varchar(15) NOT NULL,  
  name varchar(50) NOT NULL,
  code varchar(20) NOT NULL PRIMARY KEY,
  type varchar(15) NOT NULL,
  color varchar(15) NOT NULL,
  sizee varchar(15) ,
  price int NOT NULL,
  quantity int NOT NULL,  
  description varchar(200)  NOT NULL,
  uploaddate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  pic1 varchar(70)  NOT NULL,
  pic2 varchar(70)  ,
  pic3 varchar(70)  
);
CREATE TABLE visitedusers( id INT(11) AUTO_INCREMENT PRIMARY KEY,
    ip VARCHAR(35) NOT NULL,
    link VARCHAR(70) NOT NULL,  
  timee VARCHAR(35) NOT NULL,  
  datee VARCHAR(35 ) NOT NULL
); 
CREATE TABLE customers  
( id INT(11) AUTO_INCREMENT PRIMARY KEY,
    name varchar(30) NOT NULL,  
  username varchar(30) NOT NULL,
  email varchar(30) NOT NULL,  
  password varchar(100)  NOT NULL
);

INSERT INTO products(category , name , code , type, color,
         sizee , price , quantity , description , pic1 , pic2 , pic3 ) 
         VALUES('category' , 'name' , 'code' , 'type', 'color',
         'sizee' , 40 , 10 , 'description', 'pic1' , 'pic2' , 'pic3')
