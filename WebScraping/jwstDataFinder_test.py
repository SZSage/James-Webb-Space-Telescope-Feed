"""
Filename: jwstDataFinder_test.py
Author: Jacob Burke
Date Created: 03/11/2024
Date Last Modified: 03/11/2024
Description: This file provides a test to ensure a connection can be established
to the observation data website
"""

import pytest #type: ignore
import requests
from jwstDataFinder import create_session

def test_session_connection():
    session = create_session()
    url = "https://www.stsci.edu/jwst/science-execution/observing-schedules"

    # Check that session object is made
    assert isinstance(session, requests.Session)    
    
    # Check for response using session object
    response = session.get(url)
    assert response.status_code == 200, f"Failed to connect to {url}"

