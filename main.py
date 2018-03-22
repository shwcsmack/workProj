import requests
from bs4 import BeautifulSoup
import lxml
import configparser
import os, time, datetime
from math import floor
from session import getData

#Bring in config file
config = configparser.ConfigParser()
config.read('config.ini')

#setup session object
s = requests.session()

#check how old the current cache of files is
file_mod_time = os.stat("worksheet.html").st_mtime
last_time = (time.time() - file_mod_time) / 60

#last_time = 450
if last_time > int(config['GENERAL']['CacheTime']):
    getData(s)
else:
    print("Using cached version -- " + str(floor(last_time)) + " mins old.")

#print(last_time)