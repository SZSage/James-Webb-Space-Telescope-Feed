!/bin/bash

# stop script on error
set -e

# run webscraper and setup SQL database
python3 jwstDataFinder.py
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
