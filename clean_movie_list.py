#This script cleans up the boxofficemojo data and adds to it, to make it
#ready for scraping putlocker.

import urllib2, re
from bs4 import BeautifulSoup
import pandas as pd

data = pd.read_csv('movie_list.csv')


#***Clean up data:
#Before trying to scrape putlocker, clean up titles to make them more like
#what they look like on putlocker.

#Remove dates, (re-issue) and  (Undocumented Releases) from movie titles:
data.title = [re.sub("\((\d+)\)", '', row) for row in data.title]
data.title = [re.sub("\(re-issue\)", '', row) for row in data.title]
data.title = [re.sub("\(Undocumented Releases\)", '', row) for row in 
    data.title]

#Remove 3D movies and IMAX films from data entirely:
data = data[data['title'].str.contains('3D') == False]
data = data[data['title'].str.contains('IMAX') == False]

#Remove movie ratings that are built into titles:
ratings_regex = ["\(U.S.-only\)", "\(PG-13\)", "\(R\)", "\(G\)"]
for regular_exp in ratings_regex:
    data.title = [re.sub(regular_exp, '', row) for row in data.title]

def year_converter(date):
    """Converts year out of DD/MM/YY string to 4-digit year."""
    if date == '-':
        four_digit_year = 'DATE ERROR'
    elif int(str(date)[-2:]) < 16:
        four_digit_year = '20' + str(date)[-2:]
    elif int(str(date)[-2:]) > 20:
        four_digit_year = '19' + str(date)[-2:]
    return four_digit_year

data['year'] = [year_converter(d) for d in data.opening_date]

#Remove movies with no date:
data = data[data['year'] != 'DATE ERROR']

#Now figure out the proper putlocker URL for each movie and fill that
#into the csv file in a separate column:

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

#Fill the dataframe with proper movie urls and remove rows that have
#a MULTI_URL_ERROR:
data['putlocker_url'] = data.apply(proper_movie_url, axis = 1)
data2 = data[data['putlocker_url'] != 'MULTI_URL_ERROR']

data2.to_csv(path_or_buf = "/Users/ilya/metis/week2/project2/movie_list2.csv",
    encoding = 'utf-8')



def pull_alt_version_count(row):
    url = row['putlocker_url']
    if url == 'NO_URL_ERROR':
        return 0
    else:
        soup = soup_maker(url)
        content = soup.find('div', class=)
        tables = content.find_all('table')
        print tables
        rows = tables[3].tbody.find_all('tr')
        print rows
        print len(rows)

data['version_count'] = data[:2].apply(pull_alt_version_count, axis = 1)




