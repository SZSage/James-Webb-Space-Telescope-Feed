"""
Filename: mast_query_test.py
Author: Simon Zhao
Date Created: 03/02/2024
Date Last Modified: 03/09/2024
Description: This file provides tests for the methods within the MastQuery class.
"""

import sys 
from pathlib import Path
import os

sys.path.append(str(Path(__file__).parent.parent))

import pytest #type: ignore
from unittest.mock import patch, MagicMock
from fetch_process.mast_query import MastQuery
import pandas as pd #type: ignore
from astropy.time import Time

@pytest.fixture
def mast_query():
    """
    Pytest fixture to create a MASTQuery instance fors testing
    """
    mq = MastQuery()
    mq.connection = MagicMock()
    return mq

def test_mast_auth_success(mast_query):
    """Test authentication to MAST database successful."""
    with patch("fetch_process.mast_query.Observations.login") as mock_login:
        token = "94a6a64c40904490a3512db4218ffca9"
        mast_query.mast_auth(token)
        mock_login.assert_called_with(token=token)


def test_connect_sqlite3_success(mast_query):
    """Test successful connection to SQLite database."""
    db_path = "../Webscraping/jwstDatabaseFile.sqlite"
    with patch("sqlite3.connect") as mock_connect, \
        patch("logging.Logger.info") as mock_logger_info:
        assert mast_query.connect_sqlite3(db_path) is True
        mock_connect.assert_called_with(db_path)
        mock_logger_info.assert_called()

def test_disconnect_from_db(mast_query):
    """Test disconnection from SQLite database."""
    mast_query.disconnect_from_db()
    mast_query.connection.close.assert_called_once_with()

def test_fetch_from_sql_db_success(mast_query):
    """Test fetching data from SQL database successfully."""
    db_path = "test_db.sqlite"
    test_data = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    with patch.object(mast_query, "connect_sqlite3", return_value=True), \
         patch("pandas.read_sql_query", return_value=test_data) as mock_read_sql_query, \
         patch.object(mast_query, "disconnect_from_db") as mock_disconnect_from_db:
        result = mast_query.fetch_from_sql_db(db_path)
        assert not result.empty
        assert result.equals(test_data)
        mock_read_sql_query.assert_called()
        mock_disconnect_from_db.assert_called()


def test_convert_mjd_to_datetime(mast_query):
    mjd = 59344
    expected_iso = "2021-05-10"
    time_obj = Time(mjd, format='mjd')
    
    result = mast_query.convert_mjd_to_datetime(time_obj)
    result_date = result.split(' ')[0]
    assert result_date == expected_iso, f"Expected ISO date to be {expected_iso}, got {result_date}"


