import mysql.connector
import os, logging
from dotenv import find_dotenv, load_dotenv
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

#Global Logging Configuration
# logging.basicConfig(filename='/var/log/avgprice-calculator.log', 
                    # encoding='utf-8', level=logging.DEBUG)

# This function maintains the average
# listing price of each city in the
# given province.
def city_avg_price_calculator():
  try:
    conn = mysql.connector.connect(
      host = os.getenv("MYSQL_HOST"),
      user = os.getenv("MYSQL_USER"),
      password = os.getenv("MYSQL_PASSWORD"),
      database = os.getenv("MYSQL_DATABASE"),
      port = os.getenv("MYSQL_PORT"),
      auth_plugin='mysql_native_password')
    cursor = conn.cursor(buffered=True , dictionary=True)
    # logging.info(f'Connection to {os.getenv("MYSQL_HOST")} server was successful')
  except Exception as e:
    print(e)
    # logging.error(e)
  # Get the latest average price of all the cities in Ontario
  # Rental listings only
  query_rent_price = ''' SELECT rl2.CityName, ROUND(AVG(rla2.Price), 0) AS Price
                    FROM Ontario.RealEstateListingsAssociations rla2 
                    INNER JOIN Ontario.RealEstateListings rl2 ON rl2.Id = rla2.Id
                    INNER JOIN Ontario.CitiesData cd ON rl2.CityName = cd.CityName
                    WHERE rl2.Beds <= 15
                    AND rl2.Baths <= 10
                    AND rla2.`timestamp` = (SELECT MAX(rla.`timestamp`)  FROM Ontario.RealEstateListingsAssociations rla)
                    AND rl2.ListingType = 'Rental'
                    GROUP BY rl2.CityName '''
  cursor.execute(query_rent_price)
  results_set = cursor.fetchall()
  # logging.info(f'Number of enteries query returned: {len(results_set)}.')
  for value in results_set:
    try:
      city = value['CityName']
      price = value['Price']
      query = ''' UPDATE CitiesData SET AverageRentalPrice = %s WHERE CityName = %s '''
      values = (price, city)
      cursor.execute(query, values)
      conn.commit()
      # logging.info(f'{cursor.rowcount} record(s) affected')
    except Exception as e:
      print(e)
      # logging.error(e)
  # # Real Estate price not rentals
  # query_rl_price = '''SELECT rl2.CityName, ROUND(AVG(rla2.Price), 0) AS Price
  #                     FROM Ontario.RealEstateListingsAssociations rla2 
  #                     INNER JOIN Ontario.RealEstateListings rl2 ON rl2.Id = rla2.Id
  #                     INNER JOIN Ontario.CitiesData cd ON rl2.CityName = cd.CityName
  #                     WHERE rl2.Beds <= 15
  #                     AND rl2.Baths <= 10
  #                     AND rla2.`timestamp` = (SELECT MAX(rla.`timestamp`)  FROM Ontario.RealEstateListingsAssociations rla)
  #                     AND rl2.ListingType != 'Rental'
  #                     GROUP BY rl2.CityName '''
  # cursor.execute(query_rl_price)
  # results_set = cursor.fetchall()
  # # logging.info(f'Number of enteries query returned: {len(results_set)}.')
  # for value in results_set:
  #   try:
  #     city = value['CityName']
  #     price = value['Price']
  #     query = ''' UPDATE CitiesData SET AveragePrice = %s WHERE CityName = %s '''
  #     values = (price, city)
  #     cursor.execute(query, values)
  #     conn.commit()
  #     # logging.info(f'{cursor.rowcount} record(s) affected')
  #   except Exception as e:
  #     print(e)
  #     # logging.error(e)  

if __name__ == '__main__':
  city_avg_price_calculator()