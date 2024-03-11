"""
Filename: main.py
Author: Simon Zhao
Date Created: 03/02/2024
Date Last Modified: 03/08/2024
Description: This is the main script that utilizes the MastQuery and Processing class.
"""

from mast_query import MastQuery
import time

def main() -> None:
    start = time.time()
    # mast authorization
    
    with open("token.txt", "r+") as file:
        mast_token = file.readline().strip()

    query = MastQuery("processed_png/")
    query.mast_auth(mast_token)
    db_path = "../WebScraping/jwstDatabaseFile.sqlite"

    weekly_dataframes = query.fetch_and_segment_by_week(db_path)
    
    query.process_weekly_observations(weekly_dataframes)
    

    end = time.time()
    print("The time of execution of above program is :",(end-start), "seconds")

if __name__ == "__main__":
    main()

