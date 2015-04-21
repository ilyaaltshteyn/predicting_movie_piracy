###Metis project 2: Predicting movie piracy
**For variable descriptions and some data collection notes, please see readme.txt**

####To do next:

1. Fix opening theater count variable

2. Re-run model with categorical: film on putlocker or not.

3. Re-run model with categorical: 1/2 versions vs more than that on putlocker.

4. Predict total_gross from theater count.

1. Fix NO_URL_ERRORs (which means there is no working putlocker url with the default structure) -- DONE

2. Retrieve piracy data from putlocker.is -- DONE

3. Retrieve more info about each movie from boxofficemojo. Retrieve the following about each:
 *Genre
 *rating
 *production budget
 *director (later, pull length of wiki page)
 *writer (later, pull length of wiki page)
 *actors (later, pull length of wiki page)
 *widest release

4. Retrieve info from wikipedia:
 *director fame
 *writer fame
 *actors' fame
 *movie fame
 *movie 

5. Run descriptive and inferential stats

6. Check for why NO_URL_ERRORs happen so that you can say X% of these errors are due to the movie actually not being on putlocker.
