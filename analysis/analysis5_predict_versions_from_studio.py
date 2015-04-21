import pandas as pd
import statsmodels.formula.api as smf
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import scipy.stats as sci
import seaborn as sns

data = pd.read_csv('/Users/ilya/metis/week2/project2/clean_data.csv')
del data['Unnamed: 0']
predictors = ['studio_name', 'version_count', 'total_gross', 'metascore',
    'imdb_rating', 'major_award_wins_or_noms', 'votecount_clean']
data = data.dropna(subset = predictors)
data = data[data.version_count > 0]
data = data[predictors]

unique_studios = set(data.studio_name)
data['studio1'] = [1 if x == 'Weinstein Company' else 0 for x \
    in data.studio_name]

fit1 = smf.ols("version_count ~ C(studio1)", data).fit()
print fit1.summary()

sm.graphics.plot_fit(fit1, 1)
plt.title('Categorical metascore predicting version count for studio1:\n\
    version_count ~ C(studio1)')
plt.show()

#Plot residuals:
plt.hist(fit1.resid)
plt.show()

#Plot residuals against feature variable:
resids1 = fit1.resid
plt.scatter(data.studio1, resids1, alpha = .2)
# plt.hlines(y = 0, xmin = -2, xmax = 12)
plt.title('Residuals plotted against model prediction')
plt.show()

#***---Transform outcome variable, boxcox:

data['version_count_boxcox'] = sci.boxcox(data.version_count + 1)[0]
fit1 = smf.ols("version_count_boxcox ~ C(studio1)", data).fit()
print fit1.summary()

sm.graphics.plot_fit(fit1, 1)
plt.title('Categorical metascore predicting version count for studio1:\n\
    version_count_boxcox ~ C(studio1)')
plt.show()

#Plot the same thing as above but in seaborn:
sns.regplot(data.studio1, data.version_count_boxcox)
plt.show()

#Plot residuals:
plt.hist(fit1.resid)
plt.show()

#Plot residuals against feature variable:
resids1 = fit1.resid
plt.scatter(data.studio1, resids1, alpha = .2)
# plt.hlines(y = 0, xmin = -2, xmax = 12)
plt.title('Residuals plotted against model prediction')
plt.show()

#***RUN SEPARATE MODELS FOR EACH STUDIO:
models_list = []
for studio in unique_studios:
    data['studio1'] = [1 if x == studio else 0 for x in data.studio_name]
    data['version_count_boxcox'] = sci.boxcox(data.version_count + 1)[0]
    fit1 = smf.ols("version_count_boxcox ~ C(studio1)", data).fit()
    models_list.append([str(studio), fit1.rsquared, fit1.params])

#***RUN MODEL THAT INCLUDES ALL STUDIOS AS CATEGORICAL VARS:
for studio in unique_studios:
    data[studio] = [1 if x == studio else 0 for x in data.studio_name]

data.columns = ['pred'+str(x) for x in range(len(data.columns))]

predictors = ['studio_name', 'version_count', 'total_gross', 'metascore',
    'imdb_rating', 'major_award_wins_or_noms', 'votecount_clean']

fit2 = smf.ols("pred1 ~ C(pred8) + C(pred9)+ C(pred10) + C(pred11) + C(pred12) + C(pred13) +\
    C(pred14) + C(pred15) + C(pred16) + C(pred17) + C(pred18) + \
    C(pred19) + C(pred20) + C(pred21)+ C(pred22) + C(pred23) + C(pred24) +\
    + C(pred25) + C(pred26)",
    data).fit()
print fit2.summary()

plt.hist(fit2.resid)
plt.show()



