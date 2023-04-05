# %% imports

import pandas as pd
import math
import matplotlib.pyplot as plt
import csv
import krippendorff
import numpy as np

pd.set_option('display.max_rows', 500)

# %% params

# Android
AND_APPS = "data/Android/processed/app_store_data.csv"
AND_ALL_REVIEWS = "data/Android/processed/reviews_english.csv"
AND_FILTERED_REVIEWS = "data/Android/processed/reviews_filtered.csv"
AND_SAMPLED_REVIEWS = "data/companion_apps_sample.xlsx"

# iOS
IOS_APPS = "data/iOS/processed/app_store_data.csv"
IOS_ALL_REVIEWS = "data/iOS/processed/reviews_english.csv"
IOS_FILTERED_REVIEWS = "data/iOS/processed/reviews_filtered.csv"
IOS_SAMPLED_REVIEWS = "data/companion_apps_sample.xlsx"


# %% load data

# Android
a_all_reviews = pd.read_csv(AND_ALL_REVIEWS, delimiter=";")
a_filtered_reviews = pd.read_csv(AND_FILTERED_REVIEWS, delimiter=";")
a_sampled_reviews = pd.read_excel(AND_SAMPLED_REVIEWS,sheet_name="Android")
a_apps = pd.read_csv(AND_APPS, delimiter=";")

# iOS
i_all_reviews = pd.read_csv(IOS_ALL_REVIEWS, delimiter=";")
i_filtered_reviews = pd.read_csv(IOS_FILTERED_REVIEWS, delimiter=";")
i_sampled_reviews = pd.read_excel(IOS_SAMPLED_REVIEWS,sheet_name="iOS")
i_apps = pd.read_csv(IOS_APPS, delimiter=";")

# Filter out apps without reviews
i_apps = i_apps[i_apps['reviews'] > 0]

# %% Parse year of reviews

a_all_reviews['date'] = pd.to_datetime(a_all_reviews['date'])
a_all_reviews['year'] = a_all_reviews['date'].dt.year
a_all_reviews['month'] = a_all_reviews['date'].dt.month

a_filtered_reviews['date'] = pd.to_datetime(a_filtered_reviews['date'])
a_filtered_reviews['year'] = a_filtered_reviews['date'].dt.year
a_filtered_reviews['month'] = a_filtered_reviews['date'].dt.month

i_all_reviews['date'] = pd.to_datetime(i_all_reviews['updated'])
i_all_reviews['year'] = i_all_reviews['date'].dt.year
i_all_reviews['month'] = i_all_reviews['date'].dt.month

i_filtered_reviews['date'] = pd.to_datetime(i_filtered_reviews['updated'])
i_filtered_reviews['year'] = i_filtered_reviews['date'].dt.year
i_filtered_reviews['month'] = i_filtered_reviews['date'].dt.month

# %% descriptive stats 

a_all_reviews.describe()
a_filtered_reviews.describe()
a_apps.describe()

i_all_reviews.describe()
i_filtered_reviews.describe()
i_apps.describe()

# %% Newest/Oldest reviews

print(max(a_all_reviews['date']))
print(min(a_all_reviews['date']))

print(max(i_all_reviews['date']))
print(min(i_all_reviews['date']))

# %% check frequencies of scores and sentiments

# Android
print(a_all_reviews['score'].value_counts(normalize=True).apply(lambda x: round(x,2)))

print(a_all_reviews['sentiment'].value_counts(normalize=True).apply(lambda x: round(x,2)))

#iOS
print(i_all_reviews['score'].value_counts(normalize=True).apply(lambda x: round(x,2)))

print(i_all_reviews['sentiment'].value_counts(normalize=True).apply(lambda x: round(x,2)))

# %% compute score frequencies by year

a_freqs_by_year = a_all_reviews[a_all_reviews['score'] > 0] 
i_freqs_by_year = i_all_reviews[i_all_reviews['score'] > 0] 

a_year_counts = a_freqs_by_year.groupby(['year']).count()['id']
i_year_counts = i_freqs_by_year.groupby(['year']).count()['id']

a_freqs_by_year = a_freqs_by_year.groupby(['year', 'score']).size()
i_freqs_by_year = i_freqs_by_year.groupby(['year', 'score']).size()

a_freqs_by_year = round(a_freqs_by_year / a_year_counts, 2) * 100
i_freqs_by_year = round(i_freqs_by_year / i_year_counts, 2) * 100

a_freqs_by_year = a_freqs_by_year.reset_index()
i_freqs_by_year = i_freqs_by_year.reset_index()

# Add zeros for years with missing data points
a_freqs_by_year.loc[-1] = [2010, 1, 0]
a_freqs_by_year.loc[-2] = [2010, 4, 0]
a_freqs_by_year.index = a_freqs_by_year.index + 2  # shifting index
a_freqs_by_year.sort_index(inplace=True)

i_freqs_by_year.loc[-1] = [2008, 1, 0]
i_freqs_by_year.loc[-2] = [2008, 2, 0]
i_freqs_by_year.index = i_freqs_by_year.index + 2  # shifting index
i_freqs_by_year.sort_index(inplace=True)
i_freqs_by_year.loc[-1] = [2009, 1, 0]
i_freqs_by_year.loc[-2] = [2009, 2, 0]
i_freqs_by_year.index = i_freqs_by_year.index + 2  # shifting index
i_freqs_by_year.sort_index(inplace=True)
i_freqs_by_year.loc[-1] = [2010, 2, 0]
i_freqs_by_year.loc[-2] = [2010, 3, 0]
i_freqs_by_year.index = i_freqs_by_year.index + 2  # shifting index
i_freqs_by_year.sort_index(inplace=True)

a_freqs_by_year = a_freqs_by_year.reset_index()
i_freqs_by_year = i_freqs_by_year.reset_index()
i_freqs_by_year.sort_values('year', inplace=True)


# %% plot score frequencies by year

# Android
# Prepare data
data = a_freqs_by_year
data.columns = ['Index', 'Year', 'Score', 'Ratio']
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

plt.xlim((2010,2021.25))
plt.ylim((0,72))
plt.gca().axvspan(2010, 2010.5, facecolor='gray', alpha=0.25)
plt.axvline(x=2010.5, linestyle ="--", color='black', alpha=0.55)

plt.legend(['1 Star', '2 Stars', '3 Stars', '4 Stars', '5 Stars'], loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=5, fancybox=True, shadow=True, prop={'size': 8.5})
plt.xticks(rotation=65)
plt.gca().xaxis.set_major_locator(plt.MultipleLocator(1))
plt.gca().yaxis.set_minor_locator(plt.MultipleLocator(5))
plt.gca().yaxis.grid(True, linestyle='-.', which='both')

plt.xlabel("Year", size=12)
plt.ylabel("Score %", size=12)
plt.tight_layout()
plt.savefig('figures/android_scores_by_year.pdf', facecolor='white', dpi=600)
plt.clf()

# iOS
# Prepare data
data = i_freqs_by_year
data.columns = ['Index', 'Year', 'Score', 'Ratio']
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

plt.xlim((2008,2021.25))
plt.ylim((0,72))
plt.gca().axvspan(2008, 2013.5, facecolor='gray', alpha=0.25)
plt.axvline(x=2013.5, linestyle ="--", color='black', alpha=0.55)

plt.legend(['1 Star', '2 Stars', '3 Stars', '4 Stars', '5 Stars'], loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=5, fancybox=True, shadow=True, prop={'size': 8.5})
plt.xticks(rotation=65)
plt.gca().xaxis.set_major_locator(plt.MultipleLocator(1))
plt.gca().yaxis.set_minor_locator(plt.MultipleLocator(5))
plt.gca().yaxis.grid(True, linestyle='-.', which='both')

plt.xlabel("Year", size=12)
plt.ylabel("Score %", size=12)
plt.tight_layout()
plt.savefig('figures/ios_scores_by_year.pdf', facecolor='white', dpi=600)

# %% sentiment frequencies

a_sentiments = a_all_reviews['sentiment'].value_counts(normalize=True).apply(lambda x: round(x,2))
i_sentiments = i_all_reviews['sentiment'].value_counts(normalize=True).apply(lambda x: round(x,2))

# %% sentiment by year

a_sentiments_by_year = a_all_reviews[a_all_reviews['score'] > 0]
i_sentiments_by_year = i_all_reviews[i_all_reviews['score'] > 0]

a_year_counts = a_sentiments_by_year.groupby(['year']).count()['id']
i_year_counts = i_sentiments_by_year.groupby(['year']).count()['id']

a_sentiments_by_year = a_sentiments_by_year.groupby(['year', 'sentiment']).size()
i_sentiments_by_year = i_sentiments_by_year.groupby(['year', 'sentiment']).size()

a_sentiments_by_year = round(a_sentiments_by_year / a_year_counts, 2) * 100
i_sentiments_by_year = round(i_sentiments_by_year / i_year_counts, 2) * 100

a_sentiments_by_year = a_sentiments_by_year.reset_index()
i_sentiments_by_year = i_sentiments_by_year.reset_index()

# Add missing data points
a_sentiments_by_year.loc[-1] = [2010, 'NEGATIVE', 0]
a_sentiments_by_year.sort_values('year', inplace=True)

i_sentiments_by_year.loc[-1] = [2008, 'NEGATIVE', 0]
i_sentiments_by_year.loc[-2] = [2008, 'NEUTRAL', 0]
i_sentiments_by_year.loc[-3] = [2009, 'NEUTRAL', 0]
i_sentiments_by_year.loc[-4] = [2010, 'NEUTRAL', 0]
i_sentiments_by_year.loc[-5] = [2010, 'NEGATIVE', 0]
i_sentiments_by_year.sort_values('year', inplace=True)

# %% Plot sentiment by year

# Android
# Prepare data
data = a_sentiments_by_year
data.columns = ['Year', 'Sentiment', 'Ratio']
score_neu = data[data['Sentiment'] == 'NEUTRAL'] 
score_pos = data[data['Sentiment'] == 'POSITIVE']
score_neg = data[data['Sentiment'] == 'NEGATIVE']

plt.plot(score_pos['Year'], score_pos['Ratio'], marker='.')
plt.plot(score_neu['Year'], score_neu['Ratio'], marker='.')
plt.plot(score_neg['Year'], score_neg['Ratio'], marker='.')

plt.xlim((2010,2021.25))
plt.ylim((0,100))
plt.gca().axvspan(2010, 2010.5, facecolor='gray', alpha=0.25)
plt.axvline(x=2010.5, linestyle ="--", color='black', alpha=0.55)

plt.legend(['Positive', 'Neutral', 'Negative'], loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=5, fancybox=True, shadow=True, prop={'size': 8.5})
plt.xticks(rotation=65)
plt.gca().xaxis.set_major_locator(plt.MultipleLocator(1))
plt.gca().yaxis.set_minor_locator(plt.MultipleLocator(5))
plt.gca().yaxis.grid(True, linestyle='-.', which='both')

plt.xlabel("Year", size=12)
plt.ylabel("Sentiment %", size=12)
plt.tight_layout()
plt.savefig('figures/android_sentiment_by_year.pdf', facecolor='white', dpi=600)
plt.clf()

# iOs
# Prepare data
data = i_sentiments_by_year
data.columns = ['Year', 'Sentiment', 'Ratio']
score_neu = data[data['Sentiment'] == 'NEUTRAL'] 
score_pos = data[data['Sentiment'] == 'POSITIVE']
score_neg = data[data['Sentiment'] == 'NEGATIVE']

plt.plot(score_pos['Year'], score_pos['Ratio'], marker='.')
plt.plot(score_neu['Year'], score_neu['Ratio'], marker='.')
plt.plot(score_neg['Year'], score_neg['Ratio'], marker='.')

plt.xlim((2008,2021.25))
plt.ylim((0,100))
plt.gca().axvspan(2008, 2013.5, facecolor='gray', alpha=0.25)
plt.axvline(x=2013.5, linestyle ="--", color='black', alpha=0.55)

plt.legend(['Positive', 'Neutral', 'Negative'], loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=5, fancybox=True, shadow=True, prop={'size': 8.5})
plt.xticks(rotation=65)
plt.gca().xaxis.set_major_locator(plt.MultipleLocator(1))
plt.gca().yaxis.set_minor_locator(plt.MultipleLocator(5))
plt.gca().yaxis.grid(True, linestyle='-.', which='both')

plt.xlabel("Year", size=12)
plt.ylabel("Sentiment %", size=12)
plt.tight_layout()
plt.savefig('figures/ios_sentiment_by_year.pdf', facecolor='white', dpi=600)

# %% Mean scores/sentiment by year

for year in range(2008, 2022):
    a = a_all_reviews[a_all_reviews['year'] == year]
    i = i_all_reviews[i_all_reviews['year'] == year]

    print(year, round(a['score'].mean(),2), round(i['score'].mean(),2), round(a['sentiment_score'].mean(),2), round(i['sentiment_score'].mean(),2), len(a), len(i))

# %% Check score differences by year
import scipy
from scipy import stats

a_old = a_all_reviews[a_all_reviews['year'].between(2011, 2013, inclusive = True)]
a_new = a_all_reviews[a_all_reviews['year'].between(2019, 2021, inclusive = True)]

i_old = i_all_reviews[i_all_reviews['year'].between(2014, 2016, inclusive = True)]
i_new = i_all_reviews[i_all_reviews['year'].between(2019, 2021, inclusive = True)]

scipy.stats.mannwhitneyu(a_old['score'], a_new['score'], alternative = 'greater')
scipy.stats.mannwhitneyu(a_old['sentiment_score'], a_new['sentiment_score'], alternative = 'greater')

scipy.stats.mannwhitneyu (i_old['score'], i_new['score'],  alternative = 'greater')
scipy.stats.mannwhitneyu (i_old['sentiment_score'], i_new['sentiment_score'], alternative = 'greater')

print(round(a_old['score'].mean(),2), round(a_new['score'].mean(),2), round(a_old['sentiment_score'].mean(),2), round(a_new['sentiment_score'].mean(),2), len(a_old), len(a_new))
print(round(i_old['score'].mean(),2), round(i_new['score'].mean(),2), round(i_old['sentiment_score'].mean(),2), round(i_new['sentiment_score'].mean(),2), len(i_old), len(i_new))

# %% Scores and sentiments trend analysis

# Compute score frequencies by month
a_freqs_by_month = a_all_reviews[a_all_reviews['score'] > 0] 
i_freqs_by_month = i_all_reviews[i_all_reviews['score'] > 0] 

a_monthly_counts = a_freqs_by_month.groupby(['year', 'month']).count()['id']
i_monthly_counts = i_freqs_by_month.groupby(['year', 'month']).count()['id']

a_freqs_by_month = a_freqs_by_month.groupby(['year', 'month', 'score']).size()
i_freqs_by_month = i_freqs_by_month.groupby(['year', 'month', 'score']).size()

a_freqs_by_month = round(a_freqs_by_month / a_monthly_counts, 2) * 100
i_freqs_by_month = round(i_freqs_by_month / i_monthly_counts, 2) * 100

a_freqs_by_month = a_freqs_by_month.reset_index()
i_freqs_by_month = i_freqs_by_month.reset_index()

a_freqs_by_month.columns = ['Year', 'Month', 'Score', 'Ratio']
i_freqs_by_month.columns = ['Year', 'Month', 'Score', 'Ratio']

# Compute sentiments by month
a_sentiments_by_month = a_all_reviews[a_all_reviews['score'] > 0]
i_sentiments_by_month = i_all_reviews[i_all_reviews['score'] > 0]  

a_monthly_counts = a_sentiments_by_month.groupby(['year', 'month']).count()['id']
i_monthly_counts = i_sentiments_by_month.groupby(['year', 'month']).count()['id']

a_sentiments_by_month = a_sentiments_by_month.groupby(['year', 'month', 'sentiment']).size()
i_sentiments_by_month = i_sentiments_by_month.groupby(['year', 'month', 'sentiment']).size()

a_sentiments_by_month = round(a_sentiments_by_month / a_monthly_counts, 2) * 100
i_sentiments_by_month = round(i_sentiments_by_month / i_monthly_counts, 2) * 100

a_sentiments_by_month = a_sentiments_by_month.reset_index()
i_sentiments_by_month = i_sentiments_by_month.reset_index()

a_sentiments_by_month.columns = ['Year', 'Month', 'Sentiment', 'Ratio']
i_sentiments_by_month.columns = ['Year', 'Month', 'Sentiment', 'Ratio']

# Select data for the test

a_freqs = a_freqs_by_year  
i_freqs =  i_freqs_by_year 
a_sentiments = a_sentiments_by_year  
i_sentiments =  i_sentiments_by_year 

# a_freqs = a_freqs_by_month 
# i_freqs =  i_freqs_by_month
# a_sentiments = a_sentiments_by_month
# i_sentiments =  i_sentiments_by_month

# Divide by score/sentiment
a_one_star = a_freqs[a_freqs['Score'] == 1]
a_two_star = a_freqs[a_freqs['Score'] == 2]
a_three_star = a_freqs[a_freqs['Score'] == 3]
a_four_star = a_freqs[a_freqs['Score'] == 4]
a_five_star = a_freqs[a_freqs['Score'] == 5]

i_one_star = i_freqs[i_freqs['Score'] == 1]
i_two_star = i_freqs[i_freqs['Score'] == 2]
i_three_star = i_freqs[i_freqs['Score'] == 3]
i_four_star = i_freqs[i_freqs['Score'] == 4]
i_five_star = i_freqs[i_freqs['Score'] == 5]

a_pos = a_sentiments[a_sentiments['Sentiment'] == 'POSITIVE']
a_neg = a_sentiments[a_sentiments['Sentiment'] == 'NEGATIVE']
a_neu = a_sentiments[a_sentiments['Sentiment'] == 'NEUTRAL']

i_pos = i_sentiments[i_sentiments['Sentiment'] == 'POSITIVE']
i_neg = i_sentiments[i_sentiments['Sentiment'] == 'NEGATIVE']
i_neu = i_sentiments[i_sentiments['Sentiment'] == 'NEUTRAL']

# Remove years with low sample
a_one_star = a_one_star[a_one_star['Year'] > 2010]
a_two_star = a_two_star[a_two_star['Year'] > 2010]
a_three_star = a_three_star[a_three_star['Year'] > 2010]
a_four_star = a_four_star[a_four_star['Year'] > 2010]
a_five_star = a_five_star[a_five_star['Year'] > 2010]

i_one_star = i_one_star[i_one_star['Year'] > 2013]
i_two_star = i_two_star[i_two_star['Year'] > 2013]
i_three_star = i_three_star[i_three_star['Year'] > 2013]
i_four_star = i_four_star[i_four_star['Year'] > 2013]
i_five_star = i_five_star[i_five_star['Year'] > 2013]

a_pos = a_pos[a_pos['Year'] > 2010]
a_neg = a_neg[a_neg['Year'] > 2010]
a_neu = a_neu[a_neu['Year'] > 2010]

i_pos = i_pos[i_pos['Year'] > 2013]
i_neg = i_neg[i_neg['Year'] > 2013]
i_neu = i_neu[i_neu['Year'] > 2013]

def adf_test(timeseries):
    print("Results of Dickey-Fuller Test:")
    dftest = adfuller(timeseries, autolag="AIC", regression="c")
    dfoutput = pd.Series(
        dftest[0:4],
        index=[
            "Test Statistic",
            "p-value",
            "#Lags Used",
            "Number of Observations Used",
        ],
    )
    for key, value in dftest[4].items():
        dfoutput["Critical Value (%s)" % key] = value
    print(dfoutput)

def kpss_test(timeseries):
    print("Results of KPSS Test:")
    kpsstest = kpss(timeseries, regression="c", nlags="auto")
    kpss_output = pd.Series(
        kpsstest[0:3], index=["Test Statistic", "p-value", "Lags Used"]
    )
    for key, value in kpsstest[3].items():
        kpss_output["Critical Value (%s)" % key] = value
    print(kpss_output)

from statsmodels.tsa.stattools import adfuller, kpss

series = [
    {'name': 'Android 1 Star', 'values': a_one_star},
    {'name': 'Android 2 Star', 'values': a_two_star},
    {'name': 'Android 3 Star', 'values': a_three_star},
    {'name': 'Android 4 Star', 'values': a_four_star},
    {'name': 'Android 5 Star', 'values': a_five_star},

    {'name': 'Android Positive', 'values': a_pos},
    {'name': 'Android Negative', 'values': a_neg},
    {'name': 'Android Neutral', 'values': a_neu},

    {'name': 'iOS 1 Star', 'values': i_one_star},
    {'name': 'iOS 2 Star', 'values': i_two_star},
    {'name': 'iOS 3 Star', 'values': i_three_star},
    {'name': 'iOS 4 Star', 'values': i_four_star},
    {'name': 'iOS 5 Star', 'values': i_five_star},

    {'name': 'iOS Positive', 'values': i_pos},
    {'name': 'iOS Negative', 'values': i_neg},
    {'name': 'iOS Neutral', 'values': i_neu},
    ]

# ADF Test
for x in series:
    print(x['name'])
    adf_test(x['values']['Ratio'])

# KPSS Test
#for x in series:
#    print(x['name'])
#    kpss_test(x['values']['Ratio'])

# %% Visual inspection of test results

# Android

adf_test(a_one_star['Ratio'])
#kpss_test(a_one_star['Ratio'])
a_one_star['Ratio'].plot()

adf_test(a_two_star['Ratio'])
#kpss_test(a_two_star['Ratio'])
a_two_star['Ratio'].plot()

adf_test(a_three_star['Ratio'])
#kpss_test(a_three_star['Ratio'])
a_three_star['Ratio'].plot()

adf_test(a_four_star['Ratio'])
#kpss_test(a_four_star['Ratio'])
a_four_star['Ratio'].plot()

adf_test(a_five_star['Ratio'])
#kpss_test(a_five_star['Ratio'])
a_five_star['Ratio'].plot()

adf_test(a_pos['Ratio'])
#kpss_test(a_pos['Ratio'])
a_pos['Ratio'].plot()

adf_test(a_neg['Ratio'])
#kpss_test(a_neg['Ratio'])
a_neg['Ratio'].plot()

adf_test(a_neu['Ratio'])
#kpss_test(a_neu['Ratio'])
a_neu['Ratio'].plot()

# iOS

adf_test(i_one_star['Ratio'])
#kpss_test(a_one_star['Ratio'])
i_one_star['Ratio'].plot()

adf_test(i_two_star['Ratio'])
#kpss_test(a_two_star['Ratio'])
i_two_star['Ratio'].plot()

adf_test(i_three_star['Ratio'])
#kpss_test(a_three_star['Ratio'])
i_three_star['Ratio'].plot()

adf_test(i_four_star['Ratio'])
#kpss_test(a_four_star['Ratio'])
i_four_star['Ratio'].plot()

adf_test(i_five_star['Ratio'])
#kpss_test(a_five_star['Ratio'])
i_five_star['Ratio'].plot()

adf_test(i_pos['Ratio'])
#kpss_test(a_pos['Ratio'])
i_pos['Ratio'].plot()

adf_test(i_neg['Ratio'])
#kpss_test(a_neg['Ratio'])
i_neg['Ratio'].plot()

adf_test(i_neu['Ratio'])
#kpss_test(a_neu['Ratio'])
i_neu['Ratio'].plot()


# %% Krippendorf Aplha in sample

r1 = a_sampled_reviews['App_or_device_R1'][:499]
r2 = a_sampled_reviews['App_or_device_R2'][:499]

sum(r1 == r2)/len(r1 == r2)

r1 = [ord(v) for v in r1] 
r2 = [ord(v) for v in r2] 

print("Android {}".format(krippendorff.alpha(reliability_data=[r1, r2], level_of_measurement='nominal')))

r1 = i_sampled_reviews['App_or_device_R1'][:499]
r2 = i_sampled_reviews['App_or_device_R2'][:499]

sum(r1 == r2)/len(r1 == r2)

r1 = [ord(v) for v in r1] 
r2 = [ord(v) for v in r2] 

print("iOS {}".format(krippendorff.alpha(reliability_data=[r1, r2], level_of_measurement='nominal')))

# %% Counts

# A = app-related
# D = device-related
# B = both
# U = unclear

print(a_sampled_reviews['App_or_device_Final'].value_counts())
print(i_sampled_reviews['App_or_device_Final'].value_counts())

# %% Process manual labels 

# remove unclear reviews
#a_sampled_reviews = a_sampled_reviews[a_sampled_reviews.App_or_device_Final != 'U'] 
#i_sampled_reviews = i_sampled_reviews[i_sampled_reviews.App_or_device_Final != 'U'] 

a_sampled_reviews['Labels_Final'] = a_sampled_reviews['Labels_Final'].apply(lambda x: str(x).lower().strip())
i_sampled_reviews['Labels_Final'] = i_sampled_reviews['Labels_Final'].apply(lambda x: str(x).lower().strip())

def split_clean(x):
    elems = [y.strip() for y in str(x).lower().split(',')]
    return elems 
     
labels = set()
i_sampled_reviews['Labels_Final'].apply(lambda x: labels.update(split_clean(x)))
a_sampled_reviews['Labels_Final'].apply(lambda x: labels.update(split_clean(x)))
print(labels)
print(len(labels))

def type_counts(bool_flag):
    a = a_sampled_reviews[a_sampled_reviews[bool_flag] == True]['App_or_device_Final'].value_counts() 
    b = i_sampled_reviews[i_sampled_reviews[bool_flag] == True]['App_or_device_Final'].value_counts()
    print('Android')
    print(a)
    print('iOS')
    print(b)


# Privacy issues
a_sampled_reviews['is_privacy'] = a_sampled_reviews['Labels_Final'].str.contains('privacy issues')
i_sampled_reviews['is_privacy'] = i_sampled_reviews['Labels_Final'].str.contains('privacy issues')
print("Privacy issues: {} Android, {} iOS".format(sum(a_sampled_reviews['is_privacy']),sum(i_sampled_reviews['is_privacy'])))
type_counts('is_privacy')


# Energy consumption
a_sampled_reviews['is_battery'] = a_sampled_reviews['Labels_Final'].str.contains('battery drain')
i_sampled_reviews['is_battery'] = i_sampled_reviews['Labels_Final'].str.contains('battery drain')
print("Battery drain: {} Android, {} iOS".format(sum(a_sampled_reviews['is_battery']),sum(i_sampled_reviews['is_battery'])))
type_counts('is_battery')

# Dangerous
i_sampled_reviews['is_dangerous'] = i_sampled_reviews['Labels_Final'].str.contains('dangerous')
a_sampled_reviews['is_dangerous'] = a_sampled_reviews['Labels_Final'].str.contains('dangerous')
print("Dangerous: {} Android, {} iOS".format(sum(a_sampled_reviews['is_dangerous']),sum(i_sampled_reviews['is_dangerous'])))
type_counts('is_dangerous')

# Dark patterns
i_sampled_reviews['is_dark_pattern'] = i_sampled_reviews['Labels_Final'].str.contains('dark pattern')
a_sampled_reviews['is_dark_pattern'] = a_sampled_reviews['Labels_Final'].str.contains('dark pattern')
print("Dark pattern: {} Android, {} iOS".format(sum(a_sampled_reviews['is_dark_pattern']),sum(i_sampled_reviews['is_dark_pattern'])))
type_counts('is_dark_pattern')

# Platform fragmentation
i_sampled_reviews['is_platform_fragmentation'] = i_sampled_reviews['Labels_Final'].str.contains('platform fragmentation')
a_sampled_reviews['is_platform_fragmentation'] = a_sampled_reviews['Labels_Final'].str.contains('platform fragmentation')
print("Platform fragmentation: {} Android, {} iOS".format(sum(a_sampled_reviews['is_platform_fragmentation']),sum(i_sampled_reviews['is_platform_fragmentation'])))
type_counts('is_platform_fragmentation')

# Login issues
i_sampled_reviews['is_login'] = i_sampled_reviews['Labels_Final'].str.contains('login issues')
a_sampled_reviews['is_login'] = a_sampled_reviews['Labels_Final'].str.contains('login issues')
print("Login issues: {} Android, {} iOS".format(sum(a_sampled_reviews['is_login']),sum(i_sampled_reviews['is_login'])))
type_counts('is_login')

# Feature request
# feature request + update request
i_sampled_reviews['is_feature_request'] = i_sampled_reviews['Labels_Final'].str.contains('feature request')
a_sampled_reviews['is_feature_request'] = a_sampled_reviews['Labels_Final'].str.contains('feature request')

i_sampled_reviews['is_update'] = i_sampled_reviews['Labels_Final'].str.contains('updated request')
a_sampled_reviews['is_update'] = a_sampled_reviews['Labels_Final'].str.contains('update request')

i_sampled_reviews['is_feature_request'] = i_sampled_reviews['is_update'] | i_sampled_reviews['is_feature_request']
a_sampled_reviews['is_feature_request'] = a_sampled_reviews['is_update'] | a_sampled_reviews['is_feature_request']

print("Feature request: {} Android, {} iOS".format(sum(a_sampled_reviews['is_feature_request']),sum(i_sampled_reviews['is_feature_request'])))
type_counts('is_feature_request')

# Bad documentation
i_sampled_reviews['is_bad_documentation'] = i_sampled_reviews['Labels_Final'].str.contains('bad documentation')
a_sampled_reviews['is_bad_documentation'] = a_sampled_reviews['Labels_Final'].str.contains('bad documentation')
print("Bad documentation: {} Android, {} iOS".format(sum(a_sampled_reviews['is_bad_documentation']),sum(i_sampled_reviews['is_bad_documentation'])))
type_counts('is_bad_documentation')

# Security issues
i_sampled_reviews['is_security'] = i_sampled_reviews['Labels_Final'].str.contains('security issue')
a_sampled_reviews['is_security'] = a_sampled_reviews['Labels_Final'].str.contains('security issue')
print("Security issues: {} Android, {} iOS".format(sum(a_sampled_reviews['is_security']),sum(i_sampled_reviews['is_security'])))
type_counts('is_security')

# Flakiness
i_sampled_reviews['is_flakiness'] = i_sampled_reviews['Labels_Final'].str.contains('flakiness')
a_sampled_reviews['is_flakiness'] = a_sampled_reviews['Labels_Final'].str.contains('flakiness')
print("Flakiness: {} Android, {} iOS".format(sum(a_sampled_reviews['is_flakiness']),sum(i_sampled_reviews['is_flakiness'])))
type_counts('is_flakiness')

# Connection/Pairing issues
i_sampled_reviews['is_connection'] = i_sampled_reviews['Labels_Final'].str.contains('connection issues')
a_sampled_reviews['is_connection'] = a_sampled_reviews['Labels_Final'].str.contains('connection issues')
print("Connection/Pairing issues: {} Android, {} iOS".format(sum(a_sampled_reviews['is_connection']),sum(i_sampled_reviews['is_connection'])))
type_counts('is_connection')

# 3rd party service issues
i_sampled_reviews['is_third'] = i_sampled_reviews['Labels_Final'].str.contains('3rd party integration issues')
a_sampled_reviews['is_third'] = a_sampled_reviews['Labels_Final'].str.contains('3rd party integration issues')
print("3rd party integration issues: {} Android, {} iOS".format(sum(a_sampled_reviews['is_third']),sum(i_sampled_reviews['is_third'])))
type_counts('is_third')

# Notification issues
i_sampled_reviews['is_notification'] = i_sampled_reviews['Labels_Final'].str.contains('notification issues')
a_sampled_reviews['is_notification'] = a_sampled_reviews['Labels_Final'].str.contains('notification issues')
print("Notification issues: {} Android, {} iOS".format(sum(a_sampled_reviews['is_notification']),sum(i_sampled_reviews['is_notification'])))
type_counts('is_notification')

# End of support
i_sampled_reviews['is_eos'] = i_sampled_reviews['Labels_Final'].str.contains('end of support')
a_sampled_reviews['is_eos'] = a_sampled_reviews['Labels_Final'].str.contains('end of support')
print("End of support: {} Android, {} iOS".format(sum(a_sampled_reviews['is_eos']),sum(i_sampled_reviews['is_eos'])))
type_counts('is_eos')

# Server issues
i_sampled_reviews['is_server'] = i_sampled_reviews['Labels_Final'].str.contains('server issues')
a_sampled_reviews['is_server'] = a_sampled_reviews['Labels_Final'].str.contains('server issues')
print("Server issues: {} Android, {} iOS".format(sum(a_sampled_reviews['is_server']),sum(i_sampled_reviews['is_server'])))
type_counts('is_server')

# UI Issues
i_sampled_reviews['is_UI'] = i_sampled_reviews['Labels_Final'].str.contains('ui issues')
a_sampled_reviews['is_UI'] = a_sampled_reviews['Labels_Final'].str.contains('ui issues')
print("UI issues: {} Android, {} iOS".format(sum(a_sampled_reviews['is_UI']),sum(i_sampled_reviews['is_UI'])))
type_counts('is_UI')

# Setup issues
i_sampled_reviews['is_setup'] = i_sampled_reviews['Labels_Final'].str.contains('setup issues')
a_sampled_reviews['is_setup'] = a_sampled_reviews['Labels_Final'].str.contains('setup issues')
print("Setup issues: {} Android, {} iOS".format(sum(a_sampled_reviews['is_setup']),sum(i_sampled_reviews['is_setup'])))
type_counts('is_setup')

# Sync issues
i_sampled_reviews['is_sync'] = i_sampled_reviews['Labels_Final'].str.contains('sync issues')
a_sampled_reviews['is_sync'] = a_sampled_reviews['Labels_Final'].str.contains('sync issues')
print("Sync issues: {} Android, {} iOS".format(sum(a_sampled_reviews['is_sync']),sum(i_sampled_reviews['is_sync'])))
type_counts('is_sync')

# Crash
i_sampled_reviews['is_crash'] = i_sampled_reviews['Labels_Final'].str.contains('crash')
a_sampled_reviews['is_crash'] = a_sampled_reviews['Labels_Final'].str.contains('crash')
print("Crash: {} Android, {} iOS".format(sum(a_sampled_reviews['is_crash']),sum(i_sampled_reviews['is_crash'])))
type_counts('is_crash')

# Stopped working
i_sampled_reviews['is_stop'] = i_sampled_reviews['Labels_Final'].str.contains('stopped working')
a_sampled_reviews['is_stop'] = a_sampled_reviews['Labels_Final'].str.contains('stopped working')
print("Crash: {} Android, {} iOS".format(sum(a_sampled_reviews['is_stop']),sum(i_sampled_reviews['is_stop'])))
type_counts('is_stop')

# Unspecified bug
i_sampled_reviews['is_bug'] = i_sampled_reviews['Labels_Final'].str.contains('bug')
a_sampled_reviews['is_bug'] = a_sampled_reviews['Labels_Final'].str.contains('bug')

# Has to be labeled with bug but not with other functional issues
i_sampled_reviews['is_bug'] = i_sampled_reviews['is_bug'] & ~i_sampled_reviews['is_crash'] & ~i_sampled_reviews['is_connection'] & ~i_sampled_reviews['is_flakiness'] & ~i_sampled_reviews['is_platform_fragmentation'] & ~i_sampled_reviews['is_login'] & ~i_sampled_reviews['is_third'] & ~i_sampled_reviews['is_notification'] & ~i_sampled_reviews['is_server'] & ~i_sampled_reviews['is_sync'] & ~i_sampled_reviews['is_stop'] & ~i_sampled_reviews['is_setup']

a_sampled_reviews['is_bug'] = a_sampled_reviews['is_bug'] & ~a_sampled_reviews['is_crash'] & ~a_sampled_reviews['is_connection'] & ~a_sampled_reviews['is_flakiness'] & ~a_sampled_reviews['is_platform_fragmentation'] & ~a_sampled_reviews['is_login'] & ~a_sampled_reviews['is_third'] & ~a_sampled_reviews['is_notification'] & ~a_sampled_reviews['is_server'] & ~a_sampled_reviews['is_sync'] & ~a_sampled_reviews['is_stop'] & ~a_sampled_reviews['is_setup']

print("Unspecified bug: {} Android, {} iOS".format(sum(a_sampled_reviews['is_bug']),sum(i_sampled_reviews['is_bug'])))
type_counts('is_bug')

# Sign up issues
i_sampled_reviews['is_signup'] = i_sampled_reviews['Labels_Final'].str.contains('sign up issues')
a_sampled_reviews['is_signup'] = a_sampled_reviews['Labels_Final'].str.contains('sign up issues')
print("Signup issues: {} Android, {} iOS".format(sum(a_sampled_reviews['is_signup']),sum(i_sampled_reviews['is_signup'])))
type_counts('is_signup')

# Broken update
i_sampled_reviews['is_broken_update'] = i_sampled_reviews['Labels_Final'].str.contains('broken update')
a_sampled_reviews['is_broken_update'] = a_sampled_reviews['Labels_Final'].str.contains('broken update')
print("Broken update: {} Android, {} iOS".format(sum(a_sampled_reviews['is_broken_update']),sum(i_sampled_reviews['is_broken_update'])))
type_counts('is_broken_update')

# Performance issues
# delay + slow + lag + freeze

i_sampled_reviews['is_delay'] = i_sampled_reviews['Labels_Final'].str.contains('delay')
a_sampled_reviews['is_delay'] = a_sampled_reviews['Labels_Final'].str.contains('delay')

i_sampled_reviews['is_slow'] = i_sampled_reviews['Labels_Final'].str.contains('slow')
a_sampled_reviews['is_slow'] = a_sampled_reviews['Labels_Final'].str.contains('slow')

i_sampled_reviews['is_lag'] = i_sampled_reviews['Labels_Final'].str.contains('lag')
a_sampled_reviews['is_lag'] = a_sampled_reviews['Labels_Final'].str.contains('lag')

i_sampled_reviews['is_freeze'] = i_sampled_reviews['Labels_Final'].str.contains('freeze')
a_sampled_reviews['is_freeze'] = a_sampled_reviews['Labels_Final'].str.contains('freeze')

i_sampled_reviews['is_performance'] = i_sampled_reviews['is_delay'] | i_sampled_reviews['is_slow'] | i_sampled_reviews['is_lag'] | i_sampled_reviews['is_freeze']
a_sampled_reviews['is_performance'] = a_sampled_reviews['is_delay'] | a_sampled_reviews['is_slow'] | a_sampled_reviews['is_lag'] | a_sampled_reviews['is_freeze']

print("Performance issues: {} Android, {} iOS".format(sum(a_sampled_reviews['is_performance']),sum(i_sampled_reviews['is_performance'])))
type_counts('is_performance')

# %% Count of all labels 

a_sampled_reviews['is_any'] = a_sampled_reviews['is_battery'] |  a_sampled_reviews['is_performance'] |  a_sampled_reviews['is_bug'] |  a_sampled_reviews['is_crash'] |  a_sampled_reviews['is_connection'] |  a_sampled_reviews['is_flakiness'] |  a_sampled_reviews['is_platform_fragmentation'] |  a_sampled_reviews['is_login'] |  a_sampled_reviews['is_third'] |  a_sampled_reviews['is_notification'] |  a_sampled_reviews['is_server'] |  a_sampled_reviews['is_sync'] |  a_sampled_reviews['is_stop'] |  a_sampled_reviews['is_privacy'] |  a_sampled_reviews['is_dangerous'] |  a_sampled_reviews['is_dark_pattern'] |  a_sampled_reviews['is_feature_request'] |  a_sampled_reviews['is_broken_update'] |  a_sampled_reviews['is_eos'] |  a_sampled_reviews['is_UI'] | a_sampled_reviews['is_setup'].astype(int)


i_sampled_reviews['is_any'] = i_sampled_reviews['is_battery'] |  i_sampled_reviews['is_performance'] |  i_sampled_reviews['is_bug'] |  i_sampled_reviews['is_crash'] |  i_sampled_reviews['is_connection'] |  i_sampled_reviews['is_flakiness'] |  i_sampled_reviews['is_platform_fragmentation'] |  i_sampled_reviews['is_login'] |  i_sampled_reviews['is_third'] |  i_sampled_reviews['is_notification'] |  i_sampled_reviews['is_server'] |  i_sampled_reviews['is_sync'] |  i_sampled_reviews['is_stop'] |  i_sampled_reviews['is_privacy'] |  i_sampled_reviews['is_dangerous'] |  i_sampled_reviews['is_dark_pattern'] |  i_sampled_reviews['is_feature_request'] |  i_sampled_reviews['is_broken_update'] |  i_sampled_reviews['is_eos'] |  i_sampled_reviews['is_UI'] | i_sampled_reviews['is_setup'].astype(int)

print("Android: {} total labeled reviews".format(sum(a_sampled_reviews['is_any'])))
print("iOS: {} total labeled reviews".format(sum(i_sampled_reviews['is_any'])))

##

a_sampled_reviews['label_count'] = a_sampled_reviews['is_battery'].astype(int) +  a_sampled_reviews['is_performance'].astype(int) +  a_sampled_reviews['is_bug'].astype(int) +  a_sampled_reviews['is_crash'].astype(int) +  a_sampled_reviews['is_connection'].astype(int) +  a_sampled_reviews['is_flakiness'].astype(int) +  a_sampled_reviews['is_platform_fragmentation'].astype(int) +  a_sampled_reviews['is_login'].astype(int) +  a_sampled_reviews['is_third'].astype(int) +  a_sampled_reviews['is_notification'].astype(int) +  a_sampled_reviews['is_server'].astype(int) +  a_sampled_reviews['is_sync'].astype(int) +  a_sampled_reviews['is_stop'].astype(int) +  a_sampled_reviews['is_privacy'].astype(int) +  a_sampled_reviews['is_dangerous'].astype(int) +  a_sampled_reviews['is_dark_pattern'].astype(int) +  a_sampled_reviews['is_feature_request'].astype(int) +  a_sampled_reviews['is_broken_update'].astype(int) +  a_sampled_reviews['is_eos'].astype(int) +  a_sampled_reviews['is_UI'].astype(int) + a_sampled_reviews['is_setup'].astype(int)

i_sampled_reviews['label_count'] = i_sampled_reviews['is_battery'].astype(int) +  i_sampled_reviews['is_performance'].astype(int) +  i_sampled_reviews['is_bug'].astype(int) +  i_sampled_reviews['is_crash'].astype(int) +  i_sampled_reviews['is_connection'].astype(int) +  i_sampled_reviews['is_flakiness'].astype(int) +  i_sampled_reviews['is_platform_fragmentation'].astype(int) +  i_sampled_reviews['is_login'].astype(int) +  i_sampled_reviews['is_third'].astype(int) +  i_sampled_reviews['is_notification'].astype(int) +  i_sampled_reviews['is_server'].astype(int) +  i_sampled_reviews['is_sync'].astype(int) +  i_sampled_reviews['is_stop'].astype(int) +  i_sampled_reviews['is_privacy'].astype(int) +  i_sampled_reviews['is_dangerous'].astype(int) +  i_sampled_reviews['is_dark_pattern'].astype(int) +  i_sampled_reviews['is_feature_request'].astype(int) +  i_sampled_reviews['is_broken_update'].astype(int) +  i_sampled_reviews['is_eos'].astype(int) +  i_sampled_reviews['is_UI'].astype(int) + i_sampled_reviews['is_setup'].astype(int)

print("Android: {} total labels".format(sum(a_sampled_reviews['label_count'])))
print("iOS: {} total labels".format(sum(i_sampled_reviews['label_count'])))


# %% Co-location pairs
import nltk
from nltk.collocations import *

bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()
fourgram_measures = nltk.collocations.QuadgramAssocMeasures()

finder = BigramCollocationFinder.from_words(
    ' '.join([x for x in i_all_reviews['text']][:-4]).split(),
    window_size = 20)

finder.apply_freq_filter(2)

ignored_words = nltk.corpus.stopwords.words('english')
finder.apply_word_filter(lambda w: len(w) < 3 or w.lower() in ignored_words)

pairs = finder.nbest(bigram_measures.likelihood_ratio, 100)

#triples = finder.nbest(trigram_measures.likelihood_ratio, 100)
#quadruples = finder.nbest(fourgram_measures.likelihood_ratio, 100)

# %% extract app name from url

all_reviews['app'] = all_reviews['url'].apply(lambda x: x.split("=")[1].split("&")[0])
