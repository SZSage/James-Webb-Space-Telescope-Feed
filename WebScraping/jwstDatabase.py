"""
jwstDatabase.py: CS 422 Project 2
Author: Isabella Cortez
Credit: easyA github of willard's database implementation
This file takes the data from the jwst_data.json file and converts it to sqlite format
Date Modified: 2/27/2024
"""

import sqlite3
import json


with open('jwst_data.json') as file:
    jwst_data_json = file.read()


# jwst_data = json.loads(jwst_data_json)
#jwst_data_json = jwst_data_json.split('[')[-1].split(']')[0]

try:
    jwst_data = json.loads(jwst_data_json)
except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")
    exit()


conn = sqlite3.connect('jwstDatabaseFile.sqlite')
cursor = conn.cursor()

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



# jwst_data_json[5:]
'''
# for line in jwst_data_json[5:]:  # Skip the header row
try:
        # Split the line into individual JSON objects and parse each one
        # row_data = json.loads(line)
    data_list = json.loads("[" + jwst_data_json + "]")
    # row_data = json.loads(line.strip().rstrip(','))
    for row_data in data_list:

        row = (
            row_data.get('visit_id'),
            row_data.get('pcs_mode'),
            row_data.get('visit_type'),
            row_data.get('scheduled_start_time'),
            row_data.get('duration'),
            row_data.get('science_instrument_and_mode'),
            row_data.get('target_name'),
            row_data.get('category'),
            row_data.get('keywords')
        )
    conn.execute("INSERT INTO jwst_data VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", row)

except json.JSONDecodeError as e:
    print(f"Error decoding JSON on line: {jwst_data_json}")
    print(f"Error details: {e}")
    # continue  # Skip to the next line
'''
# Commit changes and close the connection
conn.commit()
conn.close()

print("Data inserted successfully into the SQLite database.")
