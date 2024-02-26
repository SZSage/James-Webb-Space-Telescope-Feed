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
from matplotlib.colors import LogNorm
from typing import Any

class Processing:
    def __init__(self) -> None:
        pass


    def asinh_scaling(self, data: np.ndarray, beta: float =5.0) -> np.ndarray:
        """
        Apply asinh scaling to the data.
        Parameters:
        - data: 2D numpy array, the image data to scale.
        - beta: float, scaling factor controlling the transition between linear and log.

        Returns:
        - Scaled data as a 2D numpy array.
        """
        data = data.astype(np.float64)
        scaled_data = np.arcsinh(data / beta) / np.arcsinh(1.0 / beta)
        return scaled_data


    def process_fits(self, fits_path: str, use_asinh: bool = False, beta: float = 5.0) -> np.ndarray:
        """
        Processes a FITS file and return the scaled image data.
        """
        with fits.open(fits_path) as hdul:
            # image data in first extension
            data = hdul[1].data
            if use_asinh:
                # apply asinh scaling
                scaled_data = self.asinh_scaling(data, beta=beta)
            else:
                # apply log10 scaling, ensure no log(0) issues
                data[data <= 0] = np.nan  
                scaled_data = np.log10(data)
                # handles NaNs
                scaled_data = np.nan_to_num(scaled_data, nan=0.0)
                
            # normalize scaled data for display
            scaled_data = (scaled_data - np.nanmin(scaled_data)) / (np.nanmax(scaled_data) - np.nanmin(scaled_data))
            return scaled_data


def main():
    target_name = "fits/jw01701-o052_t007_nircam_clear-f140m-sub640_i2d.fits"
    #target_name = "fits/jw01701052001_02106_00016_nrcblong_i2d.fits"
    #target_name = "fits/jw01701052001_02106_00016_nrcblong_cal.fits"
    ok = Processing()
    process = ok.process_fits(target_name, use_asinh=True)

if __name__ == "__main__":
    main()
