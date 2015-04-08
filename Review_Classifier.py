# -*- coding: utf-8 -*-
"""
This script can input the training data and tokenize the data will be predicted. 
Then convert a collection of text documents to a matrix of token counts
and transform a count matrix to a normalized tf or tf-idf representation
In the end, load data to support vector machines model to train and predict
"""
# import the libraries we will be using
import re
from sklearn import metrics
from nltk.util import ngrams
from sklearn.cross_validation import train_test_split
from sklearn import cross_validation
from sklearn.metrics import confusion_matrix
import nltk.data
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn import svm
from sklearn.pipeline import Pipeline
import numpy as np

#will include our points
points_train=[]
points_predict=[]

#will include our labels
labels_train=[]
labels_predict=[]


#load training data
text_train=open('trainingData.txt')

for line in text_train:
    rate_text=line.strip().split('\t') # split the tokens
    reviews=rate_text[1]

    rate=float(rate_text[0])   
    #if rate is negative
    if rate<3:
        labels_train.append(0)
        points_train.append(reviews)
    #if rate is positive
    if rate>3:
        labels_train.append(1)
        points_train.append(reviews)

text_train.close()


#open text will be predicted 
text_predict=open('test.txt')


#set lemmatizer and stopwords
lemmatizer=nltk.wordnet.WordNetLemmatizer()
english_stopwords=stopwords.words('english')


# tokenize the data 

n_line=0
for line in text_predict:
    
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
        #if rate is negative
        if rate<3:
            labels_predict.append(0)
            points_predict.append(' '.join(lemmatized)+' '+' '.join(twograms_w))
        #if rate is positive
        if rate>3:
            labels_predict.append(1)
            points_predict.append(' '.join(lemmatized)+' '+' '.join(twograms_w))

text_predict.close()

#build the pip with countVectorizer TfidfTransformer and  svm.LinearSVC        
pipe= Pipeline([('vect', CountVectorizer()),
                      ('tfidf', TfidfTransformer()),
                      ('clf', svm.LinearSVC()),])
                      
#fit on the training data
model=pipe.fit(points_train, labels_train)

#predict the labels of  the testing data
pred=model.predict(points_predict)  

#get the accuracy
print 'predict accuracy is: ', np.mean(pred == labels_predict)              

'''
If want to get a cross validation results use scripts below
'''
    
##count the number of times each term appears in each doc
#counter = CountVectorizer()
#countVectors = counter.fit_transform(points_train)
#countVectors_predict = counter.transform(points_predict)
#
##convert the count to the TFIDF value
#tfidf_transformer = TfidfTransformer()
#tfidfVectors = tfidf_transformer.fit_transform(countVectors)
#tfidfVectors_predict = tfidf_transformer.transform(countVectors_predict)
#
##set training model as linear support vector machine
#clf = svm.LinearSVC()
#
## training the classifier
#clf.fit(tfidfVectors,labels_train)


#print '\LinearSVC results'
#print '-----------------------------------------------------'
#
##test 
#print 'cross validation test results'
#print cross_validation.cross_val_score(clf, tfidfVectors , labels_train, cv=5)
#
#X_train, X_test, y_train, y_test = train_test_split(tfidfVectors, labels_train, test_size=0.3)
#clf.fit(X_train,y_train)
#pred = clf.predict(X_test)
#print "classification accuracy on 70/30 split:", metrics.accuracy_score(y_test, pred)
## Compute confusion matrix
#cm = confusion_matrix(y_test, pred)
#print 'Confusion Matrix:\n', cm
#
#print '-----------------------------------------------------'
#print 'results for new data'
##predict the new data
##load the model
#
#pred = clf.predict(tfidfVectors_predict)
#print "classification accuracy:", metrics.accuracy_score(labels_predict, pred)
## ompute confusion matrix
#cm = confusion_matrix(labels_predict, pred)
#print 'Confusion Matrix:\n', cm

