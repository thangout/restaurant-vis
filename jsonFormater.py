from bs4 import BeautifulSoup

import requests
import time
import json
import pickle

#%%

#load raw text repsonse
with open('placeData.pickle', 'rb') as f:
    place_data = pickle.load(f)

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

for i in range(0,len(place_data)):
    #loop through the downloaded pages and scrape the information
    
    place = BeautifulSoup(place_data[i],'lxml')
    
    name = next(place.find('h1','biz-page-title').children).strip() #need to encode utf-8 for saving into file
    
    #address
    address = place.find('address').findChildren('span')
    street = address[0].text
    postCode = address[1].text
    city = address[2].text
    
    #price
    priceRange = place.find('dd','price-description')
    priceText = priceRange.text.strip() #clean whitespaces
    #there is a case when the price range is just one number - no maximum there
    #therefore need to check the length
    
    if "Above" in priceText:
        priceText_split = priceText.split(' ')[1]
        currency = priceText_split[:3]
        priceFrom = priceText_split[3:]
        priceTo = 0
    elif "Under" in priceText:
        priceText_split = priceText.split(' ')[1]
        currency = priceText_split[:3]
        priceFrom = 0 
        priceTo = priceText_split[3:]
        
    else:
        currency = priceText[:3]
        priceText_split = priceText[3:].split('-') 
       
        priceFrom = priceText_split[0]
        priceTo = priceText_split[1]
    
    priceGroup = place.find('span','price-range').text
    
    #location
    coordTmp = place.find('a','biz-map-directions').findChildren()[0].attrs['src']
    coordStart = coordTmp.find('center')
    coordTmpShort = coordTmp[coordStart+7:coordStart+28]
    gps = coordTmpShort.split('%2C')
    gps = list(map(float,gps)) #convert to float
    
    #stars
    stars = float(place.find('div','rating-very-large').attrs['title'][0:3])
    
    #reviews
    numOfReviews = int(place.find('span','review-count rating-qualifier').text.strip().split(" ")[0])
    
    #web
    webTmp = place.find('span','biz-website')
    
    if not webTmp:
        web = ""
    else:
        web = webTmp.findChildren()[1].text
    
    #photos
    numOfPhotos = place.find('a','see-more show-all-overlay')
                      
    if numOfPhotos:
        numOfPhotos =  int(numOfPhotos.text.strip().split(" ")[2])
    else: 
        numOfPhotos = 0
                
    #tags
    tags = []
    
    tagsTmp = place.find('span','category-str-list').findChildren()
    
    for item in tagsTmp:
        tags.append(item.text)
    
    #extra info, like wifi, takeaway, reservation etc..
    extrasTmp = place.find('div','short-def-list').findChildren('dl')
    extras = {}
    
    for item in extrasTmp:
        itemChildren = item.findChildren()    
        key = itemChildren[0].text.strip()
        val = itemChildren[1].text.strip()
        extras[key] = val
      
    
    openHoursTpl = place.find('table','hours-table').find_all('tr')
    
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

   

#%%
    
with open('jsonPlaceData.txt', 'w') as outfile:
    json.dump(dataStorage, outfile)    