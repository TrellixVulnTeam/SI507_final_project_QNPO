# SI 507 F17 - Final Project

This file will scrape data from Amazon and Rakuten using a user generated input, and gather the top 10 search results and organize the data into a bar graph. 

### INSTRUCTIONS
Step 1
pip install to requirements.txt. Create config file.

Step2
Run the code using Python3 in your terminal/command line, or whatever else you use (i.e. 'python3 main.py')! So long as you have all the libraries installed (refer to requirements.txt), and config file code should run without a problem. 

### Configure
To run the code you must have a few of these configured:

#Config File
Type in your postgres username as "db_user = '_yourUserName_'". Likewise, insert your password to the database as "db_password = '_yourPassWord_'". Also add the two database names (instructions below).

#Database
Create one called "umich_jobs" and label it as "db_name_umich". Create another called "indeed_jobs" and assign the variable "db_name_indeed" to it. Throw these into the config file as well.

### Explanation
When the code runs, it will scrape 50 job postings from the umich career website, and indeed. Once this is done, the data is organized into a list of dictionaries, so that inputting it into the database follows the form: ({dict1},{dict2},...).

The data is visuallized using matplotlib.pyplot. 


### Sources
https://www.indeed.com/
http://careers.umich.edu/
Database coding borrowed heavily from pgexample_multiplerows_byname.py, from lecture
https://pythonspot.com/en/matplotlib-bar-chart/


    - What the user should expect after the code runs (what should they see, what do any numbers they see represent, what will get created at the end — a file? a chart? — and how they can view it, etc)
    - Links to any resources used (e.g. client libraries, API documentation) and citations of any code borrowed from elsewhere
    - Also include in the readme a list of everyone with whom you worked on any of the project or talked to about it in depth. Doing that is OK: sourcing help from others is great! But no two projects should be alike — this should be your own work.