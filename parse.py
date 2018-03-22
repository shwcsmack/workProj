from bs4 import BeautifulSoup
import lxml

def parseScheduleView():
    dataout = ""

    #open file
    scheduleHTML = open('scheduleview.html')
    print(scheduleHTML)

    #find the inner table
    #Get pay period
    #Get the days
    #loop through staff

    scheduleHTML.close()
    return dataout


parseScheduleView()