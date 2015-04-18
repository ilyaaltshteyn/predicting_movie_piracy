#This script calls the OMDB API to add IMDB vote count to data.

import urllib2, time, re, json
from bs4 import BeautifulSoup
import pandas as pd

#Note that you're working with movie_list4, which is the final version of
#the raw data.
data = pd.read_csv('movie_list7.csv')

def soup_maker(url):
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page)
    return soup

def dict_maker(url):
    response = urllib2.urlopen(url)
    data = json.load(response)
    return data

#Call API for each movie and return imdb rating:
for index, row in data.iterrows():
    print index
    title = row.title
    year = row.year
    title_parted = []
    for word in title.split():
        title_parted.append(word)
        title_parted.append('+')
    name_part = ''.join(title_parted[:-1])
    url = 'http://www.omdbapi.com/?t=' + name_part + '&y=' + str(year) + \
        '&plot=full&r=json'
    try:
        json_data = dict_maker(url)
    except:
        print '********API_ERROR************\n'*200
        continue
    if json_data['Response'] == 'False':
        data['imdb_vote_count'].ix[index] = 'PULL_ERROR'

    else:
        try:
            print json_data['imdbVotes']
            data['imdb_vote_count'].ix[index] = json_data['imdbVotes']

        except:
            data['imdb_vote_count'].ix[index] = 'PULL_ERROR'


