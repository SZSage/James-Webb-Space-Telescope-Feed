"""
jwstDataFinder.py: CS 422 Project 2
Author: Isabella Cortez
Credit: YouTube, GeeksforGeeks
This file scrapes James Webb Space Telescope (JWST) data off of the jwst observing schedules website;
writes data to txt file
Date Modified: 03/10/2024
"""

import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import json
import time
from time import sleep
import random


# url with jwst data
url = "https://www.stsci.edu/jwst/science-execution/observing-schedules"


# create a session
def create_session():
    session = requests.Session()
    retries = Retry(total=10, backoff_factor=0.2, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retries)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


# scrape_jwst_data takes data from the jwst table and returns the list
def scrape_jwst_data(session, u):
    # create an empty list titled jwst_data_list
    jwst_data_list = []
    jwst_list_links = []

    # wait for 5 seconds before getting request to scrape
    time.sleep(5)

    # test for errors with session creation
    try:
        # request: get request to specific url link
        request = session.get(url)
    except requests.exceptions.RequestException as e:
        print(f"Connection error for {url}: {e}")
        return None

    if request.status_code == 200:
        # use BeautifulSoup to do request.text and use html5lib to grab everything
        BeautSoup = BeautifulSoup(request.text, 'html5lib')

        # look for anything with the 'a' tag
        data = BeautSoup.find_all('a')

        # set empty strings
        jwst_link = ""
        jwst_scraped_data = ""

        # extract the data from url and convert it to text
        for check_url in data:
            href = check_url.get("href")
            jwst_link = check_url.get('href')

            # since the data on the url is .txt, you can get the text via .txt checker -- check if it ends with
            if href and href.endswith(".txt"):
                if href:
                    # link is https://www.stsci.edu + jwst observation information (.txt)
                    jwst_link = "https://www.stsci.edu" + href
                    # append that to list
                    jwst_list_links.append(jwst_link)

        # loop through the jwst_list_links
        for jwst_links in jwst_list_links:
            # use request to get the links
            link_request = requests.get(jwst_links)
            # set jwst_request equal to the text version of the content in the urls
            jwst_text = link_request.text
            # split the string into a list
            jwst_scraped_data = jwst_text.splitlines()
            # append to the overall list (jwst_data_list)
            jwst_data_list.append(jwst_scraped_data)

        # return list
        return jwst_data_list


# this function takes the information from jwst_data_list and outputs to a txt file
def write_to_txt(jwst_data_list, output_file='jwst_data.txt'):
    # open up txt file and write to it
    with open(output_file, 'w') as file:
        # go through data in list
        for data in jwst_data_list:
            # go through each line in data
            for line in data:
                # write it to file
                file.write(line + '\n')
            # write to file
            file.write('\n')


# this function calls the scraped_jwst_data and then calls save_to_json and everything is output
def return_jwst_data(session):
    # jwst url used
    url_needed = "https://www.stsci.edu/jwst/science-execution/observing-schedules"
    # scraping jwst data
    jwst_info = scrape_jwst_data(session, url_needed)
    # saving jwst data to txt
    write_to_txt(jwst_info)
    # returning the data
    return jwst_info


# saves information to python list
def get_jwst_as_py_list():
    # opens the json file (jwst_data.json)
    with open('jwst_data.json', 'r') as f:
        # sets the jwst data list to json.loads
        scraped_jwst_data = json.loads(f.read())
    # returns list as python list
    return scraped_jwst_data


# create and close session
# calls the return jwst_data function
session = create_session()
get_jwst_data = return_jwst_data(session)
session.close()

# print done when finished
print("done")
