CREATE TABLE Product(
  ASIN BIGINT PRIMARY KEY,
  Id INTEGER UNIQUE NOT NULL,
  Title VARCHAR(500),
  ProductGroup VARCHAR(50),
  Salesrank INTEGER,
  AvgRating INTEGER
);

CREATE TABLE Category(
  Id INTEGER PRIMARY KEY,
  Super_Id INTEGER,
  Name VARCHAR(50),
  
  FOREIGN KEY(Super_Id) REFERENCES Category(Id)
);

CREATE TABLE ProductCategory(
  Product_ASIN BIGINT,
  Category_Id INTEGER,
  
  PRIMARY KEY(Product_ASIN, Category_Id),
  
  FOREIGN KEY(Category_Id) REFERENCES Category(Id),
  FOREIGN KEY(Product_ASIN) REFERENCES Product(ASIN)
);

CREATE TABLE SimilarProduct(
  Product_ASIN BIGINT,
  Similar_ASIN BIGINT,
  
  PRIMARY KEY(Product_ASIN, Similar_ASIN),
  
  FOREIGN KEY(Product_ASIN) REFERENCES Product(ASIN),
  FOREIGN KEY(Similar_ASIN) REFERENCES Product(ASIN)
);

CREATE TABLE Review(
  Customer VARCHAR(50),
  Product_ASIN BIGINT,
  ReviewDate DATE,
  Rating INTEGER,
  Votes INTEGER,
  Helpful INTEGER,
  
  PRIMARY KEY(Customer, Product_ASIN),
  
  FOREIGN KEY(Product_ASIN) REFERENCES Product(ASIN)
);