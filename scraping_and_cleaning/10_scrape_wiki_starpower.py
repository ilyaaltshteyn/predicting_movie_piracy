import pandas as pd
import urllib2
from bs4 import BeautifulSoup
data = pd.read_csv('/Users/ilya/metis/week2/project2/clean_data.csv')

#Split first 2 actor names into separate columns in data:
data['actor1'] = [str(x).split(',')[0] for x in data.actors]

def soup_maker(url):
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page)
    return soup

def url_maker(name):
    splitname = name.title().split()
    name_part = '_'.join(splitname)
    url1 = 'http://en.wikipedia.org/wiki/'
    urlfinal = url1 + name_part
    return urlfinal

data['wiki_url'] = [url_maker(x) for x in data['actor1']]

def fame_calculator(wiki_url):
    if wiki_url[-10:] == 'Pull_Error':
        return 0
    try:
        soup = soup_maker(wiki_url)
        fame = len(soup.get_text())
        return fame
    except:
        return 0

data['fame'] = 0
for index, row in data.iterrows():
    fame_ans = fame_calculator(data.ix[index]['wiki_url'])
    data.fame.ix[index] = fame_ans
    print index

data.to_csv('movie_list10.csv')

#Now get the second actor name/data in there:

#Split first 2 actor names into separate columns in data:
data['actors'] += ', PULL_ERROR'
data['actor2'] = [str(x).split(',')[1] if str(x) != 'nan' else 'PULL_ERROR' for x in data.actors]
data['actor2_wiki_url'] = [url_maker(x) for x in data['actor2']]

for index, row in data.iterrows():
    fame_ans = fame_calculator(data.ix[index]['actor2_wiki_url'])
    data.fame.ix[index] = fame_ans
    print index
