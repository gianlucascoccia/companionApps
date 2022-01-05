# %% imports

import csv
from io import StringIO
import subprocess
import json
from json import JSONDecodeError
import os
import os.path

# %% script configuration

APPS_LIST = 'store_scraper_ios/data/raw/companion_apps_urls.csv'
OUT_FILE = 'store_scraper_ios/data/processed/app_store_data.csv'
OUT_FILE_MISS = 'store_scraper_ios/data/processed/app_mancanti.txt'
ERROR_LOG = 'missing_data.txt'

# %% fields to write in output

app_fields = ['id',
'appId',
'title',
'url',
'description',
'icon',
'genres',
'genreIds', 
'primaryGenre', 
'primaryGenreId', 
'contentRating', 
'languages', 
'size', 
'srequiredOsVersion', 
'relased', 
'updated', 
'releaseNotes', 
'version',
'price',  
'currency',
'free', 
'developerId', 
'developer', 
'developerUrl', 
'developerWebsite',
'score', 
'reviews', 
'currentVersionScore', 
'currentVersionReviews', 
'screenshots', 
'appletvScreenshots', 
'supportedDevices'
]

# %% error handling function

def error_report(package_name: str) -> None:
    with open(ERROR_LOG, 'a') as error_list:
        error_list.write(package_name + '\n')
        error_list.flush()
        error_list.close()

# %% funtion to write output

def write_data(data: dict) -> None:
   
   # controllo che le info dell'app siano presenti,se si salvo tutto nel csv, altrimenti inserisco l'id dell'app (assente) in un file txt
    if data[field] != 'NA':
            file_exists = os.path.isfile(OUT_FILE)
            with open(OUT_FILE, 'a', encoding='utf-8') as out_file:
                w = csv.DictWriter(out_file, app_fields, delimiter=';', quoting=csv.QUOTE_MINIMAL, extrasaction='ignore')
                if not file_exists:
                    w.writeheader()
                w.writerow(data)
                out_file.flush()
                out_file.close()
    else:
         file_exists = os.path.isfile(OUT_FILE_MISS)
         with open(OUT_FILE_MISS, 'a', encoding='utf-8') as out_file_miss:
                out_file_miss.write(app_id + '\n')
                out_file_miss.flush()
                out_file_miss.close()

# %% Perform scraping

# Open apps list
with open(APPS_LIST, 'r') as csvfile:
    csvreader = csv.DictReader(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)

    # For each app in the list
    for index, row in enumerate(csvreader):

        print('Processing app N {}'.format(index))
        if len(row['iOS_URL']) == 0:
            continue
        app_id = row['iOS_URL'].replace('=','').split('/')[-1].split('id')[1].split('?')[0].split('&')[0]
        
        # Run the node scraper
        scraper = subprocess.run(['node', 'store_scraper_ios/scrape_app.js', app_id], stdout=subprocess.PIPE)
        # sleep(randint(10, 60))
        if scraper.returncode == 0:
            try:
                output = json.loads(scraper.stdout.decode('utf-8'))
                # Check if we downloaded the app data, write to missing list otherwise
                
                if 'status' in output:
                    if output['status'] == 404:
                        error_report(app_id)
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
                error_report(app_id)
                continue

        else:
            error_report(app_id)

# %%
