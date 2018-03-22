from bs4 import BeautifulSoup
import lxml

def parseScheduleView():
    dataout = ""

    #get html
    with open('scheduleview.html') as scheduleHTML:
        soup = BeautifulSoup(scheduleHTML, "lxml")
    
    #grab the container table that wraps all the data we want
    table = soup.find("div", "background").find_all("table")[4]
    #grab the outer data since were in table hell
    outerdata = table.contents[1].contents[3]
    #find the two tables that have the data we want
    datatables = outerdata.find_all("table")
    #find the container table that has the dropdowns
    dropdownsContainer = datatables[1]
    #find the container table that has the actual data table
    dataContainer = datatables[2]

    #Get area and pay period
    selectedOptionsHTML = dropdownsContainer.find_all(selected = "selected")
    area = selectedOptionsHTML[1].string
    payperiod = selectedOptionsHTML[0].string
    print("Currently looking at: " + area + " and pay period: " + payperiod)
    
    #Get the days
    #loop through staff

    return dataout


parseScheduleView()