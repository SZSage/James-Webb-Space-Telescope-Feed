"""
jwstJson.py: CS 422 Project 2
Author: Isabella Cortez
Credit:
This file takes the data from the jwst_data.txt file and converts it to json format (output is jwst_data.json)
Date Modified: 3/10/2024
"""

import re
import json


# convert txt to json
def parse_txt_to_json(txt_file):
    # Read the content of the text file
    with open(txt_file, 'r') as file:
        lines = file.readlines()

    # Define a pattern for extracting column headers
    header_pattern = re.compile(r'\s*VISIT ID\s*PCS MODE\s*VISIT TYPE\s*SCHEDULED START TIME\s*DURATION\s*SCIENCE INSTRUMENT AND MODE\s*TARGET NAME\s*CATEGORY\s*KEYWORDS\s*')

    # Find the line number where the header is located
    header_line = next(i for i, line in enumerate(lines) if header_pattern.match(line))

    # Extract column headers
    header_line_content = lines[header_line].strip()

    headers = [header_line_content[i:j].strip() for i, j in
               zip([0] + [m.start() for m in re.finditer(r'\s{2,}', header_line_content)],
                [m.start() for m in re.finditer(r'\s{2,}', header_line_content)] + [None])]


    # Initialize a list to store the visit information
    visit_info_list = []

    # Iterate over lines below the header to extract visit information
    for line in lines[header_line + 2:]:
        visit_info = line.split('  ')
        visit_info = [value.strip() for value in visit_info if value.strip()]
        # print(visit_info)

        # iterate through headers and visit_info list
        visit_dict = dict(zip(headers, visit_info))

        # append them to visit_info_list
        visit_info_list.append(visit_dict)

    # return list
    return visit_info_list

# text file to read from
txt_file = "jwst_data.txt"

# what to call json file
json_output_file = "jwst_data.json"

# Parse the text file and get visit information list
visit_info_list = parse_txt_to_json(txt_file)

# Write the visit information to a JSON file
with open(json_output_file, 'w') as json_file:
    json.dump(visit_info_list, json_file, indent=2)

# print to make sure info is in json file
print(f"JSON data has been written to {json_output_file}.")
