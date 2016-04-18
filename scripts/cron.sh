#!/usr/bin/env bash

DIR="$( cd "$( dirname "$0" )" && pwd )"
cd $DIR

python database_updater.py

source ../../../bin/activate 
# this is for the test server. Might differ on different machines. Ideally it should be "source ../../bin/activate"



cd crawler/

scrapy crawl tbc_spider -o items.json -t json 
#sadly scrapy can only be run in the folders containing scrapy.cfg

cd ../.

python split_json.py

deactivate

