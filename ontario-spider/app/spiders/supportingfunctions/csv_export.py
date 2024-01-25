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
    query = ''' SELECT rl.Id, rl.Beds, rl.Baths,
                    rl.ListingType, rl.Area, cd.PopulationLatest,
                    COUNT(DISTINCT rls.SchoolId) AS Schools,
                    COUNT(DISTINCT rlc.CollegeName) AS Colleges,
                    COUNT(DISTINCT rlu.UniversityName) AS Universities,
                    COUNT(DISTINCT rlam.YelpDataId) AS Ameneties,
                    COUNT(DISTINCT rlab.AirbnbId) AS Airbnbs,
                    rl.CityName, ROUND(AVG(rla.Price), 0) AS Price,
                    cd.AveragePrice,
                    (CASE
                        WHEN ROUND(AVG(rla.Price), 0) > cd.AveragePrice THEN 'A'
                        WHEN ROUND(AVG(rla.Price), 0) < cd.AveragePrice THEN 'B'
                    END) AS AboveBelowAverage
                    FROM RemaxListingsAssociations rla 
                    INNER JOIN RemaxListings rl ON rl.Id = rla.Id
                    INNER JOIN CitiesData cd ON rl.CityName = cd.CityName
                    LEFT JOIN RemaxListingsSchools rls  ON
                    rl.Id = rls.Id
                    LEFT JOIN RemaxListingsColleges rlc ON
                    rl.Id = rlc.Id
                    LEFT JOIN RemaxListingsUniversities rlu ON
                    rl.Id = rlu.Id
                    LEFT JOIN RemaxListingsAmeneties rlam ON
                    rl.Id = rlam.Id
                    LEFT JOIN RemaxListingsAirbnb rlab ON
                    rl.Id = rlab.Id
                    WHERE rl.Area IS NOT NULL
                    AND rl.Area > 100
                    AND rla.Price > 100
                    AND rl.Beds IS NOT NULL
                    AND rl.Baths IS NOT NULL
                    GROUP BY rl.Id '''
    dataframe = pd.read_sql(query, engine)
    print(dataframe)
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