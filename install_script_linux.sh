# Filenamse: install_script_linux.py
# Author: Jacob Burke
# Date Created: 02/25/2024
# Date Last Modified: 03/11/2024
# Description: install_script_linux.py installs the required programs and python
# libraries needed to execute and launch the nebulanet website

#!/bin/bash

# stop script on error
set -e

# update system package (comment out for ix-dev)
sudo apt-get update

# install Python 3.11.6 and pip (comment out for ix-dev)
sudo apt-get install -y python3.11.6 python3-pip

# verify python version
python3 --version

# install SQLite3  (comment out for ix-dev)
sudo apt-get install -y sqlite3

# install React  (comment out for ix-dev)
sudo apt-get install -y nodejs
sudo apt-get install -y npm

# update pip to latest version
python3 -m pip install --upgrade pip

# install Python libraries for application
python3 -m pip install astropy astroquery matplotlib numpy pandas beautifulsoup4 html5lib requests pytest

# verify installation
python3 -c "import sqlite3; import astropy; import astroquery; import matplotlib; import numpy; import pandas; import bs4; import html5lib; import requests; import pytest; print('All modules installed successfully')"
