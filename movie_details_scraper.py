#This script scrapes movie details from the BOM site.

import urllib2
from bs4 import BeautifulSoup
import pandas as pd

#Note that you're working with movie_list4, which is the final version of
#the raw data.
data = pd.read_csv('movie_list4.csv')

def soup_maker(url):
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page)
    return soup

