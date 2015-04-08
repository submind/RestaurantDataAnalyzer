# -*- coding: utf-8 -*-
"""

@author: Ryding, Baokun Wang
"""
"""
This script reads the file that was created by GetReviewPageLink.py line-by-line.
Each line contains the url to the review page of a a restaurant. 
The script then downloads the page for each url and stores it in a new folder.
""" 
 
# import the libraries we will be using
import urllib2

# make a new browser
browser=urllib2.build_opener()
# add a header for browser
browser.addheaders=[('User-agent', 'Mozilla/5.0')]

# open the file which stores the links of reviews  
fileReader=open('R_R_Link.txt')

# create a new file to store
fileWriter=open('Rating_Reviews.txt','w')
# get the number of current filelink
n_line=0
# only process the reviews with rating less than or equal to this threshold
threshold = 5

#for every review
for link in fileReader:    
    n_line=n_line+1
    # print current number of current filelink
    print 'page ',n_line  
    #initial values for the values we will be looking for
    rating=None
    comment=None
    #open the html file for the current review page
    try:
        # read the entire file
        HTML=browser.open(link).read()
        # split for ratings       
        ratings=HTML.split('<img class="sprite-rating_s_fill rating_s_fill s')
        # if rating is not none continue split for reviews
        if ratings:    
          # for each rating strings
          for j in range(1,len(ratings)): 
            # get rating string which includes rating and reviews
            rating_str=ratings[j]
            rating_pos = rating_str.find('"')
            rating = rating_str[0:rating_pos-1]
            # get float value of rating
            rating_f = float(rating)
            # only process ratings less than and equal to threshold
            if rating_f<=threshold:
                # get reviews
                start_tag = '<p class="partial_entry">'
                end_tag = '<span class="partnerRvw">'
                if rating_str.find(end_tag) == -1: # the whole review is in this string, just split it
                    index =rating_str.index(start_tag)+len(start_tag)
                    if rating_str[index:index+len('\n<span>')] == '\n<span>': # review is between '<p class="partial_entry">\n<span>' and '</span>'
                        start_tag = '<p class="partial_entry">\n<span>'
                        end_tag = '</span>'
                    else: # review is between '<p class="partial_entry">' and '</p>'
                        end_tag='</p>'
                    comment = rating_str[(rating_str.index(start_tag)+len(start_tag)):rating_str.index(end_tag)]
                else: # there is only partial content of review in this page, should go to another page to get all of them
                    start_tag = '<span class="partnerRvw">'
                    end_tag = '</span>'
                    # starts from the position right after '<span class="partnerRvw">'
                    l1 = rating_str.index(start_tag)+len(start_tag)
                    # get the end positon
                    l2 = rating_str.index(end_tag,l1)
                    # get string which contains new link
                    detailed_v = rating_str[l1:l2]
                    start_tag = 'review_'
                    end_tag = "'"
                    if detailed_v.find(start_tag) == -1:
                        continue
                    # get numbers from string looks like 'review_146421254' 
                    l1 = detailed_v.index(start_tag)+len(start_tag)
                    l2 = detailed_v.index(end_tag,l1)
                    number = detailed_v[l1:l2]
                    # the original link is like 'http://www.tripadvisor.com/Restaurant_Review-g60763-d1367959-Reviews-or0-Vicino_Firenze-New_York_City_New_York.html'
                    # the new link will looks like 'http://www.tripadvisor.com/ShowUserReviews-g60763-d1367959-r146421254-or0-Vicino_Firenze-New_York_City_New_York.html'                  
                    v_url = link.replace('Reviews','r'+number)
                    v_url = v_url.replace('Restaurant_Review','ShowUserReviews')
                    # get detailed information about the review
                    HTML2 = browser.open(v_url).read()
                    new_tag = '<p property="v:description" id="review_'+number+'">'
                    # split the detailed review from file
                    t = HTML2.split(new_tag)
                    tt= t[1]
                    comment = tt[0:tt.index('</p>')]
                # only record legal reviews
                if comment and (not comment.isspace()):
                    fileWriter.write(rating+'\t'+comment.replace('\n','')+'\n')
                    comment = None
                
    except:
        continue
    
    
print 'finish.'
# close the file.             
fileWriter.close()
fileReader.close()  