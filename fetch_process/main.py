"""
Filename: main.py
Author: Simon Zhao
Date Created: 03/02/2024
Date Last Modified: 03/05/2024
Description: This is the main script that utilizes the MastQuery and Processing class.
"""

from mast_query import MastQuery
from convert import Processing

def main() -> None:
    # mast authorization
    mast_token = ""
    query = MastQuery("MCS-J1149.5+2223", "NIRCam", "downloaded_fits/")
    query.mast_auth(mast_token)
    db_path = "../WebScraping/jwstDatabaseFile.sqlite"
    #query.query_masts()
    list_of_weekly_dataframes = query.fetch_and_segment_by_week(db_path)
    weekly_count = 0
    for weekly_dataframe in list_of_weekly_dataframes:
        weekly_count += 1
        print(f"Processing week: {weekly_count} with {len(weekly_dataframe)} observation")
        query.process_all_rows_from_db(weekly_dataframe, weekly_count)

    #fit_process = Processing()
    #new_url = query.combine("jw02883-o008_s00256_nircam_f480m-grismc_x1d.fits")
    """

    hdul_data = query.stream_fits_data(new_url)

    # process fits data 
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
    """

    #fit_process.compare_scaling_methods(new_url)

if __name__ == "__main__":
    main()

