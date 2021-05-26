# %% imports

import os.path
import pandas as pd
import numpy as np
import glob
import csv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from langdetect import detect, DetectorFactory
DetectorFactory.seed = 0
analyzer = SentimentIntensityAnalyzer()

# %% params

IN_FOLDER = "data/raw/reviews"
APPS_LIST = "data/raw/companion_apps_urls.csv"
OUT_FOLDER = "data/processed/reviews"
OUT_FILE = "data/processed/reviews_filtered.csv"
OUT_FILE_ALL = "data/processed/reviews_all.csv"

# %% helper fun

def detect_lang(text):
    try:
        return detect(text)
    except:
        return 'UNDEFINED'

def detect_sentiment(text):
    try:
        scores = analyzer.polarity_scores(text)
        if scores['compound'] >= 0.05:
            return "POSITIVE"
        elif scores['compound'] <= -0.05:  
            return "NEGATIVE"
        else:
            return "NEUTRAL"
    except: 
        return 'UNDEFINED'

# %% load and process reviews

apps = pd.read_csv(APPS_LIST, delimiter=";")

for index, row in apps.iterrows():

    if row['Android_URL'] is np.nan:
        continue

    app_name = row['Android_URL'].split('=')[1].split('&')[0]

    out_file_name = os.path.join(OUT_FOLDER, app_name + '.csv') 

    if os.path.isfile(out_file_name):
        print("Skipping {}".format(app_name))
        continue

    in_file_name = os.path.join(IN_FOLDER, app_name + '.json')

    print("Processing {}".format(app_name))
    
    if not os.path.isfile(in_file_name):
        continue

    file_reviews = pd.read_json(in_file_name)
    file_reviews = file_reviews.drop(['criterias', 'userImage', 'scoreText'], axis=1)
    file_reviews['app'] = app_name

    reviews_number = len(file_reviews.index)
    print("Starting reviews count {}".format(reviews_number))

    # Word count
    file_reviews['wordCount'] = file_reviews['text'].str.split().str.len().astype('Int64')

    # Remove word count < 5
    file_reviews = file_reviews[file_reviews['wordCount'] >= 5]

    # Language recognition
    file_reviews['language'] = file_reviews['text'].apply(detect_lang)

    # Remove language != english
    file_reviews = file_reviews[file_reviews['language'] == 'en']

    # Sentiment analysis 
    file_reviews['sentiment'] = file_reviews['text'].apply(detect_sentiment)

    # Remove undefined sentiment
    file_reviews = file_reviews[file_reviews['sentiment'] != 'UNDEFINED']

    filtered_count = len(file_reviews.index)
    print("Filtered reviews count {}".format(filtered_count))
    
    file_reviews.to_csv(out_file_name, sep=";", quoting=csv.QUOTE_NONNUMERIC)
    

# %% Aggregate filtered reviews in a single file

dfs = [pd.read_csv(f, delimiter=";") for f in glob.glob(os.path.join(OUT_FOLDER, "*.csv"))]
all_reviews = pd.concat(dfs)

all_reviews.to_csv(OUT_FILE, sep=";", quoting=csv.QUOTE_NONNUMERIC)
print("{} Filtered reviews".format(len(all_reviews.index)))

# %% Count unfiltered reviews

dfs = [pd.read_json(f) for f in glob.glob(os.path.join(IN_FOLDER, "*.json"))]
all_reviews = pd.concat(dfs)

all_reviews.to_csv(OUT_FILE_ALL, sep=";", quoting=csv.QUOTE_NONNUMERIC)
print("{} Filtered reviews".format(len(all_reviews.index)))

# %%
