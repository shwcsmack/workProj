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
    dataContainer = datatables[2].find("div").table

    #Get area and pay period
    selectedOptionsHTML = dropdownsContainer.find_all(selected = "selected")
    area = selectedOptionsHTML[1].string
    payperiod = selectedOptionsHTML[0].string
    print("Currently looking at: " + area + " and pay period: " + payperiod)
    
    #Get the rows and loop
    dataTableRows = dataContainer.find_all("tr")
    for row in dataTableRows:
        #find cells and loop
        cells = row.find_all("td")
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
                    #TODO differentiate between names and count
                    #Name [FF - Stewart]
                    print(cell.div.string)
                #else:
                    #either a day or a help window link
                    #print("Day or Help")
            #else:
                #blank cell
                #print("blank cell")
    
    
    
    
    #loop through staff

    return dataout


parseScheduleView()