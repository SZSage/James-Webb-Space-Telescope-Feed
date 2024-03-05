"""
Filename: mast_query.py
Author: Simon Zhao
Date Created: 02/27/2024
Date Last Modified: 03/05/2024
Description: This file querys into the MAST database based on observations
"""

from astroquery.mast import Observations
from astropy.table import Table
from astropy.io import fits
from io import BytesIO
import pandas as pd
from setup_logger import logger
import sqlite3
import requests
import os

class MastQuery:
    def __init__(self, target_name: str, instrument: str, download_dir: str="downloaded_fits"):
        self.target_name = target_name
        self.instrument_name = instrument
        self.file_endings = ["_i2d.fits", "_s2d.fits", "_cal.fits", "_calints.fits"]
        self.instruments = ["NIRCam", "NIRSpec", "MIRI"]
        self.download_dir = download_dir
        self.fits_URIs = {}
        self.data_uri = None
        self.connection = None
        self.obs_table = pd.DataFrame()
        self.row_data = {}
        self.all_observations = []

    def select_best_fits_file(self, data_products):
        # Filter to include only the highest calibration level data
        highest_calib_level = max(data_products['calib_level'])
        calibrated_data_products = data_products[data_products['calib_level'] == highest_calib_level]

        # Get the index of the product with the largest file size
        largest_file_index = calibrated_data_products['size'].argmax()

        # Select the product with the largest file size
        largest_file_product = calibrated_data_products[largest_file_index]

        # Return the URI of the largest file at the highest calibration level
        best_fits_uri = largest_file_product['dataURI']
        logger.info(f"Selected best FITS file URI: {best_fits_uri}")
        return best_fits_uri

    def mast_auth(self, token: str) -> None:
        """
        Authentication to access MAST database.

        Parameters:
            token (str): The Mast API token for authentication.

        Returns:
            None
        """
        try:
            Observations.login(token=token)
        except Exception as e:
            logger.error(f"Failed to authenticate MAST API: {e}")


    def connect_sqlite3(self, db_path: str) -> bool:
        """
        Establish a connection to SQLite database.

        Parameters:
            db_path (str): Path to the sqlite database.

        Returns:
            Bool
        """
        try:
            # establish connection to SQLite database
            self.connection = sqlite3.connect(db_path)
            cursor = self.connection.cursor()
            logger.info("----------Successfully connected to SQLite database----------")
        except sqlite3.Error as e:
            logger.exception(f"----Error occurred while connecting to database-----: {e}")
            return False
        return True

    def disconnect_from_db(self) -> None:
        """
        Closes connection to SQLite database.
        """
        if self.connection:
            self.connection.close()

    def fetch_from_sql_db(self, db_path: str) -> pd.DataFrame:
        """
        Executes given query on SQLite database and returns results as a DataFrame.

        Parameters:
            db_path (str): Path of database.

        Returns:
            pd.DataFrame: The results of the query.
        """
        connect = self.connect_sqlite3(db_path)
        # return empty DataFrame is connection unsuccessful
        if not connect:
            return pd.DataFrame()
        query = "SELECT * FROM jwst_data"
        dataframe = pd.read_sql_query(query, self.connection)
        logger.info(f"-------------------Dataframe--------------------\n {dataframe}")
        self.disconnect_from_db()
        return dataframe

    def fetch_and_segment_by_week(self, db_path) -> list:
        """
        Fetches all data from the SQLite data base and segments it by week.
        
        Parameters:
            db_path (str): Path to the SQLite database.

        Returns:
            list: A list of DataFreames, each representing a week's worth of observation data.
        """

        full_dataframe = self.fetch_from_sql_db(db_path)
        weekly_dataframes = []
        current_week = []
        
        for index, row in full_dataframe.iterrows():
            if str(row["visit_id"]).startswith("Visit Information for OP Package"):
                if current_week:  # if there is data in the current week, save it before starting a new week
                    weekly_dataframes.append(pd.DataFrame(current_week))
                    current_week = []
                # skip header row
                continue
            current_week.append(row)
        
        # save the last week
        if current_week:
            weekly_dataframes.append(pd.DataFrame(current_week))
        #logger.info(f"---------Weekly DataFrames-------\n {weekly_dataframes}")
        return weekly_dataframes

    def process_weekly_observations(self, weekly_dataframes: list) -> None:
        """
        """
        for weekly_df in weekly_dataframes:
            #for index, row in weekly_df: # uncomment after done testing
            # process only first observation for testing
            first_row = weekly_df.iloc[1]
            self.process_individual_observation(first_row.to_frame().T)
            # break after processing first observation
            break

    def clean_instrument_name(self, full_instrument_name: str) -> str:
        # Define a set of known instrument names
        known_instruments = {"NIRCam", "NIRSpec", "MIRI", "FGS", "NIRISS"}

        # check if the full name is already a known instrument
        if full_instrument_name in known_instruments:
            return full_instrument_name

        # otherwise, split and return the first word
        return full_instrument_name.split()[0]

    def process_individual_observation(self, observation_row, week_count: int) -> dict | None:
        """
        Query MAST database for an individual observation and process it.

        Prarmeters:
            observation_row (): 
        """

        full_instrument_name = observation_row.get("science_instrument")
        instrument_name = None

        # clean the instrument name, whether it's already short or needs to be split
        if full_instrument_name:
            instrument_name = self.clean_instrument_name(full_instrument_name)
        else:
            logger.warning("Instrument name is missing in the observation data.")
            return
    
        # get all column entries from observation schedule
        visit_id = observation_row.get("visit_id")
        pcs_mode = observation_row.get("pcs_mode")
        visit_type = observation_row.get("visit_type")
        scheduled_start_time = observation_row.get("scheduled_start_time")
        duration = observation_row.get("duration")
        target_name = observation_row.get("target_name")
        category = observation_row.get("category")
        keywords = observation_row.get("keywords")

        # check if required information is available
        if not all([visit_id, pcs_mode, visit_type, scheduled_start_time, duration, target_name, full_instrument_name, category, keywords]):
        #logger.warning("Skipping observation due to missing information.")
            return None

        self.row_data = {
            "visit_id": visit_id,
            "pcs_mode": pcs_mode,
            "visit_type": visit_type,
            "scheduled_start_time": scheduled_start_time,
            "duration": duration,
            "instrument_name": instrument_name,
            "target_name": target_name,
            "category": category,
            "keywords": keywords,
        }

        logger.info(f"Processing observation from week {week_count} for target: {target_name}, instrument: {instrument_name}")
        self.query_mast(target_name, instrument_name)

    def query_mast(self, target: str, instrument: str) -> None:
        target_with_wildcard = f"{target}*" if "*" not in target else target
        logger.info(f"================================TARGET AND INSTRUMENT: {target}, {instrument}")
        obs_table = Observations.query_criteria( #type: ignore
            target_name=target_with_wildcard,
            dataRights="PUBLIC"
        )
        
        logger.info(f"--------OBS TABLE for current Observation-------\n {obs_table}")

    def process_all_rows_from_db(self, dataframe: pd.DataFrame, week_count: int) -> None:
        """
        Processes each row from the DataFrame.

        Parameters:
            dataframe (pd.DataFrame): The DataFrame containing the data.
        """
        for index, row in dataframe.iterrows():
            self.process_individual_observation(row, week_count)

    def query_masts(self) -> list | None:
        obs_table = Observations.query_criteria( # type:ignore
        # query into MAST database and select only PUBLIC JWST data
            target_name=self.target_name,
                                                #instrument_name=self.instruments,
            obs_collection="JWST",
            dataRights="PUBLIC")
        logger.info(f"================OBS_TABLE================: \n {obs_table}")

        if not obs_table or len(obs_table) == 0:
            logger.warning(f"The expected observations were not found for {self.target_name}")
            return

        out_cols = ['target_name','instrument_name','filters','calib_level','t_exptime','proposal_id']
        print(obs_table[out_cols])

        obs_table['title'] = [x[:200] for x in obs_table['obs_title']]
        obs_table['proposal_id','title'].pprint(max_width=-1)

        # get product list for observation 
        data_products = Observations.get_product_list(obs_table) # type:ignore
        logger.info(f"================DATA PRODUCTS==============: \n {data_products}")

        hello = data_products['description','dataURI', 'calib_level', 'size', 'proposal_id']
        print(hello)
        product = data_products["dataURI"]
        logger.info(f"================DATA URI===================: \n {product}")

        #logger.info(self.filter_fits_by_instrument(data_products, self.instrument_name))
        filtered_fits = self.filter_files(data_products)
        # check if fits files are found, then print

    def filter_files(self, product_list: list) -> list | None:
        """
        Filter FITS files ending in "_i2d.fits" or "_s2d.fits" or "_cal.fits" or "_calints.fits".

        Parameters:
            product_list (list): 
        Returns:

            list or None
        """
        filtered_fits = [product for product in product_list if "productFilename" in product.colnames and 
                        (product["productFilename"].endswith("_i2d.fits") or 
                         product["productFilename"].endswith("_s3d.fits") or
                #product["productFilename"].endswith(".jpg") or
                         product["productFilename"].endswith("_calints.fits")
                         )]
        # check if fits files are found
        if not filtered_fits:
            logger.warning(f"No filtered FITS files were found for: {self.target_name}")
        else:
            # print out list of filtered FITs files
            logger.info(f"Filtered FITS files for {self.target_name}")
            for product in filtered_fits:
                logger.info(product["productFilename"])
            return filtered_fits


    def stream_fits_data(self, data_uri: str) -> list | None:
        """
        Stream FITS data from the MAST database.

        Parameters:
            data_uri (str): The URI of data to stream

        Returns:
            hdul: The HDU list object loaded directly from the streamed FITS data
        """
        try:
            response = requests.get(data_uri, stream=True)
            response.raise_for_status()
            logger.info(f"Successfully connected to {data_uri}, status code: {response.status_code}")

            # load FITS data from the response content
            with fits.open(BytesIO(response.content)) as hdul:
                logger.info(f"Successfully opened FITS data from {data_uri}")
                image_data = hdul.info()
                logger.info(image_data)
                # return hdul list
                return hdul
        except requests.RequestException as e:
            logger.error(f"Request exception occurred: {e}")
        except Exception as e:
            logger.error(f"An error occurred while streaming FITS data: {e}")

    def get_fits_uris(self, data_products: list, file_endings: tuple=("_i2d.fits", "_s2d.fits")) -> list:
        """
        Get URIs for FITS files from data products.

        Parameters:
            data_products (list): The list of data products from MAST query.
            file_endings (list): A tuple of strings with file endings to look for.

        Returns:
            list: A list of URIs for the FITS files.
        """
        mast_url = "https://mast.stsci.edu/api/v0.1/Download/file?uri=mast:JWST/products/"
        # define a function to check if a product's filename ends with any of specified endings
        def ends_with_any(filename: str) -> bool:
            return any(filename.endswith(ending) for ending in file_endings)
        # use filter to apply check function to each product, then extract 'dataURI' from filtered products
        fits_uris = [
            product["dataURI"]
            for product in filter(lambda p: ends_with_any(p["productFilename"]), data_products)
        ]

        return fits_uris

    def download_specific_fits(self, fits_filename: str) -> None:
        """
        Downloads a specific FITS file by filename and saves it to the specified download directory.
        NOTE: This function is used for testing purposes.

        Parameters:
            fits_filename (str): The filename of the FITS file to download.

        Returns:
            None
        """
        # construct the download URL
        base_url = "https://mast.stsci.edu/api/v0.1/Download/file?uri="
        product_uri = f"mast:JWST/product/{fits_filename}"
        download_url = base_url + product_uri

        save_path = os.path.join(self.download_dir, fits_filename)

        try:
            # make the request and stream the content to a file
            with requests.get(download_url, stream=True) as response:
                response.raise_for_status()  # check for request errors
                with open(save_path, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
            logger.info(f"Successfully downloaded {fits_filename} to {save_path}")
        except requests.RequestException as e:
            logger.error(f"Request exception occurred while downloading {fits_filename}: {e}")
        except Exception as e:
            logger.error(f"An error occurred while downloading {fits_filename}: {e}")

    def filter_fits_by_instrument(self, data_products: list, target_instrument: str) -> list:
        """
        """
        filtered_products = [product for product in data_products if "instrument_name" in product and product["instrument_name"] == target_instrument]
        return filtered_products

    def combine(self, fits_uri: str) -> str:
        """
        Combines FIT URI with the MAST URL and add it to dictionary.
        """
        mast_url = "https://mast.stsci.edu/api/v0.1/Download/file?uri=mast:JWST/products/"
        new = mast_url + fits_uri
        self.fits_URIs = new
        logger.info(f"FITS URIs DICTIONARY: \n {self.fits_URIs}")
        return new

