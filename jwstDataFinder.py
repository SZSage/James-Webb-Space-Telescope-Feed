"""
jwstDataFinder.py: CS 422 Project 2
Author: Isabella Cortez
Credit: YouTube, GeeksforGeeks
This file scrapes James Webb Space Telescope (JWST) data off of the jwst observing schedules website
Date Modified: 2/23/2024
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from time import sleep
import timeit
import urllib.request
import pandas as pd

# url with jwst data
url = "https://www.stsci.edu/files/live/sites/www/files/home/jwst/science-execution/observing-schedules/_documents/20240219_report_20240215.txt"


# scrape_jwst_data takes data from the jwst table and returns the list
def scrape_jwst_data(u):
    # create an empty list titled jwst_data_list
    jwst_data_list = []

    # wait for 5 seconds before getting request to scrape
    time.sleep(5)

    # request: get request to specific url link
    request = requests.get(url)

    # extract the data from url and convert it to text
    # since the data on the url is .txt and a table, you can get the text via .text
    extract_data = request.text

    # each string in the text becomes a list of items
    jwst_scraped_data = extract_data.splitlines()

    # append to list
    jwst_data_list.append(jwst_scraped_data)

    # return list
    return jwst_data_list


# function save_to_json creates a json file to put the scraped jwst data in
def save_to_json(data, filename='jwst_data.json'):
    # open json file to write in
    with open(filename, 'w', encoding='utf-8') as json_file:
        # put information into a json file
        json.dump(data, json_file, ensure_ascii=False, indent=4)


# this function calls the scraped_jwst_data and then calls save_to_json and everything is output
def return_jwst_data():
    # jwst url used
    url_needed = "https://www.stsci.edu/files/live/sites/www/files/home/jwst/science-execution/observing-schedules/_documents/20240219_report_20240215.txt"
    # scraping jwst data
    jwst_info = scrape_jwst_data(url_needed)
    # saving jwst data to json
    save_to_json(jwst_info)
    # returning the data
    return jwst_info


def get_jwst_as_py_list():
    # opens the json file (jwst_data.json)
    with open('jwst_data.json', 'r') as f:
        # sets the jwst data list to json.loads
        scraped_jwst_data = json.loads(f.read())
    # returns list as python list
    return scraped_jwst_data


# calls the return jwst_data function
get_jwst_data = return_jwst_data()

# print done when finished
print("done")
