USE DataAnalysis;
--- Cities Data
CREATE TABLE cities_data (city_name VARCHAR(200) NOT NULL, city_type VARCHAR(100) NOT NULL, 
division VARCHAR(100) NOT NULL, population_latest BIGINT NOT NULL, population_previous BIGINT NOT NULL, 
area BIGINT NOT NULL, PRIMARY KEY(city_name));
--- Zillow Listings
CREATE TABLE zillow_listings (id BIGINT NOT NULL, address_street VARCHAR(300) NOT NULL, 
city_name VARCHAR(100) NOT NULL, address_state VARCHAR(10), address_zipcode VARCHAR(100), 
beds INT, baths INT, price INT, listing_location JSON,
listing_type VARCHAR(50), sale_status VARCHAR(50), timestamp DATETIME NOT NULL, 
PRIMARY KEY(id), FOREIGN KEY (city_name) REFERENCES cities_data(city_name));
