CREATE TABLE ZillowListingsAssociations (Id BIGINT NOT NULL, Price INT, SaleStatus VARCHAR(50),
timestamp DATETIME NOT NULL, PRIMARY KEY(Id, timestamp), FOREIGN KEY (Id) REFERENCES ZillowListings(Id));

CREATE TABLE AirbnbDataAssociations (Id BIGINT NOT NULL, Price INT,
timestamp DATETIME NOT NULL, PRIMARY KEY(Id, timestamp), FOREIGN KEY (Id) REFERENCES AirbnbData(Id));