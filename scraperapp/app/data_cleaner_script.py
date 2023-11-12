import os
import mysql.connector
from geopy.geocoders import Bing
from dotenv import find_dotenv, load_dotenv
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

#When scraping Yelp Data, the cities names sometimes won't match the city, municipality and township names
#collected using Wikipedia. To fix the citynames, this script can be used.
conn = mysql.connector.connect(
    host = os.getenv("MYSQL_HOST"),
    user = os.getenv("MYSQL_USER"),
    password = os.getenv("MYSQL_PASSWORD"),
    database = 'DataAnalysis',
    port = '3306')
cursor = conn.cursor(buffered=True , dictionary=True)

query = ''' SELECT ST_X(YelpData.BusinessCoordinates) AS lon, ST_Y(YelpData.BusinessCoordinates) AS lat FROM YelpData LEFT JOIN CitiesData ON YelpData.CityName = CitiesData.CityName WHERE CitiesData.CityName IS NULL '''
cursor.execute(query)
result_set = cursor.fetchall()

for result in result_set:
    lat = result['lat']
    lon = result['lon']
    coordinates = [lon, lat]
    g = Bing(api_key=os.getenv("BING_MAPS_API"))
    location = g.reverse(coordinates)
    city = location.raw['address']['locality']
    try:
        cursor.execute(""" SET FOREIGN_KEY_CHECKS=0 """)
        query = ''' UPDATE YelpData SET CityName = %s WHERE ST_X(YelpData.BusinessCoordinates) = %s AND ST_Y(YelpData.BusinessCoordinates) = %s '''
        values = (city, lon, lat)
        cursor.execute(query, values)
        conn.commit()
        print(cursor.rowcount, "record(s) affected")
    except:
        pass