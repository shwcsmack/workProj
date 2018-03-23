import requests
import configparser
import os, time, datetime
from math import floor
from session import getData
from parse import parseScheduleView
from pymongo import MongoClient
import json

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

#convert the schedule view into JSON for exporting to DB
scheduledata = parseScheduleView()

#connect to db
mongourl = 'mongodb://%s:%s@%s'% (config['CREDS']['dbuser'], config['CREDS']['dbpass'], config['PATHS']['dbpath'])
client = MongoClient(mongourl)
db = client.workproj    #set db

#clean db
db.schedules.drop()

#use schedules collection
schedules = db.schedules 

#load in json from file and convert to a python obj
data = {}
with open("schedule.json") as jsonfile:
    data = json.load(jsonfile)
    
#run query
result = schedules.insert_one(data)
print('Inserted: {0}'.format(result.inserted_id))
