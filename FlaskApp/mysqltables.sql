-- admin table
CREATE TABLE admins  
( id INT(11) AUTO_INCREMENT PRIMARY KEY,
    name varchar(30) NOT NULL,  
  username varchar(30) NOT NULL,
  email varchar(30) NOT NULL,  
  password varchar(100)  NOT NULL
);  


-- product table
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
  pic1 varchar(70),
  pic2 varchar(70)  ,
  pic3 varchar(70)  
);


-- visited users'ip table
CREATE TABLE visitedusers( id INT(11) AUTO_INCREMENT PRIMARY KEY,
    ip VARCHAR(35) NOT NULL,
    link VARCHAR(70) NOT NULL,  
  timee VARCHAR(35) NOT NULL,  
  datee VARCHAR(35 ) NOT NULL
);


-- customer table
CREATE TABLE customers  
( id INT(11) AUTO_INCREMENT PRIMARY KEY,
    name varchar(30) NOT NULL,  
  username varchar(30) NOT NULL,
  email varchar(30) NOT NULL,  
  password varchar(100)  NOT NULL
);


-- Invoice table
CREATE TABLE invoice
( orderid INT(25) PRIMARY KEY NOT NULL,  
  customerid INT(11) NOT NULL ,
  city VARCHAR(20) NOT NULL,
  address VARCHAR(100) NOT NULL,
  orderdate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  totalamount INT(25) NOT NULL,
  deliverystatus VARCHAR(10) NOT NULL,
  delivereddate DATE,
    FOREIGN KEY (customerid)
   REFERENCES customers(id)
     ON DELETE CASCADE  
);


-- orders table
CREATE TABLE orders
( orderid INT(25) NOT NULL,  
  productid VARCHAR(20) NOT NULL ,
  quantity INT(11) NOT NULL,
  size varchar(15) ,
  sellingprice INT(20) NOT NULL,
  costprice INT(20) NOT NULL,
  color VARCHAR(15),
  CONSTRAINT PK_orders PRIMARY KEY (orderid,productid),
    FOREIGN KEY (productid)
   REFERENCES products(CODE)
     ON DELETE CASCADE  
);


CREATE TABLE popularproduct(
 id INT(11) AUTO_INCREMENT PRIMARY KEY,
    productid  VARCHAR(20) NOT NULL,  
  category VARCHAR(15) NOT NULL,  
  yearr VARCHAR(10) NOT NULL,
  FOREIGN KEY (productid)
   REFERENCES products(CODE)
     ON DELETE CASCADE
);

CREATE TABLE frequentcustomers(
 id INT(11) AUTO_INCREMENT PRIMARY KEY,
    customerid  INT(11) NOT NULL ,
    NAME VARCHAR(30) NOT NULL,  
  yearr VARCHAR(10) NOT NULL,
   FOREIGN KEY (customerid)
   REFERENCES customers(id)
     ON DELETE CASCADE  
);
CREATE TABLE revenuegeneratedcustomers(
 id INT(11) AUTO_INCREMENT PRIMARY KEY,
    customerid  INT(11) NOT NULL ,
    NAME VARCHAR(30) NOT NULL,  
  yearr VARCHAR(10) NOT NULL,
   FOREIGN KEY (customerid)
   REFERENCES customers(id)
     ON DELETE CASCADE  
);