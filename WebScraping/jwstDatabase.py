"""
jwstDatabase.py: CS 422 Project 2
Author: Isabella Cortez
Credit: easyA github of willard's database implementation
This file takes the data from the jwst_data.json file and converts it to sqlite format
Date Modified: 3/10/2024
"""

import sqlite3
import json

# open json file
with open('jwst_data.json') as file:
    jwst_data_json = file.read()

# handle error exceptions
try:
    jwst_data = json.loads(jwst_data_json)
except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")
    exit()

# make connection to database
conn = sqlite3.connect('jwstDatabaseFile.sqlite')
cursor = conn.cursor()

# Clear existing data by truncating the table (DJW)
cursor.execute("DELETE FROM jwst_data")

# create table with these heading names
cursor.execute('''
    CREATE TABLE IF NOT EXISTS jwst_data (
        visit_id TEXT,
        pcs_mode TEXT,
        visit_type TEXT,
        scheduled_start_time TEXT,
        duration TEXT,
        science_instrument TEXT,
        target_name TEXT,
        category TEXT,
        keywords TEXT
    )
''')

# put data in these headings
for data_point in jwst_data:
    cursor.execute("INSERT INTO jwst_data VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (data_point.get('VISIT ID', ''),
                    data_point.get('PCS MODE', ''),
                    data_point.get('VISIT TYPE', ''),
                    data_point.get('SCHEDULED START TIME', ''),
                    data_point.get('DURATION', ''),
                    data_point.get('SCIENCE INSTRUMENT AND MODE', ''),
                    data_point.get('TARGET NAME', ''),
                    data_point.get('CATEGORY', ''),
                    data_point.get('KEYWORDS', '')))

# Commit changes and close the connection
conn.commit()
conn.close()

# print to know it is done
print("Data inserted successfully into the SQLite database.")
