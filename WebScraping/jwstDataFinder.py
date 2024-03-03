"""
jwstDataFinder.py: CS 422 Project 2
Author: Isabella Cortez
Credit: YouTube, GeeksforGeeks
This file scrapes James Webb Space Telescope (JWST) data off of the jwst observing schedules website;
writes data to txt file
Date Modified: 2/27/2024
"""

import os
import requests
from bs4 import BeautifulSoup
import json
import time
from time import sleep
import timeit
import urllib.request
import pandas as pd


# url with jwst data
url = "https://www.stsci.edu/jwst/science-execution/observing-schedules"


# scrape_jwst_data takes data from the jwst table and returns the list
def scrape_jwst_data(u):
    # create an empty list titled jwst_data_list
    jwst_data_list = []
    jwst_list_links = []

    # wait for 5 seconds before getting request to scrape
    time.sleep(5)

    # request: get request to specific url link
    request = requests.get(url)

    BeautSoup = BeautifulSoup(request.text, 'html5lib')

    # data = BeautSoup.find('a', {'class': 'link-icon-added', 'target': '_blank'})
    data = BeautSoup.find_all('a')

    # extract the data from url and convert it to text
    # since the data on the url is .txt and a table, you can get the text via .text

    jwst_link = ""

    jwst_scraped_data = ""

    for check_url in data:
        href = check_url.get("href")
        # extract_data = check_url.text
        jwst_link = check_url.get('href')
        if href and href.endswith(".txt"):
            if href:
                jwst_link = "https://www.stsci.edu" + href
                jwst_list_links.append(jwst_link)

    # jwst_list_links.append(jwst_link)
    # print(jwst_list_links)

    for jwst_links in jwst_list_links:
        link_request = requests.get(jwst_links)
        # print(jwst_links)
        jwst_text = link_request.text
        jwst_scraped_data = jwst_text.splitlines()

        jwst_data_list.append(jwst_scraped_data)

    # each string in the text becomes a list of items
    # jwst_scraped_data = jwst_text.splitlines()

    # append to list

    # return list
    return jwst_data_list

def write_to_txt(jwst_data_list, output_file='jwst_data.txt'):
    with open(output_file, 'w') as file:
        for data in jwst_data_list:
            for line in data:
                file.write(line + '\n')
            file.write('\n')



# this function calls the scraped_jwst_data and then calls save_to_json and everything is output
def return_jwst_data():
    # jwst url used
    url_needed = "https://www.stsci.edu/jwst/science-execution/observing-schedules"
    # scraping jwst data
    jwst_info = scrape_jwst_data(url_needed)
    # saving jwst data to json
    # save_to_json(jwst_info)
    write_to_txt(jwst_info)
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


# test = scrape_jwst_data(url)

# print done when finished
print("done")
