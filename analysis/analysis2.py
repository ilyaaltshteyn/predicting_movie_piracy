#This analysis tries to fit a bunch of different negative binomial models and
#ranks them by AIC. The models are fit on various combinations of all numerical
#predictor variables.

import pandas as pd
import itertools

data = pd.read_csv('/Users/ilya/metis/week2/project2/clean_data.csv')
del data['Unnamed: 0']

#Create all the stuff you need to make negative binomial models, 
#from: http://bit.ly/1H7QG4A
import numpy as np
from scipy.stats import nbinom
def _ll_nb2(y, X, beta, alph):
     mu = np.exp(np.dot(X, beta))
     size = 1 / alph
     prob = size / (size + mu)
     ll = nbinom.logpmf(y, size, prob)
     return ll

#Create new model class that inherits from GenericLikelihoodModel:
from statsmodels.base.model import GenericLikelihoodModel
class NBin(GenericLikelihoodModel):
     def __init__(self, endog, exog, **kwds):
         super(NBin, self).__init__(endog, exog, **kwds)
     def nloglikeobs(self, params):
         alph = params[-1]
         beta = params[:-1]
         ll = _ll_nb2(self.endog, self.exog, beta, alph)
         return -ll
     def fit(self, start_params=None, maxiter=10000, maxfun=5000, **kwds):
         if start_params == None:
             # Reasonable starting values
             start_params = np.append(np.zeros(self.exog.shape[1]), .5)
             start_params[0] = np.log(self.endog.mean())
         return super(NBin, self).fit(start_params=start_params,
                                      maxiter=maxiter, maxfun=maxfun,
                                      **kwds)

predictors = ['total_gross', 'year', 'release_clean2', 'runtime_mins', 'metascore',
    'imdb_rating', 'major_award_wins_or_noms', 'minor_award_wins',
    'minor_award_noms', 'votecount_clean']

def model_maker(predictors_list):
    model_in = "version_count ~"
    for x in predictors_list:
        model_in += x + "+"
    model_in = model_in[:-1]
    return model_in

import patsy
data = data.dropna(subset = predictors)
model_spec = model_maker(predictors)

#Outcome var is version_count
#Input var is total_gross
y, X = patsy.dmatrices(model_spec, data)
# print y[:5]
# print X[:5]

mod = NBin(y, X)
res = mod.fit()

print res.summary()












