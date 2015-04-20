#Going to model the outcome variable version_count using an
#ols regression.

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv('/Users/ilya/metis/week2/project2/clean_data.csv')
del data['Unnamed: 0']
data['minor_award_wins_and_noms'] = data['minor_award_wins'] + \
    data['minor_award_noms']

predictors = ['total_gross', 'year', 'metascore', 'major_award_wins_or_noms', 
    'version_count', 'minor_award_wins_and_noms', 'votecount_clean']
data = data[predictors]
data = data.dropna(subset = predictors)

#Model version_count using total_gross, major_award_wins and year.
fit1 = smf.ols("version_count ~ year + major_award_wins_or_noms", data).fit()
print fit1.summary()
sm.graphics.plot_fit(fit1, 2)
plt.show()

#Do the same in seaborn:


resids1 = fit1.resid
plt.hist(resids1)
plt.title('Histogram of residuals')
plt.show()
