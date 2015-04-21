import pandas as pd
import statsmodels.formula.api as smf
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import scipy.stats as sci
import seaborn as sns

data = pd.read_csv('/Users/ilya/metis/week2/project2/clean_data.csv')
del data['Unnamed: 0']
predictors = ['studio_name', 'version_count']
data = data.dropna(subset = predictors)
data = data[data.version_count > 0]
data = data[['studio_name', 'version_count']]

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

data.columns = ['studio'+str(x) for x in range(len(data.columns))]

fit2 = smf.ols("studio3 ~ C(studio5) + C(studio6) + C(studio7) + C(studio8) + \
    C(studio9)+ C(studio10) + C(studio11) + C(studio12) + C(studio13) + \
    C(studio14) + C(studio15) + C(studio16) + C(studio17) + C(studio18) + \
    C(studio19) + C(studio20) + C(studio21)+ C(studio22) + C(studio23)",
    data).fit()
print fit2.summary()

plt.hist(fit2.resid)
plt.show()



