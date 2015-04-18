import re
import pandas as pd
from matplotlib import pyplot as plt

data = pd.read_csv('movie_list5.csv')
data['release_clean2'] = [re.sub('\D+','', r) for r in data['release_clean']]

#Convert runtime to mins:
def runtime_to_mins(inp):
    try:
        runtime_list = str(inp).split()
        hours = runtime_list[0]
        mins = runtime_list[2]
        total = int(hours)*60 + int(mins)
        print runtime_list
        print hours, mins, total
        return total
    except:
        return 'CONVERSION_ERROR'

data['runtime_mins'] = [runtime_to_mins(row) for row in data['runtime_clean']]

#Remove unnecessary columns:
cols_to_del = ['Unnamed: 0', 'Unnamed: 0.1', 'Unnamed: 0.1.1', 'release',
    'genre', 'runtime', 'rating', 'release_clean', 'runtime_clean']
for name in cols_to_del:
    del data[name]

data.to_csv(path_or_buf = "movie_list6.csv", encoding = 'utf-8', 
    index = False)