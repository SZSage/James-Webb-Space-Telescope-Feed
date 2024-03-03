!/bin/bash

# stop script on error
set -e

# update system package
sudo apt-get update

# install Python 3.11.6 and pip
sudo apt-get install -y python3.11.6 python3-pip

# verify python version
python3 --version

# install SQLite3 
sudo apt-get install -y sqlite3

# update pip to latest version
python3 -m pip install --upgrade pip

# install Python libraries for application
python3 -m pip install astropy matplotlib numpy beautifulsoup requests pytest

# install Python Astroquery library
python3 -m pip install -U --pre astroquery

# verify installation
python3 -c "import sqlite3; import astropy; import astroquery; import matplotlib; import numpy; import bs4; import requests; import pytest; print('All modules installed successfully')"
