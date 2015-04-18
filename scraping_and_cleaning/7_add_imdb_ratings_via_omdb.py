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

data['metascore'] = 'Untouched'
data['imdb_rating'] = 'Untouched'
data['actors'] = 'Untouched'
data['awards'] = 'Untouched'
data['director'] = 'Untouched'
data['imdb_vote_count'] = 'Untouched'
data['imdb_id'] = 'Untouched'
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
        data['metascore'].ix[index] = 'PULL_ERROR'
        data['imdb_rating'].ix[index] = 'PULL_ERROR'
        data['actors'].ix[index] = 'PULL_ERROR'
        data['awards'].ix[index] = 'PULL_ERROR'
        data['director'].ix[index] = 'PULL_ERROR'
        data['imdb_vote_count'].ix[index] = 'PULL_ERROR'
        data['imdb_id'].ix[index] = 'PULL_ERROR'

    else:
        try:
            data['metascore'].ix[index] = json_data['Metascore']
            data['imdb_rating'].ix[index] = json_data['imdbRating']
            data['actors'].ix[index] = json_data['Actors']
            data['awards'].ix[index] = json_data['Awards']
            data['director'].ix[index] = json_data['Director']
            data['imdb_vote_count'].ix[index] = json_data['imdbVotes']
            data['imdb_id'].ix[index] = json_data['imdbID']

        except:
            data['metascore'].ix[index] = 'PULL_ERROR'
            data['imdb_rating'].ix[index] = 'PULL_ERROR'
            data['actors'].ix[index] = 'PULL_ERROR'
            data['awards'].ix[index] = 'PULL_ERROR'
            data['director'].ix[index] = 'PULL_ERROR'
            data['imdb_vote_count'].ix[index] = 'PULL_ERROR'
            data['imdb_id'].ix[index] = 'PULL_ERROR'

#Remove commas from imdb_vote_count:
regex = re.sub(r'\D+','', x)
data['imdb_vote_count'] = [int(regex) for x in data['imdb_vote_count']]

#Split up wins and nominations:
data['major_award_wins_or_noms'] = 'Untouched'
data['minor_award_wins'] = 'Untouched'
data['minor_award_noms'] = 'Untouched'
for index, row in data.iterrows():
    print index
    awards_string_elements = data['awards'].ix[index].split()
    awards_numbers = [x for x in awards_string_elements if x.isdigit()]
    if len(awards_numbers) == 3:
        data['major_award_wins_or_noms'].ix[index] = awards_numbers[0]
        data['minor_award_wins'].ix[index] = awards_numbers[1]
        data['minor_award_noms'].ix[index] = awards_numbers[2]
        continue
    elif len(awards_numbers) == 2:
        data['major_award_wins_or_noms'].ix[index] = 0
        data['minor_award_wins'].ix[index] = awards_numbers[0]
        data['minor_award_noms'].ix[index] = awards_numbers[1]
        continue
    elif len(awards_numbers) == 1:
        data['major_award_wins_or_noms'].ix[index] = 0
        data['minor_award_wins'].ix[index] = 0
        data['minor_award_noms'].ix[index] = awards_numbers[0]
        continue
    elif data['awards'].ix[index] == 'PULL_ERROR':
        continue
    elif data['awards'].ix[index] == 'N/A':
        data['major_award_wins_or_noms'].ix[index] = 0
        data['minor_award_wins'].ix[index] = 0
        data['minor_award_noms'].ix[index] = 0
        continue
    else:
        continue

del data['awards']

data.to_csv(path_or_buf = "movie_list7.csv", encoding = 'utf-8')

