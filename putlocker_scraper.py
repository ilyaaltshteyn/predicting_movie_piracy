#This script actually scrapes the putlocker site to grab number of versions
#of each movie that are available, which will be the measure of how much
#each film is pirated.
import urllib2, re
from bs4 import BeautifulSoup
import pandas as pd

#Note that you're working with movie_list3, which is the final version of
#the raw data.
data = pd.read_csv('movie_list3.csv')

def soup_maker(url):
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page)
    return soup

def pull_alt_version_count(row):
    """Returns the number of alternative versions of the movie that are
    available for viewing on putlocker. This is a measure of how much the
    movie is pirated."""

    url = row['putlocker_url']
    if url == 'NO_URL_ERROR':
        return 0
    else:
        soup = soup_maker(url)
        content = soup.find('div', "content-box")
        tables = content.find_all('table')
        # print tables[5]
        rows = tables[5].find_all('tr')
        # print rows
        print row['Unnamed: 0']
        return len(rows)

data['version_count'] = data.apply(pull_alt_version_count, axis = 1)

data.to_csv(path_or_buf = "movie_list4.csv",
    encoding = 'utf-8')
