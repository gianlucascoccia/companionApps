# %% imports

import subprocess
from subprocess import CalledProcessError
import csv
from time import sleep
import json
from json import JSONDecodeError
import os.path as path

# %% params

APP_LIST = "data/processed/app_store_data.csv"
OUT_FOLDER = "data/raw/reviews/"
ERROR_LOG = "reviews_error_log.txt"
MIN_SLEEP = 5
MAX_SLEEP = 5
SLEEP = 5
LONG_SLEEP = 300
CSV_NULL_VALUE = ""
separator = ";"

# %% helper funcs

def write_error_log(_apk_package, _page, exception, _error_log):
    with open(_error_log, 'a+') as log_file:
        log_file.write("Error while downloading reviews for app " + _apk_package
                       + " at page" + str(_page)
                       + " reason: " + str(exception.__cause__) + "\n")
        log_file.flush()
        log_file.close()


def request_reviews(_apk_package):
    try:
        output = subprocess.check_output(["node", "store_scraper/singleRevRequest.js", _apk_package.strip()])
    except CalledProcessError as ce:
        return []
    
    temp = output.decode('utf8')
    reviews_num = int(temp)

    return reviews_num

# %% run script

with open(APP_LIST) as app_list:
    app_reader = csv.DictReader(app_list, delimiter=';', quoting=csv.QUOTE_MINIMAL)
    
    for line in app_reader:
        
        app_id = line['appId']
        file_path = OUT_FOLDER + app_id + ".json"

        # Skip reviews already downloaded
        if path.exists(file_path):
            print("Reviews already collected for app {}".format(app_id))    
            continue
        
        print("Requesting reviews for app {}".format(app_id))
        reviews_num = request_reviews(app_id)

        print("Found {} reviews".format(reviews_num))
            
# %%
