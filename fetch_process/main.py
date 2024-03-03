"""
Filename: main.py
Author: Simon Zhao
Date Created: 03/02/2024
Date Last Modified: 03/02/2024
Description: This is the main script that utilizes the MastQuery and Processing class.
"""

from mast_query import MastQuery
from convert import Processing

def main() -> None:
    # mast authorization
    mast_token = ""
    query = MastQuery("M82", "NIRCam", "downloaded_fits/")
    query.mast_auth(mast_token)

    # aquire fits data
    fits_data = query.fetch_fits_data()
    new_url = query.combine("jw01701052001_02106_00016_nrcblong_i2d.fits")
    hdul_data = query.stream_fits_data(new_url)

    # process fits data 
    fit_process = Processing()
    #processed = fit_process.process_fits(new_url, use_asinh=False)
    #fit_process.inspect_fits_content(new_url)
    
    # scaling methods
    image_asinh = fit_process.process_fits(new_url, scaling_method='asinh', non_linear=5.0)
    image_linear = fit_process.process_fits(new_url, scaling_method='linear')
    image_log = fit_process.process_fits(new_url, scaling_method='log')
    image_sqrt = fit_process.process_fits(new_url, scaling_method="sqrt")
    image_hist = fit_process.process_fits(new_url, scaling_method="hist_eq")

    # visualize data
    #fit_process.visualize_fits(image_sqrt)
    #fit_process.create_pseudo_rgb_image(new_url, "pseudo_rgb.png")
    #fit_process.convert_to_png(processed, "hello.png", True)
    fit_process.compare_scaling_methods(new_url)


if __name__ == "__main__":
    main()

