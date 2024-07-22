import geopy.distance
import mysql.connector
import os, logging
from dotenv import find_dotenv, load_dotenv
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

#Global Logging Configuration
logging.basicConfig(filename='/var/log/amenties-calculator.log', encoding='utf-8', level=logging.DEBUG)
#This function is responsible for finding the amenties near each listing.
#It goes through the RealEstate and RealEstate listing objects and compares the location
#data with the Schools, Universities, Colleges and Yelp data points within 10 KM range

def realestate_amenties_calculator():
  try:
    conn = mysql.connector.connect(
      host = os.getenv("MYSQL_HOST"),
      user = os.getenv("MYSQL_USER"),
      password = os.getenv("MYSQL_PASSWORD"),
      database = os.getenv("MYSQL_DATABASE"),
      port = os.getenv("MYSQL_PORT"),
      auth_plugin='mysql_native_password')
    cursor = conn.cursor(buffered=True , dictionary=True)
    logging.info(f'Connection to {os.getenv("MYSQL_HOST")} server was successful')
  except Exception as e:
    logging.error(e)
  #Retrieve RealEstate Listings
  realestate_query = ''' SELECT RealEstateListings.Id, RealEstateListings.CityName,
                    RealEstateListingsWalkscore.WalkScore, RealEstateListingsWalkscore.TransitScore,
                    ST_X(RealEstateListings.ListingCoordinates) AS lon, 
                    ST_Y(RealEstateListings.ListingCoordinates) AS lat
                    FROM RealEstateListings
                    INNER JOIN RealEstateListingsWalkscore ON 
                    RealEstateListings.Id = RealEstateListingsWalkscore.Id  
                    WHERE RealEstateListingsWalkscore.WalkScore IS NOT NULL
                    AND NOT EXISTS (SELECT * FROM RealEstateListingsAirbnb WHERE 
                    RealEstateListingsAirbnb.Id = RealEstateListings.Id)
                    AND NOT EXISTS (SELECT * FROM RealEstateListingsAmeneties WHERE 
                    RealEstateListingsAmeneties.Id = RealEstateListings.Id)
                    AND NOT EXISTS (SELECT * FROM RealEstateListingsColleges WHERE 
                    RealEstateListingsColleges.Id = RealEstateListings.Id)
                    AND NOT EXISTS (SELECT * FROM RealEstateListingsSchools WHERE 
                    RealEstateListingsSchools.Id = RealEstateListings.Id)
                    AND NOT EXISTS (SELECT * FROM RealEstateListingsUniversities WHERE 
                    RealEstateListingsUniversities.Id = RealEstateListings.Id) '''
  cursor.execute(realestate_query)
  realestate_results_set = cursor.fetchall()
  logging.info(f'RealEstate listings query returned {len(realestate_results_set)} results.')

  #Retrieve College Data
  college_query = ''' SELECT CollegesData.CollegeName, CollegesData.CityName, ST_X(CollegesData.CollegeCoordinates) AS lon, 
                      ST_Y(CollegesData.CollegeCoordinates) AS lat FROM CollegesData '''
  cursor.execute(college_query)
  colleges_results_set = cursor.fetchall()
  logging.info(f'Colleges query returned {len(colleges_results_set)} results.')

  #Retrieve University Data
  university_query = ''' SELECT UniversitiesData.UniversityName, UniversitiesData.CityName, ST_X(UniversitiesData.UniversityCoordinates) AS lon, 
                      ST_Y(UniversitiesData.UniversityCoordinates) AS lat FROM UniversitiesData '''
  cursor.execute(university_query)
  universities_results_set = cursor.fetchall()
  logging.info(f'Universities query returned {len(universities_results_set)} results.')
  
  #Retrieve School Data
  school_query = ''' SELECT SchoolData.Id, SchoolData.CityName, ST_X(SchoolData.SchoolCoordinates) AS lon, 
                      ST_Y(SchoolData.SchoolCoordinates) AS lat FROM SchoolData '''
  cursor.execute(school_query)
  school_results_set = cursor.fetchall()
  logging.info(f'School query returned {len(school_results_set)} results.')

  #Retrieve Yelp Data
  yelp_query = ''' SELECT YelpData.Id, YelpData.CityName, ST_X(YelpData.BusinessCoordinates) AS lon, 
                  ST_Y(YelpData.BusinessCoordinates) AS lat FROM YelpData'''
  cursor.execute(yelp_query)
  yelp_results_set = cursor.fetchall()
  logging.info(f'Yelp query returned {len(yelp_results_set)} results.')

  #Retrieve Airbnb Data
  airbnb_query = ''' SELECT AirbnbData.Id, AirbnbData.CityName, ST_X(AirbnbData.ListingCoordinates) AS lon, 
                  ST_Y(AirbnbData.ListingCoordinates) AS lat FROM AirbnbData'''
  cursor.execute(airbnb_query)
  airbnb_results_set = cursor.fetchall()
  logging.info(f'Airbnb query returned {len(yelp_results_set)} results.')

  #Process Colleges Location Data
  def college_data(realestate_id, college_name, dist):
    try:
      cursor.execute(""" insert ignore into RealEstateListingsColleges (Id, CollegeName, Distance)
                    values (%s, %s, %s)""",(
                    realestate_id, college_name, dist))
      conn.commit()
      logging.info(f"RealEstate Listing: {realestate_id} | College: {college_name} | Distance: {dist}")
    except Exception as e:
      logging.error(e)
  for realestate_listing in realestate_results_set:
    realestate_coordinates = (realestate_listing['lon'], realestate_listing['lat'])
    for college in colleges_results_set:
      college_coordinates = (college['lon'], college['lat'])
      if college['CityName'] == realestate_listing['CityName']:
        try:
          distance = round(geopy.distance.geodesic(realestate_coordinates, college_coordinates).km, 2)
          if realestate_listing['WalkScore'] > 80:
            if distance <= 1:
              college_data(realestate_listing['Id'], college['CollegeName'], distance)
          elif realestate_listing['WalkScore'] > 50 and realestate_listing['WalkScore'] < 80:
            if distance <= 2:
              college_data(realestate_listing['Id'], college['CollegeName'], distance)
          elif realestate_listing['WalkScore'] < 50:
            if distance < 5:
              college_data(realestate_listing['Id'], college['CollegeName'], distance)
        except Exception as e:
          logging.error(e)

    #Processing Universities Location Data
    def uni_data(realestate_id, uni_name, dist):
      try:
        cursor.execute(""" insert ignore into RealEstateListingsUniversities (Id, UniversityName, Distance)
                      values (%s, %s, %s)""",(
                      realestate_id, uni_name, dist))
        conn.commit()
        logging.info(f"RealEstate Listing: {realestate_id} | University: {uni_name} | Distance: {dist}")
      except Exception as e:
        logging.error(e)
    for university in universities_results_set:
      university_coordinates = (university['lon'], university['lat'])
      if university['CityName'] == realestate_listing['CityName']:
        try:
          distance = round(geopy.distance.geodesic(realestate_coordinates, university_coordinates).km, 2)
          if realestate_listing['WalkScore'] > 80:
            if distance <= 1:
              uni_data(realestate_listing['Id'], university['UniversityName'], distance)
          elif realestate_listing['WalkScore'] > 50 and realestate_listing['WalkScore'] < 80:
            if distance <= 2:
              uni_data(realestate_listing['Id'], university['UniversityName'], distance)
          elif realestate_listing['WalkScore'] < 50:
            if distance < 5:
              uni_data(realestate_listing['Id'], university['UniversityName'], distance)
        except Exception as e:
          logging.error(e)

    #Processing School Location Data
    def school_data(realestate_id, school_id, dist):
      try:
        cursor.execute(""" insert ignore into RealEstateListingsSchools (Id, SchoolId, Distance)
                    values (%s, %s, %s)""",(
                    realestate_id, school_id, dist))
        conn.commit()
        logging.info(f"RealEstate Listing: {realestate_id} | School: {school_id} | Distance: {dist}")
      except Exception as e:
        logging.error(e)
    for school in school_results_set:
      school_coordinates = (school['lon'], school['lat'])
      if school['CityName'] == realestate_listing['CityName']:
        try:
          distance = round(geopy.distance.geodesic(realestate_coordinates, school_coordinates).km, 2)
          if realestate_listing['WalkScore'] > 80:
            if distance <= 0.5:
              school_data(realestate_listing['Id'], school['Id'], distance)
          elif realestate_listing['WalkScore'] > 50 and realestate_listing['WalkScore'] < 80:
            if distance <= 1:
              school_data(realestate_listing['Id'], school['Id'], distance)
          elif realestate_listing['WalkScore'] < 50:
            if distance < 3:
              school_data(realestate_listing['Id'], school['Id'], distance)
        except Exception as e:
          logging.error(e)

    #Processing Yelp Location Data
    def yelp_data(realestate_id, yelp_id, dist):
      try:
        cursor.execute(""" insert ignore into RealEstateListingsAmeneties (Id, YelpDataId, Distance)
                    values (%s, %s, %s)""",(
                    realestate_id, yelp_id, dist))
        conn.commit()
        logging.info(f"RealEstate Listing: {realestate_id} | School: {yelp_id} | Distance: {dist}")
      except Exception as e:
        logging.error(e)
        
    for yelpdata in yelp_results_set:
      yelpdata_coordinates = (yelpdata['lon'], yelpdata['lat'])
      if yelpdata['CityName'] == realestate_listing['CityName']:
        try:
          distance = round(geopy.distance.geodesic(realestate_coordinates, yelpdata_coordinates).km, 2)
          if realestate_listing['WalkScore'] > 80:
            if distance <= 0.5:
              yelp_data(realestate_listing['Id'], yelpdata['Id'], distance)
          elif realestate_listing['WalkScore'] > 50 and realestate_listing['WalkScore'] < 80:
            if distance <= 1:
              yelp_data(realestate_listing['Id'], yelpdata['Id'], distance)
          elif realestate_listing['WalkScore'] < 50:
            if distance < 2:
              yelp_data(realestate_listing['Id'], yelpdata['Id'], distance)
        except Exception as e:
          logging.error(e)

    # #Processing Airbnb Location Data
    def airbnb_data(realestate_id, airbnb_id, dist):
      try:  
        cursor.execute(""" insert ignore into RealEstateListingsAirbnb (Id, AirbnbId, Distance)
                              values (%s, %s, %s)""",(
                              realestate_id, airbnb_id, dist))
        conn.commit()
        logging.info(f"RealEstate Listing: {realestate_id} | AirbnbListing: {airbnb_id} | Distance: {dist}")
      except Exception as e:
        logging.error(e)
    for airbnbdata in airbnb_results_set:
      airbnbdata_coordinates = (airbnbdata['lon'], airbnbdata['lat'])
      if airbnbdata['CityName'] == realestate_listing['CityName']:
        try:
          distance = round(geopy.distance.geodesic(realestate_coordinates, airbnbdata_coordinates).km, 2)
          if realestate_listing['WalkScore'] > 80:
            if distance <= 1:
              airbnb_data(realestate_listing['Id'], airbnbdata['Id'], distance)  
          elif realestate_listing['WalkScore'] > 50 and realestate_listing['WalkScore'] < 80:
            if distance <= 2:
              airbnb_data(realestate_listing['Id'], airbnbdata['Id'], distance) 
          elif realestate_listing['WalkScore'] < 50:
            if distance < 5:
              airbnb_data(realestate_listing['Id'], airbnbdata['Id'], distance) 
        except Exception as e:
          logging.error(e)

if __name__ == '__main__':
  realestate_amenties_calculator()