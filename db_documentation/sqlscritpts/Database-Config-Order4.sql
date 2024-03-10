ALTER TABLE ZillowListingsAssociations ADD INDEX (Price);

CREATE TABLE RemaxListingsDetailed (Id VARCHAR(50) NOT NULL, AgentId INT, 
AgentName VARCHAR(50), AgentOffice VARCHAR(100), AgentEmail VARCHAR(50),
AgentPhone VARCHAR(15), Basement VARCHAR(50), TaxAmount INT, Fireplace BOOLEAN,
Garage BOOLEAN, Heating VARCHAR (50), Sewer VARCHAR (50), 
SubDivision VARCHAR (50), Description VARCHAR(2083), Images JSON,
PRIMARY KEY(Id), FOREIGN KEY (Id) REFERENCES RemaxListings(Id));