import geopy.distance
import mysql.connector
import os, logging
from dotenv import find_dotenv, load_dotenv
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

#Global Logging Configuration
logging.basicConfig(filename='/var/log/amenties-calculator.log', encoding='utf-8', level=logging.DEBUG)
#This function is responsible for finding the amenties near each listing.
#It goes through the Zillow and zillow listing objects and compares the location
#data with the Schools, Universities, Colleges and Yelp data points within 10 KM range

def zillow_amenties_calculator():
  try:
    conn = mysql.connector.connect(
      host = os.getenv("MYSQL_HOST"),
      user = os.getenv("MYSQL_USER"),
      password = os.getenv("MYSQL_PASSWORD"),
      database = os.getenv("MYSQL_DATABASE"),
      port = os.getenv("MYSQL_PORT"))
    cursor = conn.cursor(buffered=True , dictionary=True)
    logging.info(f'Connection to {os.getenv("MYSQL_HOST")} server was successful')
  except Exception as e:
    logging.error(e)
  #Retrieve Zillow Listings
  try:
    zillow_query = ''' SELECT ZillowListings.Id, ZillowListings.CityName,
                      ZillowListingsWalkscore.WalkScore, ZillowListingsWalkscore.TransitScore,
                      ST_X(ZillowListings.ListingCoordinates) AS lon, 
                      ST_Y(ZillowListings.ListingCoordinates) AS lat
                      FROM ZillowListings
                      INNER JOIN ZillowListingsWalkscore ON 
                      ZillowListings.Id = ZillowListingsWalkscore.Id  
                      WHERE ZillowListingsWalkscore.WalkScore IS NOT NULL
                      AND NOT EXISTS (SELECT * FROM ZillowListingsAirbnb WHERE 
                      ZillowListingsAirbnb.Id = ZillowListings.Id)
                      AND NOT EXISTS (SELECT * FROM ZillowListingsAmeneties WHERE 
                      ZillowListingsAmeneties.Id = ZillowListings.Id)
                      AND NOT EXISTS (SELECT * FROM ZillowListingsColleges WHERE 
                      ZillowListingsColleges.Id = ZillowListings.Id)
                      AND NOT EXISTS (SELECT * FROM ZillowListingsSchools WHERE 
                      ZillowListingsSchools.Id = ZillowListings.Id)
                      AND NOT EXISTS (SELECT * FROM ZillowListingsUniversities WHERE 
                      ZillowListingsUniversities.Id = ZillowListings.Id) '''
    cursor.execute(zillow_query)
    zillow_results_set = cursor.fetchall()
    logging.info(f'Zillow listings query returned {len(zillow_results_set)} results.')
  except Exception as e:
    logging.error(e)
  #Retrieve College Data
  try:
    college_query = ''' SELECT CollegesData.CollegeName, CollegesData.CityName, ST_X(CollegesData.CollegeCoordinates) AS lon, 
                        ST_Y(CollegesData.CollegeCoordinates) AS lat FROM CollegesData '''
    cursor.execute(college_query)
    colleges_results_set = cursor.fetchall()
    logging.info(f'Colleges query returned {len(colleges_results_set)} results.')
  except Exception as e:
    logging.error(e)
  #Retrieve University Data
  try:
    university_query = ''' SELECT UniversitiesData.UniversityName, UniversitiesData.CityName, ST_X(UniversitiesData.UniversityCoordinates) AS lon, 
                        ST_Y(UniversitiesData.UniversityCoordinates) AS lat FROM UniversitiesData '''
    cursor.execute(university_query)
    universities_results_set = cursor.fetchall()
    logging.info(f'Universities query returned {len(universities_results_set)} results.')
  except Exception as e:
    logging.error(e)
  #Retrieve School Data
  try:
    school_query = ''' SELECT SchoolData.Id, SchoolData.CityName, ST_X(SchoolData.SchoolCoordinates) AS lon, 
                        ST_Y(SchoolData.SchoolCoordinates) AS lat FROM SchoolData '''
    cursor.execute(school_query)
    school_results_set = cursor.fetchall()
    logging.info(f'School query returned {len(school_results_set)} results.')
  except Exception as e:
    logging.error(e)
  #Retrieve Yelp Data
  try:
    yelp_query = ''' SELECT YelpData.Id, YelpData.CityName, ST_X(YelpData.BusinessCoordinates) AS lon, 
                    ST_Y(YelpData.BusinessCoordinates) AS lat FROM YelpData'''
    cursor.execute(yelp_query)
    yelp_results_set = cursor.fetchall()
    logging.info(f'Yelp query returned {len(yelp_results_set)} results.')
  except Exception as e:
    logging.error(e)
  #Retrieve Airbnb Data
  try:
    airbnb_query = ''' SELECT AirbnbData.Id, AirbnbData.CityName, ST_X(AirbnbData.ListingCoordinates) AS lon, 
                    ST_Y(AirbnbData.ListingCoordinates) AS lat FROM AirbnbData'''
    cursor.execute(airbnb_query)
    airbnb_results_set = cursor.fetchall()
    logging.info(f'Airbnb query returned {len(yelp_results_set)} results.')
  except Exception as e:
    logging.error(e)

  #Process Colleges Location Data
  def college_data(zillow_id, college_name, dist):
    try:
      cursor.execute(""" insert ignore into ZillowListingsColleges (Id, CollegeName, Distance)
                    values (%s, %s, %s)""",(
                    zillow_id, college_name, dist))
      conn.commit()
      logging.info(f"Zillow Listing: {zillow_id} | College: {college_name} | Distance: {dist}")
    except Exception as e:
      logging.error(e)
  for zillow_listing in zillow_results_set:
    zillow_coordinates = (zillow_listing['lon'], zillow_listing['lat'])
    for college in colleges_results_set:
      college_coordinates = (college['lon'], college['lat'])
      if college['CityName'] == zillow_listing['CityName']:
        try:
          distance = round(geopy.distance.geodesic(zillow_coordinates, college_coordinates).km, 2)
          if zillow_listing['WalkScore'] > 80:
            if distance <= 1:
              college_data(zillow_listing['Id'], college['CollegeName'], distance)
          elif zillow_listing['WalkScore'] > 50 and zillow_listing['WalkScore'] < 80:
            if distance <= 2:
              college_data(zillow_listing['Id'], college['CollegeName'], distance)
          elif zillow_listing['WalkScore'] < 50:
            if distance < 5:
              college_data(zillow_listing['Id'], college['CollegeName'], distance)
        except Exception as e:
          logging.error(e)

    #Processing Universities Location Data
    def uni_data(zillow_id, uni_name, dist):
      try:
        cursor.execute(""" insert ignore into ZillowListingsUniversities (Id, UniversityName, Distance)
                      values (%s, %s, %s)""",(
                      zillow_id, uni_name, dist))
        conn.commit()
        logging.info(f"Zillow Listing: {zillow_id} | University: {uni_name} | Distance: {dist}")
      except Exception as e:
        logging.error(e)
    for university in universities_results_set:
      university_coordinates = (university['lon'], university['lat'])
      if university['CityName'] == zillow_listing['CityName']:
        try:
          distance = round(geopy.distance.geodesic(zillow_coordinates, university_coordinates).km, 2)
          if zillow_listing['WalkScore'] > 80:
            if distance <= 1:
              uni_data(zillow_listing['Id'], university['UniversityName'], distance)
          elif zillow_listing['WalkScore'] > 50 and zillow_listing['WalkScore'] < 80:
            if distance <= 2:
              uni_data(zillow_listing['Id'], university['UniversityName'], distance)
          elif zillow_listing['WalkScore'] < 50:
            if distance < 5:
              uni_data(zillow_listing['Id'], university['UniversityName'], distance)
        except Exception as e:
          logging.error(e)

    #Processing School Location Data
    def school_data(zillow_id, school_id, dist):
      try:
        cursor.execute(""" insert ignore into ZillowListingsSchools (Id, SchoolId, Distance)
                    values (%s, %s, %s)""",(
                    zillow_id, school_id, dist))
        conn.commit()
        logging.info(f"Zillow Listing: {zillow_id} | School: {school_id} | Distance: {dist}")
      except Exception as e:
        logging.error(e)
    for school in school_results_set:
      school_coordinates = (school['lon'], school['lat'])
      if school['CityName'] == zillow_listing['CityName']:
        try:
          distance = round(geopy.distance.geodesic(zillow_coordinates, school_coordinates).km, 2)
          if zillow_listing['WalkScore'] > 80:
            if distance <= 0.5:
              school_data(zillow_listing['Id'], school['Id'], distance)
          elif zillow_listing['WalkScore'] > 50 and zillow_listing['WalkScore'] < 80:
            if distance <= 1:
              school_data(zillow_listing['Id'], school['Id'], distance)
          elif zillow_listing['WalkScore'] < 50:
            if distance < 3:
              school_data(zillow_listing['Id'], school['Id'], distance)
        except Exception as e:
          logging.error(e)

    #Processing Yelp Location Data
    def yelp_data(zillow_id, yelp_id, dist):
      try:
        cursor.execute(""" insert ignore into ZillowListingsAmeneties (Id, YelpDataId, Distance)
                    values (%s, %s, %s)""",(
                    zillow_id, yelp_id, dist))
        conn.commit()
        logging.info(f"Zillow Listing: {zillow_id} | School: {yelp_id} | Distance: {dist}")
      except Exception as e:
        logging.error(e)
        
    for yelpdata in yelp_results_set:
      yelpdata_coordinates = (yelpdata['lon'], yelpdata['lat'])
      if yelpdata['CityName'] == zillow_listing['CityName']:
        try:
          distance = round(geopy.distance.geodesic(zillow_coordinates, yelpdata_coordinates).km, 2)
          if zillow_listing['WalkScore'] > 80:
            if distance <= 0.5:
              yelp_data(zillow_listing['Id'], yelpdata['Id'], distance)
          elif zillow_listing['WalkScore'] > 50 and zillow_listing['WalkScore'] < 80:
            if distance <= 1:
              yelp_data(zillow_listing['Id'], yelpdata['Id'], distance)
          elif zillow_listing['WalkScore'] < 50:
            if distance < 2:
              yelp_data(zillow_listing['Id'], yelpdata['Id'], distance)
        except Exception as e:
          logging.error(e)

    # #Processing Airbnb Location Data
    def airbnb_data(zillow_id, airbnb_id, dist):
      try:  
        cursor.execute(""" insert ignore into ZillowListingsAirbnb (Id, AirbnbId, Distance)
                              values (%s, %s, %s)""",(
                              zillow_id, airbnb_id, dist))
        conn.commit()
        logging.info(f"zillow Listing: {zillow_id} | AirbnbListing: {airbnb_id} | Distance: {dist}")
      except Exception as e:
        logging.error(e)
    for airbnbdata in airbnb_results_set:
      airbnbdata_coordinates = (airbnbdata['lon'], airbnbdata['lat'])
      if airbnbdata['CityName'] == zillow_listing['CityName']:
        try:
          distance = round(geopy.distance.geodesic(zillow_coordinates, airbnbdata_coordinates).km, 2)
          if zillow_listing['WalkScore'] > 80:
            if distance <= 1:
              airbnb_data(zillow_listing['Id'], airbnbdata['Id'], distance)  
          elif zillow_listing['WalkScore'] > 50 and zillow_listing['WalkScore'] < 80:
            if distance <= 2:
              airbnb_data(zillow_listing['Id'], airbnbdata['Id'], distance) 
          elif zillow_listing['WalkScore'] < 50:
            if distance < 5:
              airbnb_data(zillow_listing['Id'], airbnbdata['Id'], distance) 
        except Exception as e:
          logging.error(e)

if __name__ == '__main__':
  zillow_amenties_calculator()