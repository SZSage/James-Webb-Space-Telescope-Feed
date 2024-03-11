#!/bin/bash

# stop script on error
set -e

# run webscraper and setup SQL database
cd ./tests
pytest mast_query_test.py
process_id=$!
wait $process_id
echo "tests executed"
cd ../WebScraping
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
python3 ./main.py
process_id=$!
wait $process_id
echo "fetch process main.py executed"
#cd ../nebulanet
#npm install -g serve
#serve -s build
#cd ..
#echo "run_script execution complete!"
