# %% imports

import subprocess
from subprocess import CalledProcessError
import csv
from time import sleep
import json
from json import JSONDecodeError
import os.path as path
from typing import Any

# %% params

APP_LIST = 'data/processed/app_store_data.csv'
OUT_FOLDER = 'data/raw/reviews/'
ERROR_LOG = "reviews_error_log.txt"
MIN_SLEEP = 5
MAX_SLEEP = 5
SLEEP = 5
LONG_SLEEP = 300
CSV_NULL_VALUE = ""
separator = ";"
reviews_num = any

# %% helper funcs

def write_error_log(_apk_package, _page, exception, _error_log):
    with open(_error_log, 'a+') as log_file:
        log_file.write("Error while downloading reviews for app " + _apk_package
                       + " at page" + str(_page)
                       + " reason: " + str(exception.__cause__) + "\n")
        log_file.flush()
        log_file.close()


def request_reviews(_apk_package, page):
    try:
        output = subprocess.check_output(["node", "store_scraper_ios/singleRevRequest.js", _apk_package, page])
    except CalledProcessError as ce:
        return []

       
    if(output.decode('utf8') == None or output.decode('utf8') == ''): 
        return 0
    else:
        temp = int(output.decode('utf8'))
        #reviews_num = int(temp)
    
        check = isinstance(temp, int)

        if(check):
            return int(temp)
    
    return 0
    

# %% run script

with open(APP_LIST, encoding="utf8") as app_list:
    app_reader = csv.DictReader(app_list, delimiter=';', quoting=csv.QUOTE_MINIMAL)
    reviews_num = 0
    
    for line in app_reader:
        # Resetto la variabile per la prossima app
        reviews_num = 0

        app_id = line['id']
        file_path = OUT_FOLDER + app_id + ".json"

        # Skip reviews already downloaded
        if path.exists(file_path):
            print("Reviews already collected for app {}".format(app_id))    
            continue
        # Ciclo per prendere le recensioni di tutte e 10 le pagine
        for count in range(1,11):
            print("Requesting reviews for app {} page: {}".format(app_id, count))
            reviews_num += int(request_reviews(app_id,str(count)))
            #request_reviews(app_id,str(count))

        print("Found {} reviews".format(reviews_num))
       
# %%
