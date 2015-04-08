# -*- coding: utf-8 -*-
"""
The script includes the following pre-processing steps for text:
- Stopword Removal
- bi-grams
- POS tagging
- lemmatizing
- Sentence Splitting
"""

import sys
import nltk.data,re
from nltk.util import ngrams
from nltk.corpus import stopwords

reload(sys)
sys.setdefaultencoding('utf8')

text=open('Rating_Reviews_Sampling.txt')

f=open('trainingData.txt','w')


#set lemmatizer and stopwords
lemmatizer=nltk.wordnet.WordNetLemmatizer()
english_stopwords=stopwords.words('english')


# tokenize the data 

n_line=0
for line in text:
    
    #set adverb,adjective,noun and verb
    advs=set()
    adjs=set()
    nouns=set()
    vbs=set()
    
    n_line=n_line+1
    print n_line
    
    # handle data and remove the html tag
    line=re.sub(r'[^\x00-\x7F]+',' ', line)
    line=re.sub('&quot;','"',line)
    line=re.sub('&#39;',"'",line)
    line=re.sub('<br/><br/>','',line)
    line=re.sub('<br/>',' ',line)
    line=re.sub(' an ',' ',line)
    line=re.sub(' a ',' ',line)
    line=re.sub(' the ',' ',line)
    line=line.lower()
    
    
    rate_text=line.split('\t')
  
    # tokenize the data
    terms = nltk.word_tokenize(rate_text[1])
    
    #do POS tagging on the tokenized data
    tagged_terms=nltk.pos_tag(terms)
    
    lemmatized=set()#holds all the distinct term roots (lemmatized words)
    for term in terms:
        term=re.sub('[^a-z]','',term) #remove non-letters
            
        if len(term)>2 and term not in english_stopwords:lemmatized.add(lemmatizer.lemmatize(term))#ignore stopwords and words withe less than 3 chars       
            
    
    for pair in tagged_terms: 
        
        #if the word is a adverb and has more than 2 letters
        if pair[1].startswith('RB') and len(pair[0])>2:
            advs.add(pair[0]) #add to the advs
        #if the word is a adjective and has more than 2 letters
        if pair[1].startswith('JJ') and len(pair[0])>2:
            adjs.add(pair[0]) #add to the adjs
        #if the word is a nouns and has more than 2 letters
        if pair[1].startswith('NN') and len(pair[0])>2:
            nouns.add(pair[0]) #add to the nouns
        #if the word is a verb and has more than 2 letters
        if pair[1].startswith('VB') and len(pair[0])>2:
            vbs.add(pair[0]) #add to the vbs

    twograms = ngrams(terms,2) #compute 2-grams
    twograms_w=[] #maintains twograms that consist of 2 nouns   
    
    for twogram in twograms: # for each 2gram
        first=twogram[0] #first term
        sec=twogram[1] #second term
        if first in english_stopwords or sec in english_stopwords:continue  # ignore if at least one of the two terms is a stopword     
            
        if len(first)<3 or len(sec)<3:continue  # ignore  if it includes very small terms       
        
        #if just first and second are adverb or adjective or noun or verb
        if first in nouns^adjs^advs^vbs and sec in nouns^adjs^advs^vbs:
            #add bi-gram words into twograms_w after lemmatizing and replace n't to not
            twograms_w.append(lemmatizer.lemmatize(first.replace("n't",'not'))+'_'+lemmatizer.lemmatize(sec.replace("n't",'not')))
    
    
    rate=float(rate_text[0])
        
    if lemmatized:
        f.write(str(rate)+'\t'+' '.join(lemmatized)+' '+' '.join(twograms_w)+'\n')
              
f.close()
text.close()           

        
