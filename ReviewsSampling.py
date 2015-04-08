# -*- coding: utf-8 -*-
"""
Created on Wed Dec 03 08:21:41 2014

@author: Baokun Wang

This script is used for extract negative and positive reviews with same quantity 
from original review file
"""
# open the file which stores reviews  
fileReader=open('Rating_Reviews.txt','r')
# the file store the sampling data
fileWriter = open('Rating_Reviews_Sampling.txt','w')

print 'counting start...'

# count the number of negative and positive words
neg_n = 0
pos_n = 0
# ignore the first line
fileReader.next()
for r in fileReader:
    rr = r.strip().split('\t')
    if len(rr) != 2:
        continue
    rating = float(rr[0])
    if rating < 3:
        neg_n = neg_n + 1
    if rating >3:
        pos_n = pos_n + 1

print 'counting finish. There are ',neg_n,' negative reviews and ',\
        pos_n,' positive reviews'


if neg_n < pos_n:
    min_n = neg_n
else:
    min_n = pos_n

print 'sampling start...'
# sampling the original reviews to ensure negative reviews : positive reviews = 1:1

#go back to the beginning of the file
fileReader.seek(0)
neg_n = 0
pos_n = 0
# ignore the first line
fileReader.next()
for r in fileReader:
    rr = r.strip().split('\t')
    if len(rr) != 2:
        continue
    rating = float(rr[0])
    review = rr[1]
    if rating < 3 and neg_n < min_n:
        neg_n = neg_n + 1
        fileWriter.write(rr[0]+'\t'+review+'\n')
    if rating >3 and pos_n < min_n:
        pos_n = pos_n + 1
        fileWriter.write(rr[0]+'\t'+review+'\n')

print 'sampling finish.'

fileReader.close()
fileWriter.close()
    