from bs4 import BeautifulSoup

import requests
import time
import json
import pickle

#%%

# PHASE 1 - prepare links


#first loop open the big page with url
#second loop find all links to a place 

#iterate page numbers 

MAX_PAGES = 1000

for page_number in range(0, MAX_PAGES,10):
    
    #url = "www.yelp.co.uk/search?find_\loc=Praha&start=" + str(page_number)  + "&cflt=restaurants"
    url = "www.yelp.co.uk/search?find_loc=Praha&start=" + str(page_number)
    
    #get the whole page  of places
    r  = requests.get("http://" +url)
    
    soup = BeautifulSoup(r.text,"lxml")
    
    place_links = [] #store all sublinks of places
    

    #find all links to places
    for link in soup.find_all('a','biz-name'):
        place_links.append(link['href'])  
    
    try: 
        #load the links 
        with open('placeLinksData.pickle', 'rb') as f:
            entry = pickle.load(f)
            loaded_place_links = entry
        
    except:
        print ("error first loop")
        loaded_place_links = []
    
    
    loaded_place_links.extend(place_links)
    
    #save links
    with open("placeLinksData.pickle", "wb") as text_file:
        pickle.dump(loaded_place_links, text_file)
        
    time.sleep(5)
    print ("at" + str(page_number) + ", and number of links is " + str(len(loaded_place_links)))
    
    
#%%

with open('placeLinksData.pickle', 'rb') as f:
    entry = pickle.load(f)
    loaded_place_links = entry