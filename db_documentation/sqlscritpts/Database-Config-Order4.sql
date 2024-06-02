ALTER TABLE ZillowListingsAssociations ADD INDEX (Price);

CREATE TABLE RemaxListingsDetailed (Id VARCHAR(50) NOT NULL, AgentId INT, 
AgentName VARCHAR(50), AgentOffice VARCHAR(100), AgentEmail VARCHAR(50),
AgentPhone VARCHAR(15), Basement VARCHAR(50), TaxAmount INT, Fireplace BOOLEAN,
Garage BOOLEAN, Heating VARCHAR (50), Sewer VARCHAR (50), 
SubDivision VARCHAR (50), Description VARCHAR(2083), Images JSON,
Mls VARCHAR (10)
PRIMARY KEY(Id), FOREIGN KEY (Id) REFERENCES RemaxListings(Id));

CREATE TABLE NeighborhoodData (CityName VARCHAR(200) NOT NULL, 
PostalCode VARCHAR(7) NOT NULL, Neighborhood VARCHAR(50),
Coordinates POINT, PRIMARY KEY(CityName, PostalCode),
FOREIGN KEY (CityName) REFERENCES CitiesData(CityName));