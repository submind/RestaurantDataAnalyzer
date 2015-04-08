# -*- coding: utf-8 -*-
"""

@author: Ryding, Baokun Wang
"""
"""
This script retrieves the urls that correspond to restaurants in New York City on tripadvisor.com
Here is an example url:
    http://www.tripadvisor.com/Restaurant_Review-g60763-d783460-Reviews-Levain_Bakery-New_York_City_New_York.html
    
On the website, restaurant are viewed in pages (30 per page). For example, 
page 1 is http://www.tripadvisor.com/Restaurants-g60763-New_York_City_New_York.html
page 2 is http://www.tripadvisor.com/Restaurants-g60763-oa30-New_York_City_New_York.html
page 3 is http://www.tripadvisor.com/Restaurants-g60763-oa60-New_York_City_New_York.html
etc.

We want to get all these link of multiple restaurants and store them in a txt.file.

Our scipct will browse page by page, and retrieve the links of the 30 restaurants in each page.
"""

# import the library we will be using in this script
import urllib2

# make a new browser
browser=urllib2.build_opener()
# add a header for browser
browser.addheaders=[('User-agent', 'Mozilla/5.0')]

# number of pages you want to retrieve
pageStart=20
pagesToGet=70

# create a new file to store restaurant links
fileWriter=open('R_Link.txt','w')

urls = ['http://www.tripadvisor.com/RestaurantSearch-g60763-oa#page#-New_York_City_New_York.html',\
        'http://www.tripadvisor.com/Restaurants-g32655-oa#page#-Los_Angeles_California.html',\
        'http://www.tripadvisor.com/Restaurants-g35805-oa#page#-Chicago_Illinois.html']
# iterate urls
for url in urls:
    print url
    # for every number in the range from 0 to pageNum+1 
    for page in range(pageStart,pagesToGet+1):
        
        print 'processing page :', page+1
        
        # make the full page url by appending the page num to the middle of the standard prefix
        # convert the number from 0 to pagesToGet to a string first.    
        url = url.replace('#page#',str(page*30))
        # use the browser to get the url.
        response=browser.open(url)    
        # read the response in html format.
        myHTML=response.read()
        # split
        segments=myHTML.split('<div class="quality easyClear">')
        
        # for all the segments except the 1st and last one
        for j in range(1,len(segments)-1): 
            
            # get the segment in the j-th position
            segment=segments[j]
            # find the position of the start and end position of restaurant link
            start_tag = '<a href="'
            index=segment.index(start_tag)+len(start_tag)
            end_tag = '" class="property_title "'
            
            # get the part (sub-string) of the segment from position 10 all the way to (but excluding) position index
            link=segment[index:segment.index(end_tag)]
            # write the link to the file, one link per line
            
            fileWriter.write('http://www.tripadvisor.com'+link+'\n')
print 'finish.'
# close the file.
fileWriter.close()


