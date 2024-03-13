"""
jwstJsonAWS.py: CS 422 Project 2
Author: Jacob Burke, Isabella Cortez
Credit:
This file takes the data from the jwst_data.txt file from an S3 Bucket and converts it to 
json format (output is jwst_data.json and gets overwritten to a previous version of the same file)
Date Modified: 3/6/2024
"""

import re
import json
import boto3

#s3 client object used to read/write to AWS S3 service
s3 = boto3.client('s3')

def parse_txt_to_json(bucket_name, object_key):
    # Read the content of the text file
    #with open(txt_file, 'r') as file:
    #    lines = file.readlines()
    lines = []

    try:
        # Retrieve content from txt file in s3 bucket
        response = s3.get_object(Bucket=bucket_name, Key=object_key)
        existing_content = response['Body'].read().decode('utf-8')
        lines = list(existing_content.splitlines())
    except Exception as e:
            print("Error reading s3 file content:", e)


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
        # visit_info = re.findall(r'"([^"]*)"|(\S+)', line)
        # visit_info = [value[0] if value[0] else value[1] for value in visit_info]
        # visit_info = [" ".join(value) if value[0] else value[1] for value in visit_info]
        # visit_info = [value.strip('"') if '"' in value else value for value in re.findall(r'"([^"]*)"|(\S+)', line)]
        visit_info = line.split('  ')
        visit_info = [value.strip() for value in visit_info if value.strip()]
        # print(visit_info)

        # Check if the line is not empty
        # if visit_info:
            # visit_string = ""
            # for item in visit_info:
               # visit_string += item
            # print(visit_string)
            # Combine the headers and visit information into a dictionary

        visit_dict = dict(zip(headers, visit_info))


        visit_info_list.append(visit_dict)


    return visit_info_list

def write_json_to_s3(visit_info_list, bucket_name = 'nebulanet.net', object_key='WebScraping/jwst_data.txt'):
    """ Description: Function used to overwrite the contents of an s3 file with json data.
    Parameters:
           1. visit_info_list (string data stored in an array)
           2. bucket_name (name of s3 bucket)
           3. object_key (path to object inside s3 bucket)
    """
    # flatten list of lists from scrape_jwst_data function to aggregate data into one string
    new_content = json.dumps(visit_info_list, indent=2)
    try:
        # overwrite the existing S3 files content
        s3.put_object(Bucket=bucket_name, Key=object_key, Body=new_content)
        print("JSON data overwritten successfully")
    except Exception as e:
        print("Error overwriting previous JSON file:", e)


def lambda_handler(event, context):
    s3_bucket = 'nebulanet.net'
    txt_file = "WebScraping/jwst_data.txt"
    json_output_file = "WebScraping/jwst_data.json"
    
    # Parse the text file and get visit information list
    visit_info_list = parse_txt_to_json(s3_bucket, txt_file)
    
    write_json_to_s3(visit_info_list, s3_bucket, json_output_file)
    
    # for visit_dict in visit_info_list:
        # print(" ".join(f"{key}: {value}" for key, value in visit_dict.items()))
    
    print(f"JSON data has been written to {json_output_file}.")