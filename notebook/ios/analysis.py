# %% imports

import pandas as pd
import math
import matplotlib.pyplot as plt
import csv

# %% params

APPS = "data/processed/app_store_data.csv"
ALL_REVIEWS = "data/processed/reviews_all.csv"
FILTERED_REVIEWS = "data/processed/reviews_filtered.csv"

# %% load data

all_reviews = pd.read_csv(ALL_REVIEWS, delimiter=";")
filtered_reviews = pd.read_csv(FILTERED_REVIEWS, delimiter=";")

apps = pd.read_csv(APPS, delimiter=";")

# %% Parse year of reviews

all_reviews['updated'] = pd.to_datetime(all_reviews['updated'])
all_reviews['year'] = all_reviews['updated'].dt.year

filtered_reviews['updated'] = pd.to_datetime(filtered_reviews['updated'])
filtered_reviews['year'] = filtered_reviews['updated'].dt.year

# %% descriptive stats 

all_reviews.describe()
filtered_reviews.describe()
apps.describe()

# %% check frequencies of scores

freqs = all_reviews['score'].value_counts(normalize=True).apply(lambda x: round(x,2))

# %% compute frequencies by year

freqs_by_year = all_reviews[all_reviews['score'] > 0] 

year_counts = freqs_by_year.groupby(['year']).count()['id']

freqs_by_year = freqs_by_year.groupby(['year', 'score']).size()

freqs_by_year = round(freqs_by_year / year_counts, 2) * 100

# Remove year with low number of data points
freqs_by_year = freqs_by_year[3:].reset_index()

# %% plot frequencies by year

# Prepare data
data = freqs_by_year
data.columns = ['Year', 'Score', 'Ratio']
score1 = data[data['Score'] == 1] 
score2 = data[data['Score'] == 2]
score3 = data[data['Score'] == 3]
score4 = data[data['Score'] == 4]
score5 = data[data['Score'] == 5]

plt.plot(score1['Year'], score1['Ratio'], marker='.')
plt.plot(score2['Year'], score2['Ratio'], marker='.')
plt.plot(score3['Year'], score3['Ratio'], marker='.')
plt.plot(score4['Year'], score4['Ratio'], marker='.')
plt.plot(score5['Year'], score5['Ratio'], marker='.')
plt.legend(['1', '2', '3', '4', '5'], loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=5, fancybox=True, shadow=True)
plt.xticks(rotation=65)
plt.gca().xaxis.set_major_locator(plt.MultipleLocator(1))
plt.gca().yaxis.grid(True, linestyle='-.')
plt.xlabel("Year", size=12)
plt.ylabel("Score %", size=12)
plt.tight_layout()
plt.savefig('figures/scores_by_year.pdf', facecolor='white')

# %% sentiment frequencies

sentiments = filtered_reviews['sentiment'].value_counts(normalize=True).apply(lambda x: round(x,2))

# %% sentiment by year

sentiments_by_year = filtered_reviews[filtered_reviews['score'] > 0]

year_counts = sentiments_by_year.groupby(['year']).count()['id']

sentiments_by_year = sentiments_by_year.groupby(['year', 'sentiment']).size()

sentiments_by_year = round(sentiments_by_year / year_counts, 2) * 100

# Remove year with low number of data points
sentiments_by_year = sentiments_by_year[3:].reset_index()

# %%
