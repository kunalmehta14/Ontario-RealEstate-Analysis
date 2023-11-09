import geopy.distance
import mysql.connector
import os
from dotenv import find_dotenv, load_dotenv
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

#This function is responsible for finding the amenties near each listing.
#It goes through the Zillow and Remax listing objects and compares the location
#data with the Schools, Universities, Colleges and Yelp data points
