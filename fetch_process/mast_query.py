"""
Filename: mast_query.py
Author: Simon Zhao
Date Created: 02/27/2024
Date Last Modified: 02/28/2024
Description: This file querys into the MAST database based on observations
"""

from astroquery.mast import Observations
from setup_logger import logger

class MastQuery:
    def __init__(self, target_name, instrument, download_dir="downloaded_fits"):
        self.target_name = target_name
        self.instrument_name = instrument
        self.download_dir = download_dir

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

    def fetch_fits_data(self, target_name: str) -> None:
        """
        Search for processed FITS files in the MAST database and display them.

        Parameters:
            target_name (str): Name of celestial body

        Returns:
            None
        """

        # query into MAST database and select only PUBLIC JWST data
        obs_table = Observations.query_criteria(target_name=target_name, obs_collection="JWST", dataRights="PUBLIC")

        if not obs_table:
            logger.warning(f"The expected observations were not found for {target_name}")
            return

        # get product list for observation 
        products = Observations.get_product_list(obs_table)

        # filter product list for files ending in "_i2d.fits" or "_s2d.fits"
        filtered_fits = [product for product in products if "productFilename" in product.colnames and (product["productFilename"].endswith("_i2d.fits") or product["productFilename"].endswith("_s2d.fits"))]
        # check if fits files are found
        if not filtered_fits:
            logger.warning(f"No filtered FITS files were found for: {target_name}")
        else:
            # print out list of filtered FITS files
            logger.info(f"Filtered FITS files for {target_name}")
            for product in filtered_fits:
                logger.info(product["productFilename"])


def main() -> None:
    mast_token = "ADD_TOKEN_HERE"
    query = MastQuery("M-82", "NIRCAM")
    query.mast_auth(mast_token)
    query.fetch_fits_data("M-82")



if __name__ == "__main__":
    main()


