import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

data = pd.read_csv('/Users/ilya/metis/week2/project2/clean_data.csv')

sns.regplot(data.total_gross, data.version_count, y_jitter=.5, scatter = True)
plt.show()