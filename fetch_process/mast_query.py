"""
Filename: mast_query.py
Author: Simon Zhao
Date Created: 02/27/2024
Date Last Modified: 02/28/2024
Description: This file querys into the MAST database based on observations
"""

from astroquery.mast import Observations
from setup_logger import logger
import os

class MastQuery:
    def __init__(self, target_name, instrument, download_dir="downloaded_fits"):
        self.target_name = target_name
        self.instrument_name = instrument
        self.download_dir = download_dir
        self.data_uri = None
        self.filtered_products = None
        self.downloaded_files = []

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
        print(obs_table)
        if not obs_table or len(obs_table) == 0:
            logger.warning(f"The expected observations were not found for {self.target_name}")
            return

        # get product list for observation 
        data_products = Observations.get_product_list(obs_table)
        #logger.info(f"DATA PRODUCTS: \n {data_products}")
        product = data_products[0]["dataURI"]
        logger.info(f"================DATA URI===================: \n {product}")
        logger.info(self.filter_fits_by_instrument(data_products, self.instrument_name))

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

            # after filtering the FITS files, download them
            #self.download_fits_files(filtered_fits, self.download_dir)

    def fetch_obs_table(self) -> None:
        """
        Performs SQL query into SQLite database for observation schedule.
        """
        pass

    def filter_fits_by_instrument(self, data_products: list, target_instrument: str):
        filtered_products = [product for product in data_products if "instrument_name" in product and product["instrument_name"] == target_instrument]
        return filtered_products

def main() -> None:
    mast_token = "PLACE_TOKEN_HERE"

    query = MastQuery("M-82", "NIRCam", "downloaded_fits/")
    query.mast_auth(mast_token)
    query.fetch_fits_data()



if __name__ == "__main__":
    main()


