# %% imports

import pandas as pd
import math
from sklearn.model_selection import train_test_split

# %% params

IN_FILE = "data/processed/reviews_filtered.csv"
OUT_FILE = "data/processed/sample.csv"
SAMPLE_SIZE = 400

# %% load reviews

reviews = pd.read_csv(IN_FILE, delimiter=";")

# %% remove older reviews

reviews['date'] = pd.to_datetime(reviews['date'])
reviews = reviews[reviews['date'].dt.year >= 2019]

# %% check frequencies of scores

freqs = reviews['score'].value_counts(normalize=True).apply(lambda x: round(x,2))

# %% extract random sample

#sample = reviews.sample(SAMPLE_SIZE)

# %% extract stratified random sample 

#sample = pd.DataFrame()
#for score, freq in freqs.iteritems():
#    curr_score_rew = reviews[reviews['score'] == score]
#    curr_num = math.ceil(SAMPLE_SIZE * freq)
#    curr_sample = curr_score_rew.sample(curr_num)
#    sample = sample.append(curr_sample, ignore_index=True)
#sample = sample.sample(frac=1).reset_index(drop=True)

# %% extract stratified sample of most lengthy reviews

#sample = pd.DataFrame()
#for score, freq in freqs.iteritems():
#    curr_score_rew = reviews[reviews['score'] == score]
#    curr_num = math.ceil(SAMPLE_SIZE * freq)
#    curr_sample = curr_score_rew.sort_values(by='wordCount', ascending=False)
#    curr_sample = curr_sample.head(curr_num)
#    sample = sample.append(curr_sample, ignore_index=True)

# %% extract stratified weighted random sample 

sample = pd.DataFrame()
for score, freq in freqs.iteritems():
    curr_score_rew = reviews[reviews['score'] == score]
    curr_num = math.ceil(SAMPLE_SIZE * freq)
    curr_score_rew['w'] = 1/(1 + curr_score_rew.groupby('app')['app'].transform('size'))
    curr_sample = curr_score_rew.sample(curr_num,weights=curr_score_rew['w'], random_state=1)
    sample = sample.append(curr_sample, ignore_index=True)
sample = sample.sample(frac=1).reset_index(drop=True)

# %% nested stratified sample (score, app)

#reviews['Count'] = reviews.groupby('app')['app'].transform('size')
#reviews = reviews[reviews['Count'] > 100]  

#X_train, X_test, Y_train, Y_test = train_test_split(
#    reviews, pd.concat([reviews["score"], reviews["app"]], axis=1), stratify=pd.concat([reviews["score"], reviews["app"]], axis=1), random_state=99, test_size=400)

# %% save sample

sample.to_csv(OUT_FILE, sep = ";")

# %%
