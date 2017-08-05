from bs4 import BeautifulSoup

import requests
import time
import json
import pickle

#%%
#first loop open the big page with url
#second loop find all links to a place 

#iterate page numbers 

MAX_PAGES = 50

#for page_number in range(0, MAX_PAGES,10):
    #print page_number
    
page_number = 25

#url = "www.yelp.co.uk/search?find_\loc=Praha&start=" + str(page_number)  + "&cflt=restaurants"
url = "www.yelp.co.uk/search?find_loc=Praha&start=" + str(page_number)
#get the whole page  of places
r  = requests.get("http://" +url)

data = r.text

soup = BeautifulSoup(data,"lxml")

place_links = [] #store all sublinks of places

#find all links to places
for link in soup.find_all('a','biz-name'):
    place_links.append(link['href'])




#%%

#Phase 2 start quering the pages

#storing the whole html beautiful soup objects
place_pages = []

counter = 0
for place_link in place_links:
    tmpUrl = 'www.yelp.co.uk' + place_link    
    r  = requests.get("http://" +tmpUrl) #getting subpage
    data = r.text
    place_soup = BeautifulSoup(data,"lxml")
    place_pages.append(place_soup)
    counter+=1
    print ("visiting" + str(counter))
    time.sleep(1)
    
    #%%

#algorithm that scrapes the data form the page
dataStorage = []

{'name':'',#done
 'address': '', #done
 'priceRange': '', #done
 'gps': [1,2], #done
 'priceGroup': '', #done
 'stars': '', #done
 'numOfReviews': 0, #done
 'web': '', #done
 'numOfPhotos': '',#done
 'tags': [], #done
 'extras': {}, #done 
 'openHours': { #done
        'Mon' : ['9:00','22:00'],
        'Tue' : ['Closed'],
        'Wed' : '',
        'Thu' : '',
        'Fri' : '',
        'Sat' : '',
        'Sun' : '',
    }
}

#loop through the downloaded pages and scrape the information
i = 1

name = next(place_pages[i].find('h1','biz-page-title').children).strip() #need to encode utf-8 for saving into file

#address
address = place_pages[i].find('address').findChildren('span')
street = address[0].text
postCode = address[1].text
city = address[2].text

#price
priceRange = place_pages[i].find('dd','price-description')
priceText = priceRange.text.strip() #clean whitespaces
currency = priceText[:3]
priceText_split = priceText[3:].split('-') 
priceFrom = priceText_split[0]
priceTo = priceText_split[1]

priceGroup = place_pages[i].find('span','price-range').text

#location
coordTmp = place_pages[i].find('a','biz-map-directions').findChildren()[0].attrs['src']
coordStart = coordTmp.find('center')
coordTmpShort = coordTmp[coordStart+7:coordStart+28]
gps = coordTmpShort.split('%2C')
gps = list(map(float,gps)) #convert to float

#stars
stars = float(place_pages[i].find('div','rating-very-large').attrs['title'][0:3])

#reviews
numOfReviews = int(place_pages[i].find('span','review-count rating-qualifier').text.strip().split(" ")[0])

#web
webTmp = place_pages[i].find('span','biz-website')

if not webTmp:
    web = ""
else:
    web = webTmp.findChildren()[1].text

#photos
numOfPhotos = place_pages[i].find('a','see-more show-all-overlay')
                  
if numOfPhotos:
    numOfPhotos =  int(numOfPhotos.text.strip().split(" ")[2])
else: 
    numOfPhotos = 0
            
#tags
tags = []

tagsTmp = place_pages[i].find('span','category-str-list').findChildren()

for item in tagsTmp:
    tags.append(item.text)

#extra info, like wifi, takeaway, reservation etc..
extrasTmp = place_pages[i].find('div','short-def-list').findChildren('dl')
extras = {}

for item in extrasTmp:
    itemChildren = item.findChildren()    
    key = itemChildren[0].text.strip()
    val = itemChildren[1].text.strip()
    extras[key] = val
  

openHoursTpl = place_pages[i].find('table','hours-table').find_all('tr')

openHours = {}

for item in openHoursTpl:
    openHourRow = item.findChildren()
    
    dayAbbrKey = openHourRow[0].text
    openHourRange = openHourRow[1].text.strip().split('-')
    
    if(len(openHourRange) == 1):
        openHours[dayAbbrKey] = 'Closed'
    else:
        openFr = openHourRange[0]
        openTo = openHourRange[1]
        openHours[dayAbbrKey] = [openFr,openTo]
        
storeNode = {
 'name': name,
 'address': street,
 'postCode' : postCode,
 'city': city,
 'priceFrom': int(priceFrom), 
 'priceTo': int(priceTo), 
 'gps': gps, 
 'priceGroup': priceGroup, 
 'stars': stars, 
 'numOfReviews': numOfReviews,
 'web': web, 
 'numOfPhotos': numOfPhotos,
 'tags': tags, 
 'extras': extras, 
 'openHours': openHours
}

dataStorage.append(storeNode)      
#json.dumps(storeNode)

#%%

# output = json.dumps(dataStorage[0])
import pickle
#saving into file
with open("Output.pickle", "wb") as text_file:
    pickle.dump(dataStorage, text_file)
    
#%%
with open('Output.pickle', 'rb') as f:
    entry = pickle.load(f)
    print (entry)
    
#%%

loaded_place_links = [2]

#with open('placeLinks.pickle', 'rb') as f:
#    entry = pickle.load(f)
#    loaded_place_links = entry
#    print (entry)
    
place_links = []

place_links.extend(loaded_place_links)

with open("place-links.pickle", "wb") as text_file:
    pickle.dump(place_links, text_file)
    
#%%

loaded_place_links = []

with open('./place-links.pickle', 'rb') as f:
    entry = pickle.load(f)
    loaded_place_links = entry
    print (entry)
    
#%%


favorite_color = { "lion": "yellow", "kitty": "red" }

pickle.dump( favorite_color, open( "./save.p", "wb" ) )

#%%

favorite_colors = pickle.load( open( "save.p", "rb" ) )

    