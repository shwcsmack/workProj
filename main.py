import requests
from bs4 import BeautifulSoup
import lxml
import configparser
import os, time, datetime
from math import floor

config = configparser.ConfigParser()
config.read('config.ini')

WEB_PATH = config['PATHS']['LoginForm']
POST_PATH = config['PATHS']['LoginPost']
s = requests.session()

login = s.get(WEB_PATH)
soup = BeautifulSoup(login.text, "lxml")
hidden_inputs = soup.find_all("input", type="hidden")
form = {x["name"]: x["value"] for x in hidden_inputs}

form["hprLogin$adUserName"] = config['CREDS']['Username']
form["hprLogin$adPass"] = config['CREDS']['Password']
form["hprLogin$rdLoginType"] = "cn"
form["hprLogin$btnSubmit"] = "Login"

file_mod_time = os.stat("output.html").st_mtime
last_time = (time.time() - file_mod_time) / 60

if last_time > int(config['GENERAL']['CacheTime']):
    print("Getting Data")
    
    response = s.post(POST_PATH, data=form)

    response_cache = open("output.html", "w")
    response_cache.writelines(response.text)
    response_cache.close()
else:
    print("Using cached version -- " + str(floor(last_time)) + " mins old.")

#print(last_time)