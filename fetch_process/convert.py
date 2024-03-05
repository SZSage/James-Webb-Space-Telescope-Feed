"""
Filename: convert.py
Author: Simon Zhao
Date Created: 01/24/2024
Date Last Modified: 03/03/2024
Description: This script automates the processes of Flexible Image Transport System (FITS) files taken from the Mikulski Archive for Space Telescopes (MAST) database.

    - Reading FITS files to extract astronomical image data.
    - Applying different scaling methods (linear, logarithmic, square root, histogram equalization, and asinh scaling) to enhance image contrast and detail visibility.
    - Converting processed image data into PNG format.
    - Visual comparison of scaling methods to help with selecting the most appropriate technique for specific data sets.
"""

from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt # type: ignore
from astropy.visualization import make_lupton_rgb, astropy_mpl_style, LogStretch, ImageNormalize
import os
from setup_logger import logger

import pprint
pp = pprint.PrettyPrinter(indent=4)

class Processing:
    def __init__(self, download_dir="processed_png") -> None:
        self.download_dir = download_dir

    def linear_scaling(self, data, scale_min=None, scale_max=None) -> np.ndarray:
        """
        Perform linear scaling on FITS data to the range [0, 1].
    
        Parameters:
            data (np.ndarray): Input data array to be scaled.
            scale_min (float, optional): Min value for scaling
            scale_max (float, optional): Max value for scaling

        Returns:
            np.ndarray: Scaled data with values between 0 and 1.
        """
        # handling NaN values and edge cases
        valid_data = data[np.isfinite(data)]
        if scale_min is None:
            scale_min = np.nanmin(valid_data)
        if scale_max is None:
            scale_max = np.nanmax(valid_data)
       
        scaled_data = (data - scale_min) / (scale_max - scale_min)
        # ensuring scaled data is within [0, 1]
        scaled_data = np.clip(scaled_data, 0, 1)
        return scaled_data

    def log_scaling(self, data: np.ndarray, scale_min=None, scale_max=None) -> np.ndarray:
        """
        Apply logarithmic scaling to the data.

        Parameters:
            data (np.ndarray): Input data array to be scaled.
            scale_min (float, optional): Minimum value for scaling.
            scale_max (float, optional): Maximum value for scaling.

        Returns:
            np.ndarray: Logarithmically scaled data
        """
        # handling of scale limits and NaN values
        valid_data = data[np.isfinite(data)]
        if scale_min is None:
            scale_min = np.nanmin(valid_data)
        if scale_max is None:
            scale_max = np.nanmax(valid_data)
            
        # avoid log(0) issues
        data_clipped = np.clip(data, scale_min, scale_max)
        scaled_data = np.log10(data_clipped - scale_min + 1) / np.log10(scale_max - scale_min + 1)
        return scaled_data


    def sqrt_scaling(self, data: np.ndarray, scale_min=None, scale_max=None) -> np.ndarray:
        """
        Apply square root scaling to the data.

        Parameters:
            data (np.ndarray): Input data array to be scaled.
            scale_min (float, optional): Minimum value for scaling.
            scale_max (float, optional): Maximum value for scaling.

        Returns:
            np.ndarray: Square root scaled data.
        """
        valid_data = data[np.isfinite(data)]
        if scale_min is None:
            scale_min = np.nanmin(valid_data)
        if scale_max is None:
            scale_max = np.nanmax(valid_data)
        
        data_clipped = np.clip(data, scale_min, scale_max)
        scaled_data = np.sqrt(data_clipped - scale_min) / np.sqrt(scale_max - scale_min)
        return scaled_data

    def hist_eq_scaling(self, data: np.ndarray) -> np.ndarray:
        """
        Apply histogram equalization scaling to the data.

        Parameters:
            data (np.ndarray): Input data array for histogram equalization.

        Returns:
            np.ndarray: Data scaled using histogram equalization.
        """
        img_hist, bins = np.histogram(data.flatten(), bins=np.arange(257))
        cdf = img_hist.cumsum()
        cdf_normalized = cdf * float(img_hist.max()) / cdf.max()
        scaled_data = np.interp(data.flatten(), bins[:-1], cdf_normalized)
        return scaled_data.reshape(data.shape)


    def asinh_scaling(self, data: np.ndarray, scale_min=None, scale_max=None, non_linear=2.0) -> np.ndarray:
        """
        Apply asinh scaling to the data.

        Parameters:
            data (np.ndarray): Input data array to be scaled.
            scale_min (float, optional): Minimum value for scaling.
            scale_max (float, optional): Maximum value for scaling.
            non_linear (float): Non-linearity factor for asinh scaling.

        Returns:
            np.ndarray: Data scaled using asinh function.
        """
        # convert data to a numpy array with a floating-point type if it's not already
        if not isinstance(data, np.ndarray) or data.dtype.kind not in "fi":
            data = np.array(data, dtype=np.float64)
        
        valid_data = data[np.isfinite(data)]
        if scale_min is None:
            scale_min = np.nanmin(valid_data)
        if scale_max is None:
            scale_max = np.nanmax(valid_data)
        
        factor = np.arcsinh((scale_max - scale_min) / non_linear)
        scaled_data = np.arcsinh((data - scale_min) / non_linear) / factor
        return scaled_data

    def compare_scaling_methods(self, fits_path: str) -> None:
        """
        Compare different scaling methods by visualizing them in a single plot.
        
        Parameters:
            fits_path (str): Path to the FITS file.
        """
        methods = ["linear", "asinh", "sqrt", "log", "hist_eq"]
        # initialize subplots
        fig, axs = plt.subplots(1, len(methods), figsize=(5 * len(methods), 5))
        
        for ax, method in zip(axs, methods):
            scaled_data = self.process_fits(fits_path, scaling_method=method)
            ax.imshow(scaled_data, cmap="magma", origin="lower")
            ax.set_title(f"{method.capitalize()} Scaling")
            ax.axis("off")
        
        plt.tight_layout()
        plt.show()

    def process_fits(self, fits_path: str, scaling_method: str, frame=0, **kwargs) -> np.ndarray:
        """
        Processes a FITS file and return scaled image data using the specified scaling method.
        
        Parameters:
            fits_path (str): Path to the FITS file.
            scaling_method (str): The scaling method to use ("asinh", "linear", "log", "sqrt", "hist_eq").
            **kwargs: Additional arguments to pass to the scaling function.
            
        Returns:
            np.ndarray: The scaled image data.
        """
        with fits.open(fits_path) as hdul:
            hdul.info()
            data = hdul[1].data # type: ignore

            if data.ndim == 3:
                data = data[frame]
            logger.info(f"IMAGE DATA IN FIRST EXTENSION: \n {data}")

            # scaling methods
            if scaling_method == "asinh":
                scaled_data = self.asinh_scaling(data, **kwargs)
            elif scaling_method == "linear":
                scaled_data = self.linear_scaling(data, **kwargs)
            elif scaling_method == "log":
                scaled_data = self.log_scaling(data, **kwargs)
            elif scaling_method == "sqrt":
                scaled_data = self.sqrt_scaling(data, **kwargs)
            elif scaling_method == "hist_eq":
                scaled_data = self.hist_eq_scaling(data, **kwargs)
            else:
                raise ValueError(f"Unknown scaling method: {scaling_method}")

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
            plt.imshow(image_data, cmap="gray")
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
        # toggle colorbar
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
