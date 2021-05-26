# %% imports

import csv
import requests
import json
from bs4 import BeautifulSoup
import pandas as pd

# %% script configuration

PRODUCTS_FILE = 'data/raw/products_urls.csv'
OUT_FILE = 'data/raw/companion_apps_urls.csv'
BASE_URL = 'https://www.smarthomedb.com'

PRODUCTS_URL = BASE_URL + '/products?ProductName=&filterName=Software&Category=&VoiceCategory=&Software=1,3&CompanyNameRef=&Features=&Connectivity=&PowerSupply=&Price=0,27224&Reviews=0,35009&Star=&CompatibilityCount=0,424&productSort=Review%20DESC&productShowColumn=OSCompatibility&R_Category=OR&R_VoiceCategory=OR&R_Software=OR&R_Features=AND&R_Connectivity=OR&R_PowerSupply=OR&page={}'

APPS_URL = '/product/getsectiondata?productInnerId=P{}&section=apps&customdata='

MAX_PAGE = 33

# %% scrape all product urls

product_urls = []

for p in range(1, MAX_PAGE + 1):
    url = PRODUCTS_URL.format(p)

    page = requests.get(url)
    print(page.status_code)
    if page.status_code == 200:
        
        soup = BeautifulSoup(page.content, 'html.parser')
        page_urls = [a.get("href") for a in  soup.findAll("a", {"class":"item-logo"})]
        product_urls.extend(page_urls)
        
# %% Save products file

with open(PRODUCTS_FILE, 'w+') as pf:
    pf.writelines([a + '\n' for a in product_urls])
    pf.flush()

# %% Parse product pages

apps = []

for p in product_urls:
    p_id = p.split('/')[-1][1:]
    url = BASE_URL + APPS_URL.format(p_id.zfill(8))

    page = requests.get(url)

    print(url)
    print(page.status_code)

    if page.status_code == 200:
        content = json.loads(page.content)
        soup = BeautifulSoup(content['data'], 'html.parser')
        
        # Extract app urls
        store_urls = [a.get("href") for a in  soup.findAll("a", {"class":"outbound-link"})]

        # Find Android url
        try:
            android_url = next(filter(lambda x: 'play.google.com' in x, store_urls))
        except StopIteration:
            android_url = ''

        # Find iOS url
        try:
            ios_url = next(filter(lambda x: 'itunes.apple.com' in x, store_urls))
        except StopIteration:
            ios_url = ''

        app = {
            'product': BASE_URL + p,
            'Android_URL': android_url,
            'iOS_URL': ios_url
        }

        apps.append(app)

# %% Save results

apps_out = pd.DataFrame(apps)
apps_out.to_csv(OUT_FILE, sep=";")

# %%

