import pandas as pd
import numpy as np
import re

data = pd.read_csv('/Users/ilya/metis/week2/project2/clean_data.csv')
del data['Unnamed: 0']


#The goal of the following is to turn all missing values to NaN and all other
#numeric values to floats.
#First, convert everything to strings:
for col in data:
    data[col] = [str(item) for item in data[col]]
    
non_numeric_columns = ['title', 'studio_name', 'studio_abbrev', 'opening_date',
        'link', 'putlocker_url', 'genre_clean', 'actors', 'director', 
        'imdb_id']
#Next, convert all numeric columns to float if they don't contain digits, and
#to none if they contain missing values or non-digits.
p = re.compile(r'\D+')
for col in data:
    if col in non_numeric_columns:
        continue
    else:
        data[col] = [float(item) if p.match(item) == None else None for 
            item in data[col]]

data.to_csv(path_or_buf = "/Users/ilya/metis/week2/project2/movie_list9.csv")
