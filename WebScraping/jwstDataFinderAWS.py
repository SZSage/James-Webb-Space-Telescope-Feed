"""
jwstDataFinderAWS.py: CS 422 Project 2
Author: Jacob Burke, Isabella Cortez
Credit: YouTube, GeeksforGeeks, AWS boto3 documentation
This file scrapes James Webb Space Telescope (JWST) data off of the jwst observing schedules website;
writes data to txt file. It has been modified from the original local linux version to now work
with AWS Lambda and S3.
Date Modified: 3/6/2024
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
import boto3


# url with jwst data
url = "https://www.stsci.edu/jwst/science-execution/observing-schedules"

#s3 client object used to read/write to AWS S3 service
s3 = boto3.client('s3')

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

    try:
        # request: get request to specific url link
        request = session.get(url)
    except requests.exceptions.RequestException as e:
        print(f"Connection error for {url}: {e}")
        return None

    if request.status_code == 200:


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

def write_txt_to_s3(jwst_data_list, bucket_name = 'nebulanet.net', object_key='WebScraping/jwst_data.txt'):
    """ Description: Function used to overwrite the contents of an s3 file.
    Parameters:
           1. jwst_data_list (web scraped string data stored in an array)
           2. bucket_name (name of s3 bucket)
           3. object_key (path to object inside s3 bucket)
    """
    new_content = '\n'.join(jwst_data_list)

    try:
        # overwrite the existing S3 files content
        s3.put_object(Bucket=bucket_name, Key=object_key, Body=new_content)
        print("Object overwritten successfully")
    except Exception as e:
        print("Error overwriting object:", e)


# this function calls the scraped_jwst_data and then calls save_to_json and everything is output
def return_jwst_data(session):
    # jwst url used
    url_needed = "https://www.stsci.edu/jwst/science-execution/observing-schedules"
    # scraping jwst data
    jwst_info = scrape_jwst_data(session, url_needed)
    # saving jwst data to json
    # save_to_json(jwst_info)
    write_txt_to_s3(jwst_info)
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
session = create_session()
get_jwst_data = return_jwst_data(session)
session.close()

# test = scrape_jwst_data(url)

# print done when finished
print("done")
