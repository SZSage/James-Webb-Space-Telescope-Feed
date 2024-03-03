"""
Filename: mast_query.py
Author: Simon Zhao
Date Created: 02/27/2024
Date Last Modified: 03/03/2024
Description: This file querys into the MAST database based on observations
"""

from astroquery.mast import Observations
from astropy.io import fits
from io import BytesIO
from setup_logger import logger
import pandas as pd
import sqlite3
import requests
import os

class MastQuery:
    def __init__(self, target_name: str, instrument: str, download_dir: str="downloaded_fits"):
        self.target_name = target_name
        self.instrument_name = instrument
        self.file_endings = ["_i2d.fits", "_s2f.fits", "_cal.fits", "_calints.fits"]
        self.instruments = ["NIRCam", "NIRSpec", "MIRI"]
        self.download_dir = download_dir
        self.data_uri = None
        self.filtered_products = None
        self.fits_URIs = {}

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

    



    def fetch_fits_data(self) -> list | None:
        """
        Search for processed FITS files in the MAST database and display them.

        Parameters:
            target_name (str): Name of celestial body

        Returns:
            None
        """
        # query into MAST database and select only PUBLIC JWST data
        obs_table = Observations.query_criteria(target_name=self.target_name, obs_collection="JWST", dataRights="PUBLIC") # type:ignore
        logger.info(f"================OBS_TABLE================: \n {obs_table}")

        if not obs_table or len(obs_table) == 0:
            logger.warning(f"The expected observations were not found for {self.target_name}")
            return

        # get product list for observation 
        data_products = Observations.get_product_list(obs_table) # type:ignore
        logger.info(f"================DATA PRODUCTS==============: \n {data_products}")

        # check if data_products is empty
        if len(data_products) == 0:
            logger.warning("No data products were found for the given query.")
            return
        product = data_products[0]["dataURI"]
        logger.info(f"================DATA URI===================: \n {product}")
        #logger.info(self.filter_fits_by_instrument(data_products, self.instrument_name))

        # filter product list for files ending in "_i2d.fits" or "_s2d.fits"
        # and avoid "seg"
        filtered_fits = [product for product in data_products if "productFilename" in product.colnames and 
                        (product["productFilename"].endswith("_i2d.fits") or 
                         product["productFilename"].endswith("_s2d.fits") or 
                         product["productFilename"].endswith("_calints.fits") and
                        "seg" not in product["productFilename"]
                         )]
        #logger.info(f"=================FILTERED FITS================: \n {filtered_fits}")
        # check if fits files are found
        if not filtered_fits:
            logger.warning(f"No filtered FITS files were found for: {self.target_name}")
        else:
            # print out list of filtered FITS files
            logger.info(f"Filtered FITS files for {self.target_name}")
            for product in filtered_fits:
                logger.info(product["productFilename"])
            return filtered_fits


    def filter_files(self, product_list: list) -> list | None:
        """
        Filter FITS files ending in "_i2d.fits" or "_s2d.fits" or "_cal.fits" or "_calints.fits" 
        and avoid "seg"

        Parameters:
            product_list (list): 

        Returns:
            list or None
        """
        filtered_fits = [product for product in product_list if "productFilename" in product.colnames and 
                        (product["productFilename"].endswith("_i2d.fits") or 
                         product["productFilename"].endswith("_s2d.fits") or 
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

    def fetch_obs_table(self) -> None:
        """
        Performs SQL query into SQLite database for observation schedule.
        """
        pass


    def download_specific_fits(self, fits_filename: str) -> None:
        """
        Downloads a specific FITS file by filename and saves it to the specified download directory.
        NOTE: This function is used for testing purposes.

        Parameters:
            fits_filename (str): The filename of the FITS file to download.

        Returns:
            None
        """
        # Construct the download URL
        base_url = "https://mast.stsci.edu/api/v0.1/Download/file?uri="
        product_uri = f"mast:JWST/product/{fits_filename}"
        download_url = base_url + product_uri

        # Define the path where the file will be saved
        save_path = os.path.join(self.download_dir, fits_filename)

        try:
            # Make the request and stream the content to a file
            with requests.get(download_url, stream=True) as response:
                response.raise_for_status()  # Check for request errors
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

    def connect_sqlite3(self, path_db: str) -> None:
        """
        Establish a connection to SQLite database.
        """


"""
def main() -> None:
    mast_token = ""

    query = MastQuery("IR05189", "MIRI", "downloaded_fits/")
    query.mast_auth(mast_token)
    fits_data = query.fetch_fits_data()
    fits_filename = "jw03368-o140_t001_nircam_clear-f356w-sub160p_i2d.fits"
    #query.download_specific_fits(fits_filename)
    #new_url = query.combine("jw01701-o052_t007_nircam_clear-f140m-sub640_i2d.fits")
    #hdul_data = query.stream_fits_data(new_url)
    #image_data = hdul_data[1].data

if __name__ == "__main__":
    main()
"""
