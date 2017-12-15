from bs4 import BeautifulSoup as Soup
import unittest
import requests
from datetime import date
import psycopg2
import psycopg2.extras
import sys
import numpy as np
import matplotlib.pyplot as plt
from config_finalproj import *


# GLOBALS
TIMESTAMP = str(date.today())
TIMESTAMP.replace(" ","_")

# Functions
def requester(base_url,params):
    returnable = requests.get(baseurl, params = params)
    returnable.encoding = 'utf-8'
    returnable = returnable.text()
    return returnable


### Scrape data from umich and save the raw html text file
# http://careers.umich.edu/search/advanced?career_interest=&work_location=4&position=&regular_temporary=&keyword=&all_words=&this_phrase=&words1=&words2=&words3=&posting_date=&job_id=&department=&title=
print("scraping umich")
try:
    umich_data = open('umich_data_{}.html'.format(TIMESTAMP),'r').read()
except:
    # Format and create the URL
    baseurl = "http://careers.umich.edu/search/advanced"
    params = {}
    params["work_location"] = 4
    params["keyword"] = ""
    
    # Get data from the url
    umich_data = requester(baseurl,params)
    # print(umich_data)

    # Make sure umich_data is a string
    print('The umich_data is type: {}'.format(type(umich_data)))
    
    f = open('umich_data_{}.html'.format(TIMESTAMP),'w')
    f.write(umich_data)
    f.close()
    
    # time.sleep(30)
# First, umich
print('Create BS instance for Umich')
try:
    umich_resultUL = open("umich_data_{}.html".format(TIMESTAMP),'r').read()
    umich_resultUL = Soup(umich_resultUL,'html.parser')
except:
    umich_data = open('umich_data_{}.html'.format(TIMESTAMP)).read()
    # Create a BeautifulSoup instance of the umich search page data
    umich_soup = Soup(umich_data,'html.parser')

    # Access the unordered list of the search results
    umich_resultUL = umich_soup.find("tbody")
    #connect the following to the above line to find the shit within the filtred results: .find("ul",{"id":"atfResults"})

    # prettify the umich results page
    f = open("umich_data_{}_pretty.html".format(TIMESTAMP),'w')
    umich_resultUL = umich_resultUL_pretty
    f.write(umich_resultUL_pretty.prettify())
    f.close()

### Iterate through each "tr" in the table to find data
print('Organze umich data')
# A list of dictionaries will be created
table_umich = umich_resultUL.find_all("td")
# print("table umich: {}".format(table_umich[-6:]))
categories = ["Date_Posted","Posting_Title","Job_Opening_ID","Department","Work_location"]
data_dict = {}
entries = {}
job_list = []
position_list = []
i = 0
entries_i = 1

# print(len(umich_resultUL.find_all("tr")))
# print(len(umich_resultUL.find_all("td")))
# print(umich_resultUL.find_all("tr")[:5])
# print(umich_resultUL.find_all("td")[:5])

new_umich_result = umich_resultUL.find_all("td")
# print(type(indeed_resultUL))    #BS instance
# print(type(indeed_resultUL_pretty))  #REsultset

### Make a Class Results that takes in search results
class Results_umich(object):
    def __init__(self, dict):
        #self.id = entries.keys()
        raw_title = dict["Posting_Title"][:-9]
        self.title = raw_title.split('">')[1]
        self.date = dict["Date_Posted"][4:-5]
        self.department = dict["Department"][4:-5]
    def __contains__(self,test_string):
        return test_string in self.title
    def __repr__(self):
        return "Date is {}, Title is: {}, Dept is {}".format(self.date,self.title, self.department)
    def database_output(self):
        return str({"Posting_Title":self.title, "Date_Posted":self.date, "Department":self.department})

print('Create Database ready format')
debug = 0
if debug == 1:
    pass
else:
    while i<51:
        print(i)
        data_dict[categories[0]] = str(new_umich_result[i])
        data_dict[categories[1]] = str(new_umich_result[i+1])
        data_dict[categories[2]] = str(new_umich_result[i+2])
        data_dict[categories[3]] = str(new_umich_result[i+3])
        data_dict[categories[4]] = str(new_umich_result[i+4])
        # print(data_dict)
        # print(Results_umich(data_dict))
        position_list.append(str(new_umich_result[i+1]))
        job_list.append(Results_umich(data_dict))
        i+=5
job_list_umich = ''
# with open("entries_file",'w') as f:
    # f.write(str(entries))
for i in job_list:
    job_list_umich += '{},'.format(i.database_output())
    
job_list_umich = job_list_umich[:-1]
print(job_list_umich)

############
###INDEED###
############
print('')
print('-----------------Indeed stuff----------------------')
print('')
### Scrape from Indeed and save the raw html text file
# https://www.indeed.com/jobs?q=&l=Ann+Arbor%2C+MI
print('Scraping Indeed')
try:
    indeed_data = open('indeed_data_{}.html'.format(TIMESTAMP),'r').read()
except:
    # Format and create the URL
    baseurl = "https://www.indeed.com/jobs"
    params = {}
    params["l"] = ["Ann+Arbor","2C+MI"]
    params["limit"] = [50]
    
    # Get data from the url
    indeed_data = requester(baseurl,params)
    # print(indeed_data)
    
    # Make sure indeed_data is a string
    print('The indeed_data is type: {}'.format(type(indeed_data)))

    f = open('indeed_data_{}.html'.format(TIMESTAMP),'w')
    f.write(indeed_data)
    f.close()
    
    # time.sleep(30)
# Next, Indeed
print('Create BS instance for Indeed')
try:
    indeed_resultUL = open("indeed_data_{}.html".format(TIMESTAMP),'r').read()
    indeed_resultUL = Soup(indeed_resultUL,'html.parser')
    # f = open("indeed_data_{}_pretty.html".format(TIMESTAMP),'w')
    # # print(indeed_resultUL)
    # indeed_resultUL = indeed_resultUL.find_all("h2",{"class":"jobtitle"})
    # # print(indeed_resultUL_pretty)
    # with open("indeed_result_file",'w') as f:
        # f.write(str(indeed_resultUL))
except:
    indeed_data = open('indeed_data_{}.html'.format(TIMESTAMP)).read()
    # Create a BeautifulSoup instance of the indeed search page data
    indeed_soup = Soup(indeed_soup,'html.parser')

    # Access the unordered list of the search results
    indeed_resultUL = indeed_soup.find("td",{"id":"resultsCol"})
    #connect the following to the above line to find the shit within the filtred results: .find("ul",{"id":"atfResults"})

    # prettify the indeed results page
    f = open("indeed_data_{}_pretty.html".format(TIMESTAMP),'w')
    indeed_resultUL = indeed_resultUL_pretty
    f.write(indeed_resultUL_pretty.prettify())
    f.close()

# organize indeed results
print('Organize Indeed data')
# print('indeed_resultUL is {}'.format(indeed_resultUL.find_all(attrs={"data-tn-component": "organicJob"})))
# print('indeed_resultUL count number is {}'.format(len(indeed_resultUL.find_all(attrs={"data-tn-component": "organicJob"}))))    it's 50, my dude
indeed_BS_list = indeed_resultUL.find_all('h2',attrs=('rel'=="noopener nofollow"))
new_indeed_result = indeed_BS_list
# print('indeed_BS_list is type {}'.format(type(indeed_BS_list)))  It's a ResultSet

# print('')
# print('test')
# print('')

# print(len(indeed_resultUL.find_all('h2',attrs=('rel'=="noopener nofollow"))))
# with open('indeed_newfindall','w') as f:
    # f.write(str(indeed_resultUL.find_all('h2',attrs=('class'=="jobtitle"))))
# indeed_jobtitles = indeed_resultUL.find_all(attrs={"class" == "jobtitle"})
# with open("indeed_jobtitles",'w') as f:
    # f.write(str(indeed_jobtitles))


# Test to see what the new_umich_result looks like
# with open("new_indeed_result",'w') as f:
    # f.write(str(new_indeed_result))

## Make a Class Results for indeed that takes in search results
class Results_indeed(object):
    def __init__(self, list):
        #self.id = entries.keys()
        raw_title = list[:-9]
        raw_title = raw_title.split('">')[1]
        self.title = raw_title.split('title="')[1]
        # self.date = list["Date_Posted"][4:-5]
        # self.department = list["Department"][4:-5]
    def __contains__(self,test_string):
        return test_string in self.title
    def __repr__(self):
        return "Title is: {}".format(self.title)
    def database_output(self):
        return str({"Posting_Title":self.title})

print('Create Database ready format for Indeed')
job_list_indeed = []
debug = 0
if debug == 1:
    pass
else:
    for each_item in indeed_BS_list:
        # print(Results_indeed(str(each_item)))
        job_list_indeed.append(Results_indeed(str(each_item)))

# print(len(job_list_indeed))
jobs_list_indeed = ''
for i in job_list_indeed:
    jobs_list_indeed += '{},'.format(i.database_output())
jobs_list_indeed = jobs_list_indeed[:-1]
# print(jobs_list_indeed)
    
print('Putting umich data into the DB')
###Putting the data into a database
try:
    conn = psycopg2.connect("dbname = '{0}' user = '{1}' password='{2}'".format(db_name_umich, db_user, db_password))
    print("Success connecting to the database")

except:
    print("Unable to connect to the database")
    sys.exit(1)

## SETUP FOR CREATING DATABASE AND INTERACTING IN PYTHON
# cur = conn.cursor()
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) # So you can insert by column name, instead of position, which makes the Python code even easier to write!

## Code to DROP TABLES IF EXIST IN DATABASE (so no repeats)
## We'll address this idea in more depth later.
cur.execute("DROP TABLE IF EXISTS UmichJobs") # Normally in SQL, you need to end statements with semicolons, but often, that's not required when you're using these psycopg2 module functions to interact with the database.

## CREATE TABLE(S) IN DATABASE
cur.execute("CREATE TABLE IF NOT EXISTS UmichJobs(Title VARCHAR(64) PRIMARY KEY, Date Posted VARCHAR(20), Departments VARCHAR(64)")

## INSERT DATA INTO TABLE(S) IN DATABASE
# Insert one row only

# Insert many with .executemany
jobs_diction = (jobs_list_umich)

cur.executemany("""INSERT INTO UmichJobs(Title,Date Posted,Departments) VALUES (%(Posting_Title)s, %(Date_Posted)s, %(Department)s)""",jobs_diction)

print('Putting indeed data into the DB')
###Putting the data into a database
try:
    conn = psycopg2.connect("dbname = '{0}' user = '{1}' password='{2}'".format(db_name_indeed, db_user, db_password))
    print("Success connecting to the database")

except:
    print("Unable to connect to the database")
    sys.exit(1)

## SETUP FOR CREATING DATABASE AND INTERACTING IN PYTHON
# cur = conn.cursor()
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) # So you can insert by column name, instead of position, which makes the Python code even easier to write!

## Code to DROP TABLES IF EXIST IN DATABASE (so no repeats)
## We'll address this idea in more depth later.
cur.execute("DROP TABLE IF EXISTS IndeedJobs") # Normally in SQL, you need to end statements with semicolons, but often, that's not required when you're using these psycopg2 module functions to interact with the database.

## CREATE TABLE(S) IN DATABASE
cur.execute("CREATE TABLE IF NOT EXISTS IndeedJobs(Title VARCHAR(64) PRIMARY KEY")

## INSERT DATA INTO TABLE(S) IN DATABASE
# Insert one row only

# Insert many with .executemany
jobs_diction = (jobs_list_indeed)

cur.executemany("""INSERT INTO UmichJobs(Title) VALUES (%(Posting_Title)s)""",jobs_diction)


####Data Vis
# data to plot
n_groups = 1
means_umich = (len(position_list))
means_indeed = (len(job_list_indeed))

# create plot
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.35
opacity = 0.8
 
rects1 = plt.bar(index, means_umich, bar_width,
                 alpha=opacity,
                 color='b',
                 label='umich')
 
rects2 = plt.bar(index + bar_width, means_indeed, bar_width,
                 alpha=opacity,
                 color='g',
                 label='Indeed')

plt.xlabel('Source')
plt.ylabel('Count')
plt.title('Job count per Source')
plt.xticks(index + bar_width, ('A'))
plt.legend()
 
plt.tight_layout()
plt.show()