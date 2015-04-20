#This plots some predictors against the outcome variable to see what possible
#relationships exist between the variables.

import pandas as pd
from matplotlib import pyplot as plt

data = pd.read_csv('/Users/ilya/metis/week2/project2/clean_data.csv')
del data['Unnamed: 0']


outcome = data.votecount_clean
predictor1 = data.major_award_wins_or_noms


predictors = ['total_gross', 'year', 'version_count']
    # 'rating_clean', 'release_clean2', 'runtime_mins', 'metascore',
    # 'imdb_rating', 'major_award_wins_or_noms', 'minor_award_wins',
    'minor_award_noms', 'votecount_clean']
data = data.dropna(subset = predictors)
sub_df = data.ix[:, predictors]


