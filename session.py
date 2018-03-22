import requests
from bs4 import BeautifulSoup
import lxml
import configparser
import os, time, datetime
from math import floor

#bring in config in global scope
config = configparser.ConfigParser()
config.read('config.ini')

#Gets the data from the site to cache
def getData(session):
    print("Getting Data")
    
    #Login and establish the session
    response = session.post(config['PATHS']['LoginPost'], data=makeForm(session))

    #dump worksheet view
    response_cache = open("worksheet.html", "w")
    response_cache.writelines(response.text)
    response_cache.close()

    #dump schedule view
    #payload = {'Action': config['PATHS']['ScheduleView']}
    # print(config['PATHS']['WMTroot'] + "?Action=" + config['PATHS']['ScheduleView'])
    response = session.get(config['PATHS']['WMTroot'] + "?Action=" + config['PATHS']['ScheduleView'])
    sched_view = open("scheduleview.html", "w")
    sched_view.writelines(response.text)

#helper function to setup the login form
def makeForm(session):
    #get the login html so we can find hidden inputs to get around CSRF
    login = session.get(config['PATHS']['LoginForm'])
    soup = BeautifulSoup(login.text, "lxml")
    hidden_inputs = soup.find_all("input", type="hidden")
    form = {x["name"]: x["value"] for x in hidden_inputs}

    form["hprLogin$adUserName"] = config['CREDS']['Username']
    form["hprLogin$adPass"] = config['CREDS']['Password']
    form["hprLogin$rdLoginType"] = "cn"
    form["hprLogin$btnSubmit"] = "Login"

    return form