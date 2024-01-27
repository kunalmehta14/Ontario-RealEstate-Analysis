CREATE TABLE ZillowListings (Id BIGINT NOT NULL, `Address` VARCHAR(300) NOT NULL,
AddressStreet VARCHAR(300) NOT NULL, CityName VARCHAR(100) NOT NULL, 
Beds INT, Baths INT, ListingCoordinates POINT NOT NULL, 
ListingType VARCHAR(50), ListingUrl VARCHAR(2083),
PRIMARY KEY(Id), FOREIGN KEY (CityName) REFERENCES CitiesData(CityName));

CREATE TABLE RemaxListings (Id VARCHAR(50) NOT NULL,
AddressStreet VARCHAR(300) NOT NULL, CityName VARCHAR(100) NOT NULL, 
Beds INT, Baths INT, ListingCoordinates POINT NOT NULL, ListingType VARCHAR(50),
ListingDate DATETIME, Area INT, ListingUrl VARCHAR(2083),
PRIMARY KEY(Id), FOREIGN KEY (CityName) REFERENCES CitiesData(CityName));

CREATE TABLE YelpData (Id VARCHAR(50) NOT NULL, BusinessName VARCHAR(300), 
Rating DECIMAL (1,1), Reviews INT, BusinessAddress VARCHAR(300), 
CityName VARCHAR(100) NOT NULL, BusinessCoordinates POINT NOT NULL, 
PRIMARY KEY(Id), FOREIGN KEY (CityName) REFERENCES CitiesData(CityName));

CREATE TABLE AirbnbData (Id BIGINT NOT NULL, ListingName VARCHAR(300),
ListingObjType VARCHAR(20), CityName VARCHAR(100) NOT NULL, 
ListingCoordinates POINT NOT NULL, RoomTypeCategory VARCHAR(20),
PRIMARY KEY(Id), FOREIGN KEY (CityName) REFERENCES CitiesData(CityName));

CREATE TABLE SchoolData (Id BIGINT NOT NULL, SchoolName VARCHAR(100) NOT NULL, 
SchoolAddress VARCHAR(300) NOT NULL, SchoolCoordinates POINT NOT NULL,
CityName VARCHAR(100) NOT NULL, PRIMARY KEY(Id), FOREIGN KEY (CityName) REFERENCES CitiesData(CityName));

CREATE TABLE CollegesData (CollegeName VARCHAR(100) NOT NULL, CityName VARCHAR(100) NOT NULL,
CollegeAddress VARCHAR(300) NOT NULL, CollegeCoordinates POINT NOT NULL, 
PRIMARY KEY(CollegeName, CityName), FOREIGN KEY (CityName) REFERENCES CitiesData(CityName));

CREATE TABLE UniversitiesData (UniversityName VARCHAR(100) NOT NULL, CityName VARCHAR(100) NOT NULL,
UniversityAddress VARCHAR(300) NOT NULL, UniversityCoordinates POINT NOT NULL, 
PRIMARY KEY(UniversityName, CityName), FOREIGN KEY (CityName) REFERENCES CitiesData(CityName));

CREATE TABLE MortgageData (LenderName VARCHAR(100) NOT NULL, Variable FLOAT, SixMonths FLOAT,
OneYear FLOAT, TwoYears FLOAT, ThreeYears FLOAT, FourYears FLOAT, FiveYears FLOAT, 
timestamp DATETIME NOT NULL, PRIMARY KEY(LenderName, timestamp));