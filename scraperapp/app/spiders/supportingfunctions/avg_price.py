import mysql.connector
import os, logging
from dotenv import find_dotenv, load_dotenv
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

#Global Logging Configuration
logging.basicConfig(filename='/var/log/avgprice-calculator.log', 
                    encoding='utf-8', level=logging.DEBUG)

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
      port = os.getenv("MYSQL_PORT"))
    cursor = conn.cursor(buffered=True , dictionary=True)
    print(f'Connection to {os.getenv("MYSQL_HOST")} server was successful')
    logging.info(f'Connection to {os.getenv("MYSQL_HOST")} server was successful')
  except Exception as e:
    logging.error(e)

  try: 
    query = ''' SELECT rl2.CityName, ROUND(AVG(rla2.Price), 0) AS Price
                FROM RemaxListingsAssociations rla2 
                INNER JOIN RemaxListings rl2 ON rl2.Id = rla2.Id
                WHERE rl2.Beds <= 15
                AND rl2.Baths <= 10
                AND rla2.`timestamp` = CURDATE()
                GROUP BY rl2.CityName '''
    cursor.execute(query)
    results_set = cursor.fetchall()
    logging.info(f'Number of enteries query returned: {len(results_set)}.')
  except Exception as e:
    logging.error(e)
  for value in results_set:
    try:
      city = value['CityName']
      price = value['Price']
      query = ''' UPDATE CitiesData SET AveragePrice = %s WHERE CityName = %s '''
      values = (price, city)
      cursor.execute(query, values)
      conn.commit()
      logging.info(f'{cursor.rowcount} record(s) affected')
    except Exception as e:
      logging.error(e)

if __name__ == '__main__':
  city_avg_price_calculator()