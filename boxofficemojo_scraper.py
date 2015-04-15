#This script scrapes movie names and various characteristics about each movie
#from the boxofficemojo.com (BOM) website.

import urllib2
from bs4 import BeautifulSoup
import pandas as pd

def soup_maker(url):
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page)
    return soup

#Going to scrape the boxofficemojo site by sampling up to 200 movies from each
#of the top 20 studios. 


def pull_studio_table(studio_name, page):
    """Visits BOM website's page that lists all movies for a given studio. The
    page parameter is the page number for studios that have more than one page
    of movies listed. BOM lists a max of 100 movies per page. Returns the rows
    of the table that the movies on the BOM site are listed, as an iterable of
    bs4 tag objects."""

    url = 'http://www.boxofficemojo.com/studio/chart/?page=' + str(page) + \
    '&yr=&view=company&view2=allmovies&studio=' + studio_name + \
    '.htm&p=.htm'
    soup = soup_maker(url)
    body = soup.find('div', id="body")
    table = body.find_all('table')[2]
    rows = table.find_all('tr')
    # body.table
    return rows

def pull_movies_from_table(table, studio_name, studio_abbrev, page):
    """Pulls apart table into rows and puts the elements that we want from
    each row as a list. Returns a list of rows. Each row is one movie."""

    movies_on_1_page = []
    try:
        for row in table[1:101]:
            cols = row.find_all('td')
            rank = cols[0].string
            title = cols[1].string
            total_gross = cols[3].string
            opening_date = cols[7].string
            movies_on_1_page.append([title, studio_name, studio_abbrev, page,
            rank, total_gross, opening_date])
    except:
        pass
    return movies_on_1_page

#Make a dict of studio names as keys and the shortcode that BOM uses to 
#represent each studio as values:
studio_names = {'20th century fox' : 'fox', 'Buena vista' : 'buenavista',
    'Warner Bros' : 'wb-newline', 'Sony/Columbia' : 'tristar', 
    'Universal' : 'universal', 'Paramount' : 'paramount', 'Lionsgate' : 
    'lionsgatesummit', 'Weinstein Company' : 'weinsteincompany',
    'Relativity' : 'relativity', 'Open Road Films' : 'openroads',
    'Fox Searchlight' : 'foxsearchlight', 'Focus Features' : 'focus',
    'Freestyle Releasing' : 'freestyle', 'Sony Classics' : 'sonyclassics',
    'Roadside Attractions' : 'roadsideattractions', 'IFC' : 'ifc',
    'Clarius Entertainment' : 'clarius', 'UTV Communications' : 'utv',
    'CBS Films' : 'cbsfilms', 'A24' : 'a24'}

#Use the above functions to pull the movies for all the studios in the studio_names dictionary.
data = pd.DataFrame()
for studio_name, studio_abbrev in studio_names.items()[:3]:
    rows = pull_studio_table(studio_abbrev, 1)
    movies = pull_movies_from_table(rows, studio_name, studio_abbrev, 1)
    data = data.append(movies, ignore_index = True)




