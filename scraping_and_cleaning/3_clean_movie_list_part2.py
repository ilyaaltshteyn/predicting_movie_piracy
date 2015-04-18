#This script fixes NO_URL_ERRORs. A lot of the time, these happen because 
#movies have punctuation in the title. Some of the time, these are movies 
#that have the year wrong.

import urllib2, re
from bs4 import BeautifulSoup
import pandas as pd

data = pd.read_csv('movie_list2.csv')

#Remove punctuation from titles:
regex = r'[^a-zA-Z\d\s]'
data.title = [re.sub(regex, '', row) for row in data.title]

#Re-define functions used to figure out proper url:
def soup_maker(url):
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page)
    return soup

def go_to_movie(movie_name, year):
    """Removes apostrophes from movie name, creates 2 possible urls for
    putlocker page for the movie and returns the urls."""
    url1 = "http://putlocker.is/watch-"
    url2 = "http://putlocker.is/watch-"
    movie_subbed = re.sub("[']",'',movie_name).split()

    for x in movie_subbed:
        url1 += x + '-'
        url2 += x + '-'

    url1 += str(year) + '-online-free-putlocker.html'
    url2 += 'online-free-putlocker.html'
    return url1, url2

def proper_movie_url(row):
    """Figures out which of the 2 possible URLs is the proper one. If both
    work, then it returns MULTI_URL_ERROR."""
    movie_name = row['title']
    year = row['year']
    print row['Unnamed: 0']
    url1, url2 = go_to_movie(movie_name, year)
    try:
        html1 = urllib2.urlopen(url1)
    except:
        html1 = 0
    try:
        html2 = urllib2.urlopen(url2)
    except:
        html2 = 0
    if html1 != 0 and html2 != 0:
        return 'MULTI_URL_ERROR'
        print 'MULTI_URL_ERROR'
    elif html1 != 0:
        return url1
    elif html2 != 0:
        return url2
    else:
        return 'NO_URL_ERROR'
        print 'NO_URL_ERROR'

#Re-run proper_movie_url on rows where putlocker_url says NO_URL_ERROR:
for row in data.index:
    if data.ix[row]['putlocker_url'] == 'NO_URL_ERROR':
        print data.ix[row]['putlocker_url']
        data.ix[row,'putlocker_url'] = proper_movie_url(data.ix[row])
        print data.ix[row]['putlocker_url']

def proper_movie_url_plus_year(row):
    """Figures out which of the 2 possible URLs is the proper one, but does
    this for one year ahead of the normal year. Useful because sometimes,
    movie years differ between putlocker and BOM. If both work, then it 
    returns MULTI_URL_ERROR."""
    movie_name = row['title']
    year = str(int(row['year']) + 1)
    print row['Unnamed: 0']
    url1, url2 = go_to_movie(movie_name, year)
    try:
        html1 = urllib2.urlopen(url1)
    except:
        html1 = 0
    try:
        html2 = urllib2.urlopen(url2)
    except:
        html2 = 0
    if html1 != 0 and html2 != 0:
        return 'MULTI_URL_ERROR'
        print 'MULTI_URL_ERROR'
    elif html1 != 0:
        return url1
    elif html2 != 0:
        return url2
    else:
        return 'NO_URL_ERROR'
        print 'NO_URL_ERROR'

for row in data.index:
    if data.ix[row]['putlocker_url'] == 'NO_URL_ERROR':
        print data.ix[row]['putlocker_url']
        data.ix[row,'putlocker_url'] = proper_movie_url_plus_year(data.ix[row])
        print data.ix[row]['putlocker_url']

def proper_movie_url_minus_year(row):
    """Figures out which of the 2 possible URLs is the proper one, but does
    this for one year ahead of the normal year. Useful because sometimes,
    movie years differ between putlocker and BOM. If both work, then it 
    returns MULTI_URL_ERROR."""
    movie_name = row['title']
    year = str(int(row['year']) - 1)
    print row['Unnamed: 0']
    url1, url2 = go_to_movie(movie_name, year)
    try:
        html1 = urllib2.urlopen(url1)
    except:
        html1 = 0
    try:
        html2 = urllib2.urlopen(url2)
    except:
        html2 = 0
    if html1 != 0 and html2 != 0:
        return 'MULTI_URL_ERROR'
        print 'MULTI_URL_ERROR'
    elif html1 != 0:
        return url1
    elif html2 != 0:
        return url2
    else:
        return 'NO_URL_ERROR'
        print 'NO_URL_ERROR'

for row in data.index:
    if data.ix[row]['putlocker_url'] == 'NO_URL_ERROR':
        print data.ix[row]['putlocker_url']
        data.ix[row,'putlocker_url'] = proper_movie_url_minus_year(data.ix[row])
        print data.ix[row]['putlocker_url']

data2 = data[data['putlocker_url'] != 'MULTI_URL_ERROR']

data2.to_csv(path_or_buf = "/Users/ilya/metis/week2/project2/movie_list3.csv",
    encoding = 'utf-8')

