import os
import logging, csv
from urllib.parse import quote
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
from dotenv import find_dotenv, load_dotenv
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

#Global Logging Configuration For The Program
timestamp = datetime.now()
logging.basicConfig(filename=f"/var/log/data_collector.log", 
					format='%(asctime)s %(message)s', 
					filemode='w')
logger=logging.getLogger() 
logger.setLevel(logging.DEBUG)

def main():
  try:
    #MySQL Connnection Configuration
    engine = create_engine(f"mysql://{os.getenv('MYSQL_USER')}:%s@{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DATABASE')}" % quote(os.getenv('MYSQL_PASSWORD')))
    query = ''' SELECT rl.Id, rl.CityName, rl.Beds, rl.Baths,
                rl.ListingType, rl.Area, cd.PopulationLatest,
                COUNT(DISTINCT rls.SchoolId) AS Schools,
                COUNT(DISTINCT rlc.CollegeName) AS Colleges,
                COUNT(DISTINCT rlu.UniversityName) AS Universities,
                COUNT(DISTINCT rlam.YelpDataId) AS Ameneties,
                COUNT(DISTINCT rlab.AirbnbId) AS Airbnbs,
                ROUND(AVG(rla.Price), 0) AS Price,
                cd.AveragePrice,
                (CASE
                    WHEN ROUND(AVG(rla.Price), 0) > cd.AveragePrice THEN 'A'
                    WHEN ROUND(AVG(rla.Price), 0) < cd.AveragePrice THEN 'B'
                END) AS AboveBelowAverage,
                (CASE
                    WHEN Price BETWEEN 0 AND 25000 THEN '0-25000'
                    WHEN Price BETWEEN 25000 AND 50000 THEN '25000-50000'
                    WHEN Price BETWEEN 50000 AND 75000 THEN '50000-75000'
                    WHEN Price BETWEEN 75000 AND 100000 THEN '75000-100000'
                    WHEN Price BETWEEN 100000 AND 125000 THEN '100000-125000'
                    WHEN Price BETWEEN 125000 AND 150000 THEN '125000-150000'
                    WHEN Price BETWEEN 150000 AND 175000 THEN '150000-175000'
                    WHEN Price BETWEEN 175000 AND 200000 THEN '175000-200000'
                    WHEN Price BETWEEN 200000 AND 225000 THEN '200000-225000'
                    WHEN Price BETWEEN 225000 AND 250000 THEN '225000-250000'
                    WHEN Price BETWEEN 250000 AND 275000 THEN '250000-275000'
                    WHEN Price BETWEEN 275000 AND 300000 THEN '275000-300000'
                    WHEN Price BETWEEN 300000 AND 325000 THEN '300000-325000'
                    WHEN Price BETWEEN 325000 AND 350000 THEN '325000-350000'
                    WHEN Price BETWEEN 350000 AND 375000 THEN '350000-375000'
                    WHEN Price BETWEEN 375000 AND 400000 THEN '375000-400000'
                    WHEN Price BETWEEN 400000 AND 425000 THEN '400000-425000'
                    WHEN Price BETWEEN 425000 AND 450000 THEN '425000-450000'
                    WHEN Price BETWEEN 450000 AND 475000 THEN '450000-475000'
                    WHEN Price BETWEEN 475000 AND 500000 THEN '475000-500000'
                    WHEN Price BETWEEN 500000 AND 550000 THEN '500000-550000'
                    WHEN Price BETWEEN 550000 AND 600000 THEN '550000-600000'
                    WHEN Price BETWEEN 600000 AND 650000 THEN '600000-650000'
                    WHEN Price BETWEEN 650000 AND 700000 THEN '650000-700000'
                    WHEN Price BETWEEN 700000 AND 750000 THEN '700000-750000'
                    WHEN Price BETWEEN 750000 AND 800000 THEN '750000-800000'
                    WHEN Price BETWEEN 800000 AND 850000 THEN '800000-850000'
                    WHEN Price BETWEEN 850000 AND 900000 THEN '850000-900000'
                    WHEN Price BETWEEN 900000 AND 950000 THEN '900000-950000'
                    WHEN Price BETWEEN 950000 AND 1000000 THEN '950000-1000000'
                    WHEN Price BETWEEN 1000000 AND 1100000 THEN '1000000-1100000'
                    WHEN Price BETWEEN 1100000 AND 1200000 THEN '1100000-1200000'
                    WHEN Price BETWEEN 1200000 AND 1300000 THEN '1200000-1300000'
                    WHEN Price BETWEEN 1300000 AND 1400000 THEN '1300000-1400000'
                    WHEN Price BETWEEN 1400000 AND 1500000 THEN '1400000-1500000'
                    WHEN Price BETWEEN 1500000 AND 1600000 THEN '1500000-1600000'
                    WHEN Price BETWEEN 1600000 AND 1700000 THEN '1600000-1700000'
                    WHEN Price BETWEEN 1700000 AND 1800000 THEN '1700000-1800000'
                    WHEN Price BETWEEN 1800000 AND 1900000 THEN '1800000-1900000'
                    WHEN Price BETWEEN 1900000 AND 2000000 THEN '1900000-2000000'
                    WHEN Price BETWEEN 2000000 AND 2500000 THEN '2000000-2500000'
                    WHEN Price BETWEEN 2500000 AND 3000000 THEN '2500000-3000000'
                    WHEN Price BETWEEN 3000000 AND 3500000 THEN '3000000-3500000'
                    WHEN Price BETWEEN 3500000 AND 4000000 THEN '3500000-4000000'
                    WHEN Price BETWEEN 4000000 AND 4500000 THEN '4000000-4500000'
                    WHEN Price BETWEEN 4500000 AND 5000000 THEN '4500000-5000000'
                    WHEN Price BETWEEN 5000000 AND 5500000 THEN '5000000-5500000'
                    WHEN Price BETWEEN 5500000 AND 6000000 THEN '5500000-6000000'
                    WHEN Price BETWEEN 6000000 AND 6500000 THEN '6000000-6500000'
                    WHEN Price BETWEEN 6500000 AND 7000000 THEN '6500000-7000000'
                    WHEN Price BETWEEN 7000000 AND 7500000 THEN '7000000-7500000'
                    WHEN Price BETWEEN 7500000 AND 10000000 THEN '7500000-10000000'
                    WHEN Price BETWEEN 10000000 AND 15000000 THEN '10000000-15000000'
                    WHEN Price BETWEEN 15000000 AND 20000000 THEN '15000000-20000000'
                END) AS PriceCategorization
                FROM Ontario.RemaxListingsAssociations rla 
                INNER JOIN Ontario.RemaxListings rl ON rl.Id = rla.Id
                INNER JOIN CitiesData cd ON rl.CityName = cd.CityName
                LEFT JOIN Ontario.RemaxListingsSchools rls  ON
                rl.Id = rls.Id
                LEFT JOIN Ontario.RemaxListingsColleges rlc ON
                rl.Id = rlc.Id
                LEFT JOIN Ontario.RemaxListingsUniversities rlu ON
                rl.Id = rlu.Id
                LEFT JOIN Ontario.RemaxListingsAmeneties rlam ON
                rl.Id = rlam.Id
                LEFT JOIN Ontario.RemaxListingsAirbnb rlab ON
                rl.Id = rlab.Id
                WHERE rl.Area IS NOT NULL
                AND rl.Area > 100
                AND rla.Price > 1000
                AND rl.Beds IS NOT NULL
                AND rl.Baths IS NOT NULL
                GROUP BY rl.Id '''
    dataframe = pd.read_sql(query, engine)
    logger.info('Generating CSV File Now')
    csv_path = f"/opt/app/RealEstateData.csv"
    dataframe.to_csv(csv_path, sep=',', index=False, encoding='utf-8')
    if len(dataframe) > 0:
      logger.info(f"CSV Data was generated successfully")
      # sftp_upload(csv_path, csv_file)
    else:
      logger.info('No items were recorded in the CSV File')
  except Exception as e:
    logger.error(e)
  
if __name__ == '__main__':
  main()