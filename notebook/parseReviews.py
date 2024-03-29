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

IN_FOLDER = "data/Android/raw/reviews"
APPS_LIST = "data/Android/processed/app_store_data.csv"
OUT_FOLDER = "data/Android/processed/reviews"
OUT_FILE = "data/Android/processed/reviews_english2.csv"
OUT_FILE_ALL = "data/Android/processed/reviews_all2.csv"

FILTER_WORDS = False
FILTER_LANGUAGE = True
FILTER_SENTIMENT = False

# %% helper fun

def detect_lang(text):
    try:
        return detect(text)
    except:
        return 'UNDEFINED'

def detect_sentiment(text):
    try:
        scores = analyzer.polarity_scores(text)
        return scores['compound']
    except: 
        return np.nan

def parse_sentiment(score):
    try:
        if score >= 0.05:
            return "POSITIVE"
        elif score <= -0.05:  
            return  "NEGATIVE"
        else:
            return "NEUTRAL"
    except: 
        return 'UNDEFINED'

# %% load and process reviews

apps = pd.read_csv(APPS_LIST, delimiter=";")

for index, row in apps.iterrows():

    if row['appId'] is np.nan:
        continue

    app_name = row['appId']

    out_file_name = os.path.join(OUT_FOLDER, '{}.csv'.format(app_name)) 

    if os.path.isfile(out_file_name):
        print("Skipping {}".format(app_name))
        continue

    in_file_name = os.path.join(IN_FOLDER, '{}.json'.format(app_name))

    print("Processing {}".format(app_name))
    
    if not os.path.isfile(in_file_name):
        continue

    file_reviews = pd.read_json(in_file_name)
    try:
        file_reviews = file_reviews.drop(['criterias', 'userImage', 'scoreText'], axis=1)
    except KeyError:
        pass
    file_reviews['app'] = app_name

    reviews_number = len(file_reviews.index)
    print("Starting reviews count {}".format(reviews_number))

    # Word count
    file_reviews['wordCount'] = file_reviews['text'].str.split().str.len().astype('Int64')

    # Remove word count < 5
    if FILTER_WORDS:
        file_reviews = file_reviews[file_reviews['wordCount'] >= 5]

    # Language recognition
    file_reviews['language'] = file_reviews['text'].apply(detect_lang)

    # Remove language != english
    if FILTER_LANGUAGE:
        file_reviews = file_reviews[file_reviews['language'] == 'en']

    # Sentiment analysis 
    file_reviews['sentiment_score'] = np.nan
    file_reviews['sentiment_score'] = file_reviews['text'].apply(detect_sentiment)
    file_reviews['sentiment'] = file_reviews['sentiment_score'].apply(parse_sentiment)

    # Remove undefined sentiment
    if FILTER_SENTIMENT:
        file_reviews = file_reviews[file_reviews['sentiment'] != 'UNDEFINED']

    filtered_count = len(file_reviews.index)
    print("Filtered reviews count {}".format(filtered_count))
    
    file_reviews.to_csv(out_file_name, sep=";", quoting=csv.QUOTE_NONNUMERIC)
    

# %% Aggregate filtered reviews in a single file

dfs = [pd.read_csv(f, delimiter=";") for f in glob.glob(os.path.join(OUT_FOLDER, "*.csv"))]
all_reviews = pd.concat(dfs)
all_reviews = all_reviews.drop(["Unnamed: 0"], axis = 1 )

all_reviews.to_csv(OUT_FILE, sep=";", quoting=csv.QUOTE_NONNUMERIC)
print("{} Filtered reviews".format(len(all_reviews.index)))

# %% Count unfiltered reviews

dfs = [pd.read_json(f) for f in glob.glob(os.path.join(IN_FOLDER, "*.json"))]
all_reviews = pd.concat(dfs)
all_reviews = all_reviews.drop(['criterias', 'userImage', 'scoreText'], axis=1)

all_reviews.to_csv(OUT_FILE_ALL, sep=";", quoting=csv.QUOTE_NONNUMERIC)
print("{} Unfiltered reviews".format(len(all_reviews.index)))


# %%
