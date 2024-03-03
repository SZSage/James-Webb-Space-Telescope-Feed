"""
Filename: convert.py
Author: Simon Zhao
Date Created: 01/24/2024
Date Last Modified: 02/06/2024
Description: This script processes FITS files taken from the MAST database and converts them to PNG files for visualization.
"""

from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import (astropy_mpl_style, LogStretch, ImageNormalize)
import os
from setup_logger import logger

import pprint
pp = pprint.PrettyPrinter(indent=4)

class Processing:
    def __init__(self, download_dir="processed_png") -> None:
        self.download_dir = download_dir

    def asinh_scaling(self, data: np.ndarray, scale_min=None, scale_max=None, non_linear=2.0):
        """
        Apply asinh scaling to the data.
        Parameters:
            data (np.ndarray): 2D numpy array, the image data to scale.
        - beta: float, scaling factor controlling the transition between linear and log.

        Returns:
            Scaled data as a 2D numpy array.
        """
        if scale_min is None:
            scale_min = np.nanmin(data)
        if scale_max is None:
            scale_max = np.nanmax(data)
        factor = np.arcsinh((scale_max - scale_min) / non_linear)
        scaled_data = np.arcsinh((data - scale_min) / non_linear) / factor
        return scaled_data

    def process_fits(self, fits_path: str, use_asinh: bool=True, beta: float=5.0) -> np.ndarray:
        """
        Processes a FITS file and return the scaled image data.
        """
        with fits.open(fits_path) as hdul:
            # image data in first extension
            hdul.info()
            data = hdul[1].data # type: ignore
            logger.info(f"IMAGE DATA IN FIRST EXTENSION: \n {data}")
            if use_asinh:
                # apply asinh scaling
                scaled_data = self.asinh_scaling(data, non_linear=beta)
            else:
                # apply log10 scaling, ensure no log(0) issues
                data[data <= 0] = np.nan  
                scaled_data = np.log10(data)
                # handles NaNs
                scaled_data = np.nan_to_num(scaled_data, nan=0.0)
                
            # normalize scaled data for display
            scaled_data = (scaled_data - np.nanmin(scaled_data)) / (np.nanmax(scaled_data) - np.nanmin(scaled_data))
            return scaled_data

    def visualize_fits(self, image_data, frame=0) -> None:
        """
        Visualize processed FITS data.
        """
        plt.figure()
        # assuming image_data is a 3D array so we can visualize the first frame
        if image_data.ndim == 3:
            # visualize first frame for 3D data
            plt.imshow(image_data[0], cmap="magma")
        elif image_data.ndim == 2:
            # directly visualize for 3D data
            plt.imshow(image_data, cmap="magma")
        else:
            raise ValueError("image_data must be 2D or 3D.")
    
        plt.colorbar()
        plt.axis("off")
        plt.show()

    def convert_to_png(self, data: np.ndarray, output_filename: str, switch: bool) -> None:
        """
        Converts the processed FITS data to PNG and saves them to a directory.
        
        Parameters:
            data (np.ndarray): Image data to be saved
            output_filename (str): The filename for the saved PNG file
        Returns:
            None
        """
        # construct path for file
        paths = os.path.join(self.download_dir, output_filename)
        # ensures directory exists
        os.makedirs(self.download_dir, exist_ok=True)

        if switch:
            fig, ax = plt.subplots()
            cax = ax.imshow(data, cmap="magma", origin="lower")
            fig.colorbar(cax, ax=ax)
            ax.axis("off")
            plt.savefig(paths, bbox_inches="tight", pad_inches=0)
            logger.info(f"File with colorbar saved to {paths}")
            plt.close(fig)
        else:
            # save image data as png
            plt.imsave(paths, data, cmap="magma", origin="lower")
            logger.info(f"File saved to {paths}")

    def rename(self) -> None:
        """
        Renames files
        """
        pass

"""
def main():
    #target_name = "../fit_files/jw01334-o003_t003_nircam_clear-f480m_i2d.fits"
    #target_name = "../fit_files/jw01701-o052_t007_nircam_clear-f140m-sub640_i2d.fits"
    #target_name = "../fit_files/jw01701-o052_t007_nircam_f150w2-f164n-sub640_i2d.fits"
    #target_name = "../fit_files/jw01701052001_02106_00014_nrcb3_i2d.fits"
    #target_name = "../fit_files/jw04098001001_04101_00001-seg003_nis_calints.fits"
    #target_name = "../fit_files/jw03730008001_03101_00001-seg004_mirimage_calints.fits"
    #target_name = "../fit_files/jw01701052001_02106_00016_nrcblong_cal.fits"
    target_name = "downloaded_fits/jw03368-o140_t001_nircam_clear-f356w-sub160p_i2d.fits"
    #target_name = "../fit_files/jw01701052001_02106_00016_nrcblong_i2d.fits"
    ok = Processing()
    ok.inspect_fits_content(target_name)
    data = ok.process_fits(target_name, use_asinh=True)
    ok.visualize_fits(data)

if __name__ == "__main__":
    main()

"""
