This data was collected from boxofficemojo.com, IMDB (using OMDB, an IMDB API),
and putlocker.is. 

Variable descriptions:
title               movie title
studio_name         name of studio/distributor
studio_abbrev       abbreviation of studio name that boxofficemojo.com uses
page                page number in the list of "All movies" for a given studio
rank                the rank of the movie, by total gross, for its studio
total_gross         the total amount the movie has grossed
opening_date        date movie opened in theatres
link                link to boxofficemojo.com page for the movie
year                4-digit year that the movie came out in
putlocker_url       url for the movie on the putlocker site, if it exists and
                    uses one of the standard url formats. One of the standard
                    url formats includes movie year, which can sometimes be off
                    by 1 year, so I checked to see if the movie was located at
                    the url with 1 year off as well as for the year in this 
                    data.
version_count       the number of versions of the movie that are on putlocker
genre_clean         the genres that the movie falls into. Might later separate
                    into separate columns, but might just leave it dirty.
rating_clean        the MPAA rating for the movie (R, PG-13, etc)
release_clean2      the number of theatres that the movie was released to
runtime_mins        movie length in minutes
metascore           metacritic score
imdb_rating         imdb user rating
actors              bunch of actors in the movie. Might later separate them
                    out into separate columns, but for now leaving dirty.
director            movie's director. If there are multiple, they are all in
                    this one column. Might later separate them, might not.
imdb_id             imdb id code for the movie
major_award_wins_or_noms    number of major awards the movie has won or been
                            nominated for
minor_award_wins    number of more minor awards the movie has won
minor_award_noms    number of more minor awards the movie has been nominated
                    for
votecount_clean     number of people who voted for the imdb rating.
