###Needs to be integrated with emailing code in a for loop

import sqlite3

conn = sqlite3.connect('secret_santa_participants.db') #or whatever the name of the file is
#first column: group_name
#second column: first_name
#third_column: last_name
#fourth column: email
cursor = conn.cursor()
print("Sucessfully connected to database")

group_names = []
first_names = []
last_names = []
emails = []
#Arrays to hold all information

select_query = """SELECT * from Contacts""" # "Contacts" is name of table in example
cursor.execute(select_query)
records = cursor.fetchall() #set records to pull all data from database
print("Total rows are: ", len(records))

for row in records:
    group_names.append(row[0]) #assuming group name is first column
    first_names.append(row[1]) #assuming first name is secnod column
    last_names.append(row[2]) #assuming last nme is third column
    emails.append(row[3]) #assuming emails is last column

print(first_names[0], last_names[0], emails[0])

#run email bot in a loop below here using the arrays
