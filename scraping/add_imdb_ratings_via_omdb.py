#This script calls the OMDB API to add IMDB ratings to the dataset.

import urllib2, time, re, json
from bs4 import BeautifulSoup
import pandas as pd

#Note that you're working with movie_list4, which is the final version of
#the raw data.
data = pd.read_csv('movie_list6.csv')

def soup_maker(url):
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page)
    return soup

def dict_maker(url):
    response = urllib2.urlopen(url)
    data = json.load(response)
    return data

#Call API for each movie and return imdb rating:

template = 'http://www.omdbapi.com/?t=' + title[0] + '+' + title[2]etc +
'&y=' + year + '&plot=full&r=json'

title = 'Django Unchained'
year= '2012'
data['metascore'] = 'Untouched'
data['imdb_rating'] = 'Untouched'
data['actors'] = 'Untouched'
data['awards'] = 'Untouched'
data['director'] = 'Untouched'
data['imdb_vote_count'] = 'Untouched'
data['imdb_id'] = 'Untouched'
for index, row in data.iterrows():
    if index == 3:
        break
    title = row.title
    year = row.year
    title_parted = []
    for word in title.split():
        title_parted.append(word)
        title_parted.append('+')
    name_part = ''.join(title_parted[:-1])
    url = 'http://www.omdbapi.com/?t=' + name_part + '&y=' + str(year) + \
        '&plot=full&r=json'
    json_data = dict_maker(url)
    if 'Response' in json_data:
        row['metascore'] = 'PULL_ERROR'
    else:
        try:
            row['metascore'] = json_data['Metascore']
    print json_data    

    print url