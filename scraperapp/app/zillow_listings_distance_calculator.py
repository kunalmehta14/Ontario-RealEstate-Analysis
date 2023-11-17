import geopy.distance
import mysql.connector
import os
from dotenv import find_dotenv, load_dotenv
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

#This function is responsible for finding the amenties near each listing.
#It goes through the Zillow listing objects and compares the location
#data with the Schools, Universities, Colleges and Yelp data points within 10 KM range
conn = mysql.connector.connect(
  host = os.getenv("MYSQL_HOST"),
  user = os.getenv("MYSQL_USER"),
  password = os.getenv("MYSQL_PASSWORD"),
  database = 'DataAnalysis',
  port = '3306')
cursor = conn.cursor(buffered=True , dictionary=True)
#Retrieve Zillow Listings
zillow_query = ''' SELECT ZillowListings.Id, ZillowListings.CityName,
                    ZillowListingsWalkscore.WalkScore, ZillowListingsWalkscore.TransitScore,
                    ST_X(ZillowListings.ListingCoordinates) AS lon, 
                    ST_Y(ZillowListings.ListingCoordinates) AS lat
                    FROM ZillowListings
                    INNER JOIN ZillowListingsWalkscore ON 
                    ZillowListings.Id = ZillowListingsWalkscore.Id '''
cursor.execute(zillow_query)
zillow_results_set = cursor.fetchall()
#Retrieve College Data
college_query = ''' SELECT CollegesData.CollegeName, CollegesData.CityName, ST_X(CollegesData.CollegeCoordinates) AS lon, 
                    ST_Y(CollegesData.CollegeCoordinates) AS lat FROM CollegesData '''
cursor.execute(college_query)
colleges_results_set = cursor.fetchall()
#Retrieve University Data
university_query = ''' SELECT UniversitiesData.UniversityName, UniversitiesData.CityName, ST_X(UniversitiesData.UniversityCoordinates) AS lon, 
                    ST_Y(UniversitiesData.UniversityCoordinates) AS lat FROM UniversitiesData '''
cursor.execute(university_query)
universities_results_set = cursor.fetchall()
#Retrieve School Data
school_query = ''' SELECT SchoolData.Id, SchoolData.CityName, ST_X(SchoolData.SchoolCoordinates) AS lon, 
                    ST_Y(SchoolData.SchoolCoordinates) AS lat FROM SchoolData '''
cursor.execute(school_query)
school_results_set = cursor.fetchall()
#Retrieve Yelp Data
yelp_query = ''' SELECT YelpData.Id, YelpData.CityName, ST_X(YelpData.BusinessCoordinates) AS lon, 
                ST_Y(YelpData.BusinessCoordinates) AS lat FROM YelpData'''
cursor.execute(yelp_query)
yelp_results_set = cursor.fetchall()
#Retrieve Airbnb Data
airbnb_query = ''' SELECT AirbnbData.Id, AirbnbData.CityName, ST_X(AirbnbData.ListingCoordinates) AS lon, 
                ST_Y(AirbnbData.ListingCoordinates) AS lat FROM AirbnbData'''
cursor.execute(airbnb_query)
airbnb_results_set = cursor.fetchall()

#Process Location Data
for zillow_listing in zillow_results_set:
  zillow_coordinates = (zillow_listing['lat'], zillow_listing['lon'])
  for college in colleges_results_set:
    college_coordinates = (college['lat'], college['lon'])
    if college['CityName'] == zillow_listing['CityName']:
      try:
        distance = round(geopy.distance.geodesic(zillow_coordinates, college_coordinates).km, 2)
        if zillow_listing['WalkScore'] > 80:
          if distance <= 1:
            cursor.execute(""" insert ignore into ZillowListingsColleges (Id, CollegeName, Distance)
                          values (%s, %s, %s)""",(
                          zillow_listing['Id'], college['CollegeName'], distance))
            conn.commit()
        elif zillow_listing['WalkScore'] > 50 and zillow_listing['WalkScore'] < 80:
          if distance <= 2:
            cursor.execute(""" insert ignore into ZillowListingsColleges (Id, CollegeName, Distance)
                          values (%s, %s, %s)""",(
                          zillow_listing['Id'], college['CollegeName'], distance))
            conn.commit()
        elif zillow_listing['WalkScore'] < 50:
          if distance < 5:
            cursor.execute(""" insert ignore into ZillowListingsColleges (Id, CollegeName, Distance)
                          values (%s, %s, %s)""",(
                          zillow_listing['Id'], college['CollegeName'], distance))
            conn.commit()
      except:
        pass
  #Processing Universities Location Data
  for university in universities_results_set:
    university_coordinates = (university['lat'], university['lon'])
    if university['CityName'] == zillow_listing['CityName']:
      try:
        distance = round(geopy.distance.geodesic(zillow_coordinates, university_coordinates).km, 2)
        if zillow_listing['WalkScore'] > 80:
          if distance <= 1:
            cursor.execute(""" insert ignore into ZillowListingsUniversities (Id, UniversityName, Distance)
                          values (%s, %s, %s)""",(
                          zillow_listing['Id'], university['UniversityName'], distance))
            conn.commit()
        elif zillow_listing['WalkScore'] > 50 and zillow_listing['WalkScore'] < 80:
          if distance <= 2:
            cursor.execute(""" insert ignore into ZillowListingsUniversities (Id, UniversityName, Distance)
                          values (%s, %s, %s)""",(
                          zillow_listing['Id'], university['UniversityName'], distance))
            conn.commit()
        elif zillow_listing['WalkScore'] < 50:
          if distance < 5:
            cursor.execute(""" insert ignore into ZillowListingsUniversities (Id, UniversityName, Distance)
                          values (%s, %s, %s)""",(
                          zillow_listing['Id'], university['UniversityName'], distance))
            conn.commit()
      except:
        pass
  #Processing School Location Data
  for school in school_results_set:
    school_coordinates = (school['lat'], school['lon'])
    if school['CityName'] == zillow_listing['CityName']:
      try:
        distance = round(geopy.distance.geodesic(zillow_coordinates, school_coordinates).km, 2)
        if zillow_listing['WalkScore'] > 80:
          if distance <= 1:
              cursor.execute(""" insert ignore into ZillowListingsSchools (Id, SchoolId, Distance)
                          values (%s, %s, %s)""",(
                          zillow_listing['Id'], school['SchoolId'], distance))
              conn.commit()
        elif zillow_listing['WalkScore'] > 50 and zillow_listing['WalkScore'] < 80:
          if distance <= 2:
              cursor.execute(""" insert ignore into ZillowListingsSchools (Id, SchoolId, Distance)
                          values (%s, %s, %s)""",(
                          zillow_listing['Id'], school['SchoolId'], distance))
              conn.commit()
        elif zillow_listing['WalkScore'] < 50:
          if distance < 5:
              cursor.execute(""" insert ignore into ZillowListingsSchools (Id, SchoolId, Distance)
                          values (%s, %s, %s)""",(
                          zillow_listing['Id'], school['SchoolId'], distance))
              conn.commit()
      except:
        pass
  #Processing Yelp Location Data
  for yelpdata in yelp_results_set:
    yelpdata_coordinates = (yelpdata['lat'], yelpdata['lon'])
    if yelpdata['CityName'] == zillow_listing['CityName']:
      try:
        distance = round(geopy.distance.geodesic(zillow_coordinates, yelpdata_coordinates).km, 2)
        if zillow_listing['WalkScore'] > 80:
          if distance <= 1:
              cursor.execute(""" insert ignore into ZillowListingsAmeneties (Id, YelpDataId, Distance)
                          values (%s, %s, %s)""",(
                          zillow_listing['Id'], yelpdata['Id'], distance))
              conn.commit()
        elif zillow_listing['WalkScore'] > 50 and zillow_listing['WalkScore'] < 80:
          if distance <= 2:
              cursor.execute(""" insert ignore into ZillowListingsAmeneties (Id, YelpDataId, Distance)
                          values (%s, %s, %s)""",(
                          zillow_listing['Id'], yelpdata['Id'], distance))
              conn.commit()
        elif zillow_listing['WalkScore'] < 50:
          if distance < 5:
              cursor.execute(""" insert ignore into ZillowListingsAmeneties (Id, YelpDataId, Distance)
                          values (%s, %s, %s)""",(
                          zillow_listing['Id'], yelpdata['Id'], distance))
              conn.commit()
      except:
        pass
  #Processing Airbnb Location Data
  for airbnbdata in airbnb_results_set:
    airbnbdata_coordinates = (airbnbdata['lat'], airbnbdata['lon'])
    if airbnbdata['CityName'] == zillow_listing['CityName']:
      try:
        distance = round(geopy.distance.geodesic(zillow_coordinates, airbnbdata_coordinates).km, 2)
        if zillow_listing['WalkScore'] > 80:
          if distance <= 1:
              cursor.execute(""" insert ignore into ZillowListingsAmeneties (Id, AirbnbDataId, Distance)
                          values (%s, %s, %s)""",(
                          zillow_listing['Id'], airbnbdata['Id'], distance))
              conn.commit()
        elif zillow_listing['WalkScore'] > 50 and zillow_listing['WalkScore'] < 80:
          if distance <= 2:
              cursor.execute(""" insert ignore into ZillowListingsAmeneties (Id, AirbnbDataId, Distance)
                          values (%s, %s, %s)""",(
                          zillow_listing['Id'], airbnbdata['Id'], distance))
              conn.commit()
        elif zillow_listing['WalkScore'] < 50:
          if distance < 5:
              cursor.execute(""" insert ignore into ZillowListingsAmeneties (Id, AirbnbDataId, Distance)
                          values (%s, %s, %s)""",(
                          zillow_listing['Id'], airbnbdata['Id'], distance))
              conn.commit()
      except:
        pass