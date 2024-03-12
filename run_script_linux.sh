# Filenamse: run_script_linux.py
# Author: Jacob Burke
# Date Created: 02/25/2024
# Date Last Modified: 03/11/2024
# Description: run_script_linux.py executres the required programs and packages
# to create the required files/photos for the nebulanet website

#!/bin/bash

# stop script on error
set -e

# run webscraper and setup SQL database
python3 -m pytest ./fetch_process/mast_query_test.py
process_id=$!
wait $process_id
echo "tests executed"
cd ./WebScraping
python3 ./jwstDataFinder.py
process_id=$!
wait $process_id
echo "jwstDataFinder.py executed"
python3 jwstJson.py
process_id=$!
wait $process_id
echo "jwstJson.py executed"
python3 jwstDatabase.py
process_id=$!
wait $process_id
echo "jwstDatabase.py executed"
cd ../fetch_process
python3 main.py
process_id=$!
wait $process_id
echo "fetch process main.py executed"
cd ..
#python3 moveJSON.py nebulanet/src/components/testJSON.js fetch_process/obs_metadata.json
#process_id=$!
#wait $process_id
#echo "fetch process moveJSON.py executed"
#cd ./nebulanet
#npm install -g serve
#serve -s build
#cd ..
#echo "run_script execution complete!"
