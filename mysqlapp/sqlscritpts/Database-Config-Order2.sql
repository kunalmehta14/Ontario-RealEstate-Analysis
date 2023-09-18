USE DataAnalysis;

CREATE TABLE ZillowListings (Id BIGINT NOT NULL, `Address` VARCHAR(300) NOT NULL, 
CityName VARCHAR(100) NOT NULL, Beds INT, Baths INT, Price INT, ListingLat  FLOAT,
ListingLon  FLOAT, ListingType VARCHAR(50), SaleStatus VARCHAR(50), timestamp DATETIME NOT NULL, 
PRIMARY KEY(Id), FOREIGN KEY (CityName) REFERENCES CitiesData(CityName));

CREATE TABLE YelpData (Id BIGINT NOT NULL, BusinessName VARCHAR(300) NOT NULL, 
Rating INT, Reviews INT, Categories JSON, BusinessLat FLOAT NOT NULL, BusinessLon FLOAT NOT NULL, 
AddressState VARCHAR(10), CityName VARCHAR(100) NOT NULL, timestamp DATETIME NOT NULL, 
PRIMARY KEY(Id), FOREIGN KEY (CityName) REFERENCES CitiesData(CityName));

CREATE TABLE SchoolData (Id BIGINT NOT NULL, SchoolName VARCHAR(100) NOT NULL, 
SchoolAddress VARCHAR(300) NOT NULL, SchoolLat FLOAT NOT NULL, 
SchoolLon FLOAT NOT NULL, CityName VARCHAR(100) NOT NULL,
PRIMARY KEY(Id), FOREIGN KEY (CityName) REFERENCES CitiesData(CityName));

CREATE TABLE CollegesData (CollegeName VARCHAR(100) NOT NULL, CityName VARCHAR(100) NOT NULL,
CollegeAddress VARCHAR(300) NOT NULL, CollegeLat FLOAT NOT NULL, CollegeLon FLOAT NOT NULL, 
PRIMARY KEY(CollegeName, CityName), FOREIGN KEY (CityName) REFERENCES CitiesData(CityName));

CREATE TABLE UniversitiesData (UniversityName VARCHAR(100) NOT NULL, CityName VARCHAR(100) NOT NULL,
UniversityAddress VARCHAR(300) NOT NULL, UniversityLat FLOAT NOT NULL, UniversityLon FLOAT NOT NULL, 
PRIMARY KEY(UniversityName, CityName), FOREIGN KEY (CityName) REFERENCES CitiesData(CityName));

CREATE TABLE MortgageData (LenderName VARCHAR(100) NOT NULL, Variable INT, SixMonths INT,
OneYear INT, TwoYears INT, ThreeYears INT, FourYears INT, FiveYears INT, 
timestamp DATETIME NOT NULL, PRIMARY KEY(LenderName, timestamp));