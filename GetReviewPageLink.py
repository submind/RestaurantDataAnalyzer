# -*- coding: utf-8 -*-
"""

@author: Ryding, Baokun Wang
"""
"""
This script can detect how many review pages every restaurant.
Then extract the all reviews from links in RestaurantLink.txt(get previous)
Retrieve the links of the 10 reviews in each review page.
And Store in a new txt.file.
"""
# import the two libraries we will be using in this script
import urllib2
import re
import httplib
httplib.HTTPConnection._http_vsn = 10
httplib.HTTPConnection._http_vsn_str = 'HTTP/1.0'
# make a new browser
browser=urllib2.build_opener()
# add a header for browser
browser.addheaders=[('User-agent', 'Mozilla/5.0')]

# open a existed file to read
fileReader=open('R_Link.txt','r')


# create a new file to store
fileWriter=open('R_R_Link.txt','w')

# this syntax allows us to read the file line-by-line
n_line=0
for line in fileReader:
    
    n_line=n_line+1
    print 'resaurant page',n_line
    
    try:
        # use the browser to get the link and read the html into a variable
        html=browser.open(line).read()
        # extract the information between '</span> <i>of</i>' and '<i>review'
        # this is the total number reviews of the restaurant read now
        nums=re.search(r'</span> <i>of</i> (.*?) <i>review',html)
        numstr=nums.group(1)
        # remove the comma if the number of reviews over thousand
        num=numstr.replace(',','')
        # count how many pages, beacuse 10 reviews per page.
        pages=int(float(num)/10)
        # for every number in the range from 0 to pages+1          
        for page in range(0,pages+1):
            # use '-Reviews-orXX' instead of '-Reviews' 
            reviewPages=re.compile('-Reviews')
            # convert the number from 0 to pages+1 to a string first
            newlink=reviewPages.sub(('-Reviews-or'+str(page*10)),line)
            # write the link to the file, one link per line
            fileWriter.write(newlink)
    except:
         continue
print 'finish.'
# close the files.
fileWriter.close()
fileReader.close()
