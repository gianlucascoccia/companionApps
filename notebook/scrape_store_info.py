# %% imports

import csv
import subprocess
import json
from json import JSONDecodeError
import os
import os.path

# %% script configuration

APPS_LIST = 'data/raw/app_list.csv'
OUT_FILE = 'data/raw/app_store_data.csv'
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
        # Run the node scraper
        scraper = subprocess.run(['node', 'store_scraper/scrape_app.js', row['id']], stdout=subprocess.PIPE)
        # sleep(randint(10, 60))
        if scraper.returncode == 0:
            try:
                output = json.loads(scraper.stdout.decode('utf-8'))
                # Check if we downloaded the app data, write to missing list otherwise
                
                if 'status' in output:
                    if output['status'] == 404:
                        error_report(row['id'])
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
                error_report(row['id'])
                continue

        else:
            error_report(row['id'])
# %%
