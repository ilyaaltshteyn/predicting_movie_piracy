#This script scrapes movie details from the BOM site.

import urllib2, time, re
from bs4 import BeautifulSoup
import pandas as pd

#Note that you're working with movie_list4, which is the final version of
#the raw data.
data = pd.read_csv('movie_list4.csv')

def soup_maker(url):
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page)
    return soup

prefix = 'http://www.boxofficemojo.com'
data['link'] = [prefix + suffix for suffix in data['link']]

def movie_details_scraper(row_index):
    """Scrapes the details about a movie from that movie's BOM page.
    Try/excepts are in here to deal with denied server requests and 
    with irregular page structures."""

    link = data.ix[row_index]['link']
    try:
        soup = soup_maker(link)
    except:
        #This will update a counter that only allows the loop that this
        #function runs in to run a certain number of times before totally
        #giving up.
        global failcount
        failcount += 1
        time.sleep(5)
        return 'PULL_ERROR', 'PULL_ERROR', 'PULL_ERROR', 'PULL_ERROR'
    #Pull the centered table at the top of the page and get genre, runtime
    #and rating from it:
    centered = soup.find_all('center')[0]
    rows = centered.find_all('tr')
    try:
        genre_and_runtime = rows[2].find_all('td')
        genre = genre_and_runtime[0].contents[1].contents
        runtime = genre_and_runtime[1].contents[1].contents
        rating = rows[3].find('td').contents[1].contents
    except:
        genre = 'PULL_ERROR'
        runtime = 'PULL_ERROR'
        rating = 'PULL_ERROR'
    #Pull tables, find table that contains widest release data, pull that.
    tables = soup.find_all('table')
    try:
        release = tables[11].contents[1].contents[3].contents
    except:
        release = 'PULL_ERROR'
    return release, genre, runtime, rating

failcount = 0
data['release'] = 'UNTOUCHED'
data['genre'] = 'UNTOUCHED'
data['runtime'] = 'UNTOUCHED'
data['rating'] = 'UNTOUCHED'
for x in data.index:
    if failcount == 50:
        raise FAILCOUNT('failed to pull html 50 times')
    print 'failcount equals %r' % (failcount)
    release, genre, runtime, rating = movie_details_scraper(x)
    data.ix[x,'release'] = release
    data.ix[x,'genre'] = genre
    data.ix[x,'runtime'] = runtime
    data.ix[x,'rating'] = rating

#Clean up data a bit:
data['release_clean'] = [x[0].replace(u'\xa0', '') for x in data['release']]
data['genre_clean'] = [x[0] for x in data['genre']]
data['runtime_clean'] = [x[0] for x in data['runtime']]
data['rating_clean'] = [x[0] for x in data['rating']]

data.to_csv(path_or_buf = "movie_list5.csv", encoding = 'utf-8')




