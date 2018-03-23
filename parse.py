from bs4 import BeautifulSoup
import lxml
import re

def getDays(data_in):
    days = []
    day_cells = data_in[1].find_all("td")
    for day_cell in day_cells:
        if day_cell.div.a and "Name" not in day_cell.div.contents[0]:
            # print(day_cell.div.contents)
            link = day_cell.div.a.get('href')
            # print("Link: " + link)
            day = str(day_cell.div.a.string).strip()
            # print("Day: " + day)
            date = str(day_cell.div.contents[2]).strip()
            # print("Date: " + date)
            day_obj = {"Day": day, "Date": date, "Link" : link}
            days.append(day_obj)
    return days

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
    dataContainer = datatables[2].find("div").table

    #Get area and pay period
    selectedOptionsHTML = dropdownsContainer.find_all(selected = "selected")
    area = selectedOptionsHTML[1].string
    payperiod = selectedOptionsHTML[0].string
    print("Currently looking at: " + area + " and pay period: " + payperiod)

    #Get the rows and loop
    dataTableRows = dataContainer.find_all("tr")

    #Grab current days and link to worksheet before we loop
    days = getDays(dataTableRows)
    # print(days)



    for row in dataTableRows:
        #find cells and loop
        cells = row.find_all("td")
        if not cells:
            # print("No cells?")
            continue
        elif not cells[0].div:
            #Blank row
            # print("no div")
            continue
        #get list of days
        elif "Name" in cells[0].div.contents[0]:
            # print(cells[0].div.contents[0])
            continue
        else:
            # print("no name")
            continue

        for cell in cells:
            if cell.div:
                if cell.div.div:
                    #should be a cell with a shift in it inside an anchor tag
                    if cell.div.div.a:
                        #Shift [T0700]
                        # print(cell.div.div.a.contents[4].strip())
                        continue
                    #this should be a leave cell
                    else:
                        #Leave [LV]
                        # print(cell.div.div.string)
                        continue
                elif len(cell.div.contents) == 1:
                    if re.search('\w{2} - \w+', cell.div.string):
                        #Name [FF - Stewart]
                        #print(cell.div.string)
                        continue
                    else:
                        #some other table data, come here if you want more data
                        continue
                #else:
                    #either a day or a help window link
                    #print("Day or Help")
                    #print(cell.div.contents)
            #else:
                #blank cell
                #print("blank cell")
    
    
    
    
    #loop through staff

    return dataout

class Schedule:

    def __init__(self):
        self.pay_period = ""
        self.area = ""
        self.employees = []

class Employee:

    def __init__(self):
        self.initials = ""
        self.name = ""
        self.schedule = {}
parseScheduleView()