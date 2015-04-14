#This script scrapes movie names and various characteristics about each movie
#from the boxofficemojo.com website.

import urllib2
from bs4 import BeautifulSoup

def soup_maker(url):
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page)


