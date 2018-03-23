import requests
import configparser
import os, time, datetime
from math import floor
from session import getData
from parse import parseScheduleView

#Bring in config file
config = configparser.ConfigParser()
config.read('config.ini')

#setup session object
s = requests.session()

#check if this system has run the code yet
if os.path.isfile("worksheet.html"):
    file_mod_time = os.stat("worksheet.html").st_mtime
    last_time = (time.time() - file_mod_time) / 60
else:
    last_time = 9999999

#check how old the current cache of files is
if last_time > int(config['GENERAL']['CacheTime']):
    getData(s)
else:
    print("Using cached version -- " + str(floor(last_time)) + " mins old.")

#print(last_time)
scheduledata = parseScheduleView()
print(scheduledata)