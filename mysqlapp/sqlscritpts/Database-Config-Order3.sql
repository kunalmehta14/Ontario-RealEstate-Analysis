CREATE TABLE ZillowListingsAssociations (Id BIGINT NOT NULL, Price INT, SaleStatus VARCHAR(50),
timestamp DATETIME NOT NULL, PRIMARY KEY(Id, timestamp), FOREIGN KEY (Id) REFERENCES ZillowListings(Id));

CREATE TABLE AirbnbDataAssociations (Id BIGINT NOT NULL, Price INT,
timestamp DATETIME NOT NULL, PRIMARY KEY(Id, timestamp), FOREIGN KEY (Id) REFERENCES AirbnbData(Id));

CREATE TABLE RemaxListingsAssociations (Id VARCHAR(50) NOT NULL, Price INT, SaleStatus VARCHAR(50),
timestamp DATETIME NOT NULL, PRIMARY KEY(Id, timestamp), FOREIGN KEY (Id) REFERENCES RemaxListings(Id));

CREATE TABLE YelpBusinessData (Id VARCHAR(50) NOT NULL, Categories JSON, PriceRange VARCHAR(5), 
BusinessUrl VARCHAR(2083), PRIMARY KEY(Id), FOREIGN KEY (Id) REFERENCES YelpData(Id));