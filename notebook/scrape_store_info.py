# %% imports

import csv
import subprocess
import json
from json import JSONDecodeError
import os
import os.path
import numpy as np

# %% script configuration

APPS_LIST = 'data/companion_apps_urls.csv'
OUT_FILE = 'data/processed/app_store_data.csv'
ERROR_LOG = 'missing_data.txt'

# %% fields to write in output

app_fields = ['title', 
'description', 
'descriptionHTML', 
'summary', 
'installs', 
'minInstalls', 
'maxInstalls', 
'score', 
'scoreText', 
'ratings', 
'reviews', 
'histogram', 
'price', 
'free', 
'currency', 
'priceText', 
'offersIAP', 
'IAPRange', 
'size', 
'androidVersion', 
'androidVersionText', 
'developer', 
'developerId', 
'developerEmail', 
'developerWebsite', 
'developerAddress', 
'privacyPolicy', 
'developerInternalID', 
'genre', 
'genreId', 
'icon', 
'headerImage', 
'screenshots', 
'contentRating', 
'adSupported', 
'released', 
'updated', 
'version', 
'recentChanges', 
'comments', 
'editorsChoice', 
'appId', 
'url']

# %% error handling function

def error_report(package_name: str) -> None:
    with open(ERROR_LOG, 'a') as error_list:
        error_list.write(package_name + '\n')
        error_list.flush()
        error_list.close()

# %% funtion to write output

def write_data(data: dict) -> None:
    file_exists = os.path.isfile(OUT_FILE)
    with open(OUT_FILE, 'a') as out_file:
        w = csv.DictWriter(out_file, app_fields, delimiter=';', quoting=csv.QUOTE_MINIMAL, extrasaction='ignore')
        if not file_exists:
            w.writeheader()
        w.writerow(data)
        out_file.flush()
        out_file.close()

# %% Perform scraping

# Open apps list
with open(APPS_LIST, 'r') as csvfile:
    csvreader = csv.DictReader(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)

    # For each app in the list
    for index, row in enumerate(csvreader):

        print('Processing app N {}'.format(index))
        
        if len(row['Android_URL']) == 0:
            continue
        app_name = row['Android_URL'].split('=')[1].split('&')[0]
        
        # Run the node scraper
        scraper = subprocess.run(['node', 'store_scraper/scrape_app.js', app_name], stdout=subprocess.PIPE)
        # sleep(randint(10, 60))
        if scraper.returncode == 0:
            try:
                output = json.loads(scraper.stdout.decode('utf-8'))
                # Check if we downloaded the app data, write to missing list otherwise
                
                if 'status' in output:
                    if output['status'] == 404:
                        error_report(app_name)
                        continue
                else:
                    for field in app_fields:
                        if field not in output:
                            output[field] = 'NA'
                        else:
                            if isinstance(output[field], str):
                                output[field] = ' '.join(output[field].splitlines())
                    write_data(output)
            except JSONDecodeError:
                error_report(app_name)
                continue

        else:
            error_report(app_name)

# %%
