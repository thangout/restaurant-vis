from bs4 import BeautifulSoup

import requests
import time
import json
import pickle

#%%

#PHASE 2 download html files from links that have been scraped already

with open('placeLinksData.pickle', 'rb') as f:
    entry = pickle.load(f)
    #loading all the links 
    place_links = entry
    
#%%
 
place_pages = []

raw_place_pages = []
counter = 0

#so far scraped only first 200 hunred
for place_link in place_links[:200]:
    tmpUrl = 'www.yelp.co.uk' + place_link    
    r  = requests.get("http://" +tmpUrl) #getting subpage
    data = r.text
    #place_soup = BeautifulSoup(data,"lxml")
    #place_pages.append(place_soup)
    
    raw_place_pages.append(data)
    
    counter+=1
    print ("visiting" + str(counter))
    time.sleep(5)

#%%

with open("placeData.pickle", "wb") as text_file:
    pickle.dump(raw_place_pages, text_file)
        


#%%