"""
Filename: mast_query.py
Author: Simon Zhao
Date Created: 02/27/2024
Date Last Modified: 03/09/2024
Description: 
    This file contains the MastQuery class which queries the MAST database for 
    observations related to specific astronomical targets. It allows for the 
    authentication, retrieval, filtering, and downloading of FITS files 
    corresponding to the observations made by the JWST instruments. The class 
    also includes methods to segment observational data by week and process
    individual observations for extracting metadata.
"""

from astroquery.mast import Observations
from astropy.utils.data import clear_download_cache
from astropy.time import Time
from astropy.io import fits
from io import BytesIO
from process_convert import Processing
import pandas as pd # type: ignore
import numpy as np
from datetime import timedelta
import sqlite3
import requests
import os.path
import logging
import pprint

pp = pprint.PrettyPrinter(indent=4)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MASTQuery")

class MastQuery:
    def __init__(self, download_dir: str="processed_png"):
        self.target_name = None
        #self.instrument_name = instrument
        self.file_endings = ["_i2d.fits", "_s2d.fits", "_calints.fits"]
        self.instruments = ["NIRCam", "NIRSpec", "MIRI", "FGG"]
        self.download_dir = download_dir
        self.fits_URIs = {}
        self.data_uri = None
        self.connection = None
        self.obs_table = pd.DataFrame()
        self.obs_metadata = {}
        self.row_data = {}
        self.all_observations = []
        self.scheduled_start_time = None
        self.instrument = None
        self.file_names = []

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

    def convert_mjd_to_datetime(self, mjd: Time) -> Time:
        """
        Converts mjd format to iso format

        Parameters:
            mjd (Time): Takes in mjd time format.

        Returns:
            Time: ISO time format.
        """
        t = Time(mjd, format='mjd')
        return t.iso  # or t.datetime to get a datetime object

    def fetch_from_sql_db(self, db_path: str) -> pd.DataFrame:
        """
        Executes given query on SQLite database and returns results as a DataFrame.

        Parameters:
            db_path (str): Path of database.

        Returns:
            pd.DataFrame: The results of the query.
        """
        # establish connection to slite3 database
        connect = self.connect_sqlite3(db_path)
        # return empty DataFrame is connection unsuccessful
        if not connect:
            return pd.DataFrame()
        query = "SELECT * FROM jwst_data"
        dataframe = pd.read_sql_query(query, self.connection)
        logger.info(f"-------------------Dataframe--------------------\n {dataframe}")
        self.disconnect_from_db()
        return dataframe

    def fetch_and_segment_by_week(self, db_path: str) -> list:
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
        
        week_count = 1
        max_weeks = 52
        for index, row in full_dataframe.iterrows():
            if str(row["visit_id"]).startswith("Visit Information for OP Package"):
                if current_week:
                    weekly_dataframes.append((week_count, pd.DataFrame(current_week)))
                    current_week = []
                    week_count += 1
                    if week_count > max_weeks:
                        break
                    #logger.info(f"week_count: {week_count}")
                continue
            current_week.append(row)
        
        # save the last week
        if current_week and week_count <= max_weeks:
            weekly_dataframes.append((week_count, pd.DataFrame(current_week)))
        #logger.info(f"---------Weekly DataFrames-------\n {weekly_dataframes}")
        return weekly_dataframes

    def clean_instrument_name(self, full_instrument_name: str) -> str:
        """
        Remove any additional words from the instrument name.

        Parameters:
            full_instrument_name (str): Takes in the instrument name and mode.

        Returns:
            str:  The instrument name.
        """
        known_instruments = {"NIRCam", "NIRSpec", "FGS", "NIRISS"}

        # check if the full name is already a known instrument
        if not full_instrument_name:
            return full_instrument_name
        # otherwise, split and return the first word
        instrument_name = full_instrument_name.split()[0] if " " in full_instrument_name else full_instrument_name
        return instrument_name if instrument_name in known_instruments else ""
    

    def process_individual_observation(self, observation_row, week_count: int) -> dict | None:
        """
        Query MAST database for an individual observation and process it.

        Prarmeters:
            observation_row ():
            week_count (int): Track weekly count

        Returns:
            dict:
        """
        # reset observation metadata for each observation
        self.obs_metadata = {}

        # aquire observation metadata 
        self.target_name = observation_row.get("target_name", "")

        self.instrument_name = self.clean_instrument_name(observation_row.get("science_instrument", ""))
        instrument_name_type = self.instrument_name + "/image"
        category = observation_row.get("category", "")
        keywords = observation_row.get("keywords", "")
        date = observation_row.get("scheduled_start_time", "")
        #logger.info(f"SCHEDULED START TIME BEFORE SPLIT {date}")
        self.scheduled_start_time = date.split("T")[0]
        #logger.info(f"SCHEDULED START TIME AFTER SPLIT {self.scheduled_start_time}")
        
        # skip certain rows 
        skip_obs = ["BD+60-1753", "ABELL2744"]
        if self.target_name in skip_obs:
            return
        skip_categories = ["Calibration", "Unidentified"]
        if category in skip_categories:
            #logger.warning(f"-------Skipping {category}")
            return
        if not all([self.target_name, self.instrument_name, category, keywords]):
            #logger.warning("Skipping observation due to missing information")
            return

        logger.info(f"Performing query into MAST for Week: {week_count} Target: {self.target_name}, Instrument: {self.instrument_name}, Date: {self.scheduled_start_time}, Category: {category}, Keywords: {keywords}")
        # query into MAST database to aquire FITS file and additional metadata
        final_metadata = self.query_mast(self.target_name, instrument_name_type, category, keywords)
        #logger.info(f"FINAL METADATA========: \n {final_metadata}")
        if final_metadata:
            # return metadata for this observation
            return final_metadata

    def file_exist(self, path: str) -> bool:
        """
        Check if a file exists in the specified path.

        Parameters:
            path (str): File path for PNG images.

        Returns:
            bool: True if file exists, otherwise false.
        """
        exists = os.path.isfile(path)
        if exists:
            logger.info(f"File {path} already exists.")
        return exists


    def convert_numpy(self, obj):
        """
        Recursively convert numpy data types to their native Python equivalents.
        """
        if isinstance(obj, np.generic):
            return obj.item()
        elif isinstance(obj, dict):
            return {key: self.convert_numpy(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self.convert_numpy(value) for value in obj]
        else:
            return obj

    def process_weekly_observations(self, weekly_dataframes: list, start_week: int = 16) -> None:
        """
        Process observations segmented by week.

        Parameters:
            weekly_dataframes (list): Takes in dataframes for each week as a list.
        """
        #logger.info(f"Weekly_dataframes=================\n {weekly_dataframes}")
        for week_count, weekly_df in weekly_dataframes:
            #if week_count == target_week:
            if week_count < start_week:
                continue

            logger.info(f"Processing observations for week {week_count}")
            for index, observation in weekly_df.iterrows():
                clean_instrument = self.clean_instrument_name(observation["science_instrument"])
                strip_date = observation["scheduled_start_time"].split("T")[0]
                output_filename = f"{observation['target_name']}_{clean_instrument}_{strip_date}.png"
                output_path = os.path.join(self.download_dir, output_filename)
                logger.info(f"OUTPUT FILE NAME: {output_filename}")
            
                # check if output file already exists
                if self.file_exist(output_path):
                    logger.info(f"File {output_filename} already exists. Skipping processing.")
                    continue
                observation_metadata = self.process_individual_observation(observation.to_dict(), week_count)
                logger.info(f"--------OBSERVATION METADATA-------- \n {observation_metadata}")
                
                if not observation_metadata:
                    logger.error("Skipping due to no observation metadata.")
                    continue

                # access first item in observation_metadata to get nested dict
                metadata = next(iter(observation_metadata.values()))
                logger.info(f"METADATA: \n {metadata}")
                best_fits_uri = metadata['fits_url']
                logger.info(f" BEST FITS URI: {best_fits_uri}")
                if not best_fits_uri:
                    logger.error("No fits_url found. Skipping further processing.")
                    continue
                try:
                    # construct full URL for FITS file
                    new_url = self.combine(best_fits_uri)
                    logger.info(f"Processing FITS URI: {new_url}")
                    # stream and process FITS data
                    #hello = self.stream_fits_data(new_url)
                    # process FITS file
                    Processing().compare_scaling_methods(new_url, self.target_name, self.instrument_name, self.scheduled_start_time)
                    metadata_converted = self.convert_numpy(self.obs_metadata)

                    if isinstance(metadata_converted, dict):
                        metadata_converted = self.convert_numpy(self.obs_metadata)
                        Processing().append_metadata_to_json(metadata_converted, "obs_metadata.json")
                        clear_download_cache()
                        logger.info("CLEAR DOWNLOAD CACHE")
                    else:
                        logger.error("Converted metadata is not a dictionary.")
                except Exception as e:
                    logger.error(f"Error processing observation: {e}")

    def query_mast(self, target: str, instrument: str, category: str, keywords:  str) -> dict | None:
        """
        Performs a query into MAST database for JWST observations based on target information,
        processes the observation table, selects best fits file based on data product criteria,
        and stores relevant metadata.

        Parameters:
            target (str): The name of the target object to query.
            instrument (str): The name of the instrument used for the observation.
            category (str): The category or classification of the target.
            keywords (str): Keywords associated with the observation.
        """

        obs_tables = []
        # query for calibration level 3 data 
        obs_table_calib_3 = Observations.query_criteria( #type: ignore
            target_name=target,
            obs_collection="JWST",
            instrument_name=instrument,
            dataRights="PUBLIC",
            dataproduct_type="IMAGE",
            calib_level=3
        )
        if len(obs_table_calib_3) > 0:
            obs_tables.append(obs_table_calib_3)
            logger.info(f"---------Calib lv 3 found, append to obs_table------ \n {obs_tables}")

        # if no level 3 data, fall back to level 2
        if not obs_tables:
            obs_table_level_2 = Observations.query_criteria( #type: ignore
                target_name=target,
                obs_collection="JWST",
                instrument_name=instrument,
                dataRights="PUBLIC",
                dataproduct_type="IMAGE",
                calib_level=2
            )
            if len(obs_table_level_2) > 0:
                obs_tables.append(obs_table_level_2)
                logger.info(f"------Calib lv 2 found, append to obs_table------ \n {obs_tables}")

        # if any observation data was gathered
        logger.info("Logging observation data")
        if obs_tables:
            obs_table = obs_tables[0]
            data_products = Observations.get_product_list(obs_table) #type: ignore
            logger.info(f"Data Products\n {data_products}")   
            obs_title = obs_table["obs_title"]
            # process each row in observation table to extract and store desired metadata
            # extract the desired columns from the observation table
            desired_calib_level = 3 if len(obs_table_calib_3) > 0 else 2
            filtered_data_products = data_products[data_products['calib_level'] == desired_calib_level]
            if not filtered_data_products:
                return None
            #logger.info(f"OBSERVATION TABLE------ \n {obs_table}")
            logger.info(f"FILTERED DATA PRODUCTS LIST: \n {filtered_data_products}")
            #for uri in filtered_data_products['dataURI']:
            #    print(uri)

            obs_df = obs_table.to_pandas()

            filtered_fits = self.filter_files(filtered_data_products)

            # select best fits file 
            best_fits_uri = self.select_best_fits(filtered_data_products.to_pandas())
            if not best_fits_uri:
                return None
            
            # find row that corresponds to best FITS URI
            best_fits_row = filtered_data_products[filtered_data_products["dataURI"] == best_fits_uri]
            #logger.info(f"BEST FITS ROW--------\n {best_fits_row}")

            # checking if there are any matches and handle case of multiple matches
            if  len(best_fits_row) > 0:
                best_fits_row = best_fits_row[0]
                parent_obs_id = best_fits_row["parent_obsid"].item()
                matching_row = obs_df[obs_df["obsid"] == parent_obs_id]
                # extract info
                if not matching_row.empty:
                    matching_row = matching_row.iloc[0]
                    filters = matching_row["filters"]
                    start_time = self.convert_mjd_to_datetime(matching_row["t_min"])
                    end_time = self.convert_mjd_to_datetime(matching_row["t_max"])
                    exposure_time = matching_row["t_exptime"]
                    exposure_timedelta = timedelta(seconds=exposure_time)
                    
                    # store metadata
                    metadata = {
                        "target_name": target,
                        "target_classification": category,
                        "instrument_name": instrument,
                        "filters": filters,
                        "obs_title": obs_title[0],
                        "parent_obsid":  parent_obs_id,
                        "description": best_fits_row["description"],
                        "keywords": keywords,
                        "file_name": best_fits_row["productFilename"],
                        "start_time": start_time,
                        "end_time": end_time,
                        "exposure_time": str(exposure_timedelta),
                        "calib_level": best_fits_row["calib_level"],
                        "fits_url": best_fits_row["dataURI"],
                        "size": best_fits_row.get("size", 0)
                    }

                    metadata_key = f"{target}_{self.instrument_name}_{self.scheduled_start_time}"
                    #logger.info(f"METADATA KEY===================: \n {metadata_key}")
                    
                    # unique identifier for each entry
                    self.obs_metadata[metadata_key] = metadata
                    #logger.info(f"SCHEDULED START TIME: {self.scheduled_start_time}")
                    # select best fits
                    # once selected, get date and filter
                    for target, value in self.obs_metadata.items():
                        print(f"Metadata for {target}:")
                        for k, v in value.items():
                            print(f"    {k}: {v}")
                            print()
                    logger.info(f"Metadata extracted and stored for target {target}.")
                    return self.obs_metadata


    def select_best_fits(self, data_products: pd.DataFrame, max_mb_size: float=500.0, min_mb_size: float = 15.0) -> str | None:
        """
        Selects best FITS file based on calibration level, stage 3 product types, and file size.

        Parameters:
            data_products (pd.DataFrame): Dataframe that contains data product info.
            max_mb_size (float): Define max size of FITS file in MB.
            min_mb_size (float): Minimum size of the FITS file in MB.

        Returns:
            str | None: URI of the best FITS file, or None if no suitable file is found.
        """
        # calculate max size from MB to bytes
        max_size_bytes = max_mb_size * 1e6
        min_size_bytes = min_mb_size * 1e6

        # filter by highest calibration level
        highest_calib_level = data_products['calib_level'].max()
        calib_filtered_products = data_products[data_products['calib_level'] == highest_calib_level]
        #logger.info(f"CALIB FILTERED PRODUCTS: \n {calib_filtered_products}")

        # exit early if no products match highest calibration level
        if calib_filtered_products.empty:
            logger.warning("No FITS files found matching the highest calibration level.")
            return
        
        # filter for preferred file types (e.g., '_i2d.fits', '_s2d.fits')
        fits_filtered_products = calib_filtered_products[
            calib_filtered_products['productFilename'].str.contains('|'.join(self.file_endings))
        ]
        logger.info(f"FITS FILTERED PRODUCTS: \n {fits_filtered_products}")
        # exit early if no products match the preferred file types
        if fits_filtered_products.empty:
            logger.warning("No suitable FITS files found after filtering for preferred file types.")
            return
        
        # size limit filter
        filtered_size_fits = fits_filtered_products[
                              (fits_filtered_products["size"] <= max_size_bytes) &
                              (fits_filtered_products["size"] >= min_size_bytes)
            ]

        if filtered_size_fits.empty:
            logger.warning("No suitable FITS files found.")
            return
        
        # select the product with the largest file size
        best_fits_row = filtered_size_fits.loc[filtered_size_fits['size'].idxmax()]
        # get URI of the best FITS file
        best_fits_uri = best_fits_row['dataURI']
        logger.info(f"Selected best FITS file URI under {max_mb_size} MB: {best_fits_uri}")
        return best_fits_uri

    def extract_and_store_fits_metadata(self, selected_fits: dict, obs_table: list) -> None:
        """
        Extract metadata from a selected FITS file and its corresponding metadata.

        Parameters:
            selected_fits (dict): Selected FITS file info.
            obs_table (list): List of observations with each as a dictionary.
        """
        obs_data = None 
        # loop through each observation in obs_table
        for obs in obs_table:
        # check if observation's obs_id matches the selected_files parent_obsid
            if obs["obs_id"] == selected_fits["parent_obsid"]:
            # if match is found, assign this observation to obs_data
                obs_data = obs
                break

        if obs_data:
            metadata = {
                "target_name": obs_data.get("target_name"),
                "instrument_name": obs_data.get("instrument_name"),
                "filters": obs_data.get("filters", ""),
                "obs_title": obs_data.get("obs_title", ""),
                "description": selected_fits.get("description", ""),
                "date": obs_data.get("t_min", ""),
                "calib_level": selected_fits.get("calib_level"),
                "fits_url": selected_fits.get("dataURI"),
                "size": selected_fits.get("size")
            }
            # use unique identifier for FITS file as the key
            unique_key = f"{metadata['target_name']}_{selected_fits['obs_id']}"
            self.obs_metadata[metadata[unique_key]] = metadata
            #logger.info(f"Metadata for selected FITS file: {metadata}")
        else:
            logger.warning(f"No matching observation found for selected FITS file: {selected_fits}")

    def process_all_rows_from_db(self, dataframe: pd.DataFrame, week_count: int) -> None:
        """
        Processes each row from the DataFrame.

        Parameters:
            dataframe (pd.DataFrame): The DataFrame containing the data.
        """
        for index, row in dataframe.iterrows():
            self.process_individual_observation(row, week_count)

    def filter_files(self, product_list: list) -> list | None:
        """
        Filter FITS files ending in "_i2d.fits" or "_s2d.fits" or "_cal.fits" or "_calints.fits".

        Parameters:
            product_list (list): List of product dictionaries from data_products
        Returns:
            list: List of filtered fits files
        """
        filtered_fits = [product for product in product_list if "productFilename" in product.colnames and 
                        (product["productFilename"].endswith("_i2d.fits") or 
                         product["productFilename"].endswith("_s3d.fits") or
                #product["productFilename"].endswith(".jpg") or
                         product["productFilename"].endswith("_calints.fits")
                         )]
        # check if fits files are found
        if not filtered_fits:
            logger.warning(f"No filtered FITS files were found for: ")
            return
        else:
            # print out list of filtered FITs files
            logger.info(f"Filtered FITS files for ")
            #for product in filtered_fits:
            #   logger.info(product["productFilename", "parent_obsid"])
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
                logger.info(f"IMAGE DATA \n {hdul}")
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

    def combine(self, fits_uri: str) -> str:
        """
        Combines FIT URI with the MAST URL and add it to dictionary.

        Parameters:
            fits_uri (str): The fits file name.

        Returns:
            str: The combined URL for fits file
        """
        if fits_uri is None:
            logger.error("FITS URI is None, cannot construct the full URi")
            return ""
        mast_url = "https://mast.stsci.edu/api/v0.1/Download/file?uri="
        new_uri = mast_url + fits_uri
        self.fits_URIs = new_uri
        logger.info(f"FITS URIs DICTIONARY: \n {self.fits_URIs}")
        return new_uri

