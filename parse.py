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

def parseStrengthRow(row):
    data = {"name": "", "shifts": []}

    cells = row.find_all("td")
    for cell in cells:
        #get the text
        text = cell.div.contents[0].strip()
        #change blank cells to zero
        if not text:
            text = "0"
        
        if re.search('\D+', text):
            data['name'] = text
        elif re.search('\d', text):
            data['shifts'].append(text)
    return data

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

    #Get the rows and loop
    dataTableRows = dataContainer.find_all("tr")

    #Grab current days and links to worksheet before we loop
    days = getDays(dataTableRows)

    #set up our schedule object
    schedule = Schedule()
    schedule.set_days(days)
    schedule.area = area
    schedule.pay_period = payperiod
    schedule.print()


    #loop other rows to fill out staff dict
    for row in dataTableRows:
        cells = row.find_all("td")
        
        #find out what is in the row we are working on
        if cells:  
            first_cell = cells[0]
            #find cell that has a div with just text
            if first_cell.div and len(first_cell.div.contents) == 1:
                inner_string = first_cell.div.contents[0]
                #staff row
                if re.search('\w{2} - \w+', inner_string):
                    schedule.addEmployee(Employee.from_html(row))
                #strength row
                elif "\xa0" not in  inner_string and "Name" not in inner_string:
                    schedule.addStrength(parseStrengthRow(row))
    

    
    return dataout

class Schedule:

    def __init__(self):
        self.pay_period = ""
        self.area = ""
        self.employees = []
        self.days = []
        self.strengths = []

    def set_days(self, days):
        self.days = days
    
    def print(self):
        print("Currently looking at: " + self.area + " and pay period: " + self.pay_period)

    def addEmployee(self, employee):
        self.employees.append(employee)

    def addStrength(self, strength):
        if strength not in self.strengths:
            self.strengths.append(strength)

class Employee:

    def __init__(self):
        self.initials = ""
        self.name = ""
        self.schedule = []  #shift: T1400, link:somelink.asp

    @classmethod
    def from_html(cls, html):
        employee = Employee()

        #find cells and loop
        cells = html.find_all("td")
        for cell in cells:
            #all the cells have a div inside so just jump to that
            cell = cell.div

            #cells with another div are the inner data
            if cell.div:
                if cell.div.a:
                    #Shift [T0700]
                    shift = cell.div.a.contents[4].strip()
                    link = cell.div.a.get('href')
                    employee.schedule.append({"shift": shift, "link": link})
                #this should be a leave cell
                else:
                    #Leave [LV]
                    employee.schedule.append({"shift": cell.div.string, "link": ""})
            else:
                parts = re.search('([A-Z]{2}) - ([\w ]+)' , cell.contents[0].strip())
                initials = parts[1]
                name = parts[2]
                employee.name = name
                employee.initials = initials

        return employee

    def print(self):
        print(self.name + " (" + self.initials + ")")



parseScheduleView()