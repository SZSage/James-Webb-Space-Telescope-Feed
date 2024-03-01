"""
Filename: mast_query.py
Author: Simon Zhao
Date Created: 02/27/2024
Date Last Modified: 02/28/2024
Description: This file querys into the MAST database based on observations
"""

from astroquery.mast import Observations
from astropy.io import fits
from setup_logger import logger
from io import BytesIO
import requests
import os
import pprint
pp = pprint.PrettyPrinter(indent=4)

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

    def fetch_fits_data(self) -> None:
        """
        Search for processed FITS files in the MAST database and display them.

        Parameters:
            target_name (str): Name of celestial body

        Returns:
            None
        """

        # query into MAST database and select only PUBLIC JWST data
        obs_table = Observations.query_criteria(target_name=self.target_name, obs_collection="JWST", dataRights="PUBLIC")
        logger.info(f"================OBS_TABLE================: \n {obs_table}")

        if not obs_table or len(obs_table) == 0:
            logger.warning(f"The expected observations were not found for {self.target_name}")
            return

        # get product list for observation 
        data_products = Observations.get_product_list(obs_table)
        logger.info(f"================DATA PRODUCTS==============: \n {data_products}")
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


    def stream_fits_data(self, data_uri: str):
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
                return hdul  # returning the HDU list object
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

    def filter_fits_by_instrument(self, data_products: list, target_instrument: str):
        """

        """
        filtered_products = [product for product in data_products if "instrument_name" in product and product["instrument_name"] == target_instrument]
        return filtered_products

    def combine(self, fits_uri: str) -> str:
        mast_url = "https://mast.stsci.edu/api/v0.1/Download/file?uri=mast:JWST/products/"
        new = mast_url + fits_uri
        self.fits_URIs = new
        logger.info(f"FITS URIs DICTIONARY: \n {self.fits_URIs}")
        return new

def main() -> None:
    mast_token = "PLACE_TOKEN_HERE"

    query = MastQuery("M-82", "NIRCam", "downloaded_fits/")
    query.mast_auth(mast_token)
    #fits_data = query.fetch_fits_data()
    new_url = query.combine("jw02677001003_03101_00001_nrs1_s2d.fits")
    query.stream_fits_data(new_url)



if __name__ == "__main__":
    main()

