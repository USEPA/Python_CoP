# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 09:52:13 2017

    'Script to identify similar PubMed abstracts'
    Copyright (C) <2019>  <Risa Sayre sayre.risa@epa.gov>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
    
    This script takes as an input a list of PubMed IDs and returns a csv 
    containing a list of PMIDs, their accompanying abstracts, a consensus 
    machine learning classification as similar or dissimilar to the input 
    list, and the confidence of the consensus.
    
    Although I can't commit to fully supporting this work, please feel free to
    email me any questions and I will help if I am able. I wrote it years ago 
    when I was a more novice coder (to put it kindly), so I am also quite open 
    to suggestions for improvement. Thanks!

@author: rsayre01
"""

import collections
import random

import numpy as np

import math
from statistics import mode, mean
import pandas as pd
from Bio import Entrez, Medline

import matplotlib.pyplot as plt

import pymysql.cursors
import re

import nltk
from nltk.classify.scikitlearn import SklearnClassifier

from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from nltk.metrics.scores import precision, recall
from sklearn.neural_network import MLPClassifier

##  This script requires a list of PubMed IDs as input. I leave the 
##  identification of which column has the PMIDS to you. Here are four ways:
## From csv:
#df = pd.read_csv(my_file_location, encoding='latin-1')
## From excel:
#df = pd.read_excel(my_file_location)
## From MySQL db:
# =============================================================================
# print('Fetching active PMIDs')     
# actives_pmids = []
# 
# # =============================================================================
# # connection = pymysql.connect(host='mysql-res1.epa.gov',
# #                              user='rsayre01',
# #                              password=password,
# #                              db='sbox_rsayre01_metabolites',
# #                              cursorclass=pymysql.cursors.DictCursor)
# # 
# # try:
# #     with connection.cursor() as cursor:
# #         sql = 'SELECT DISTINCT src_pmid from transformation_total WHERE species = "human" or species = "Humans" or species = "Homo sapiens"'
# #         cursor.execute(sql)
# #         result = cursor.fetchall()
# #         for record in result:
# #             actives_pmids.append(record['src_pmid'])
# # 
# # finally:
# #     connection.close()
# # =============================================================================
## From manual entry, or as a list from one of the above, you need a lst:
#actives_pmids = ['list','of','pmids']

print('Fetching abstracts')    
Entrez.email = my_email

pmid_str = list(map(str, actives_pmids))

handle = Entrez.efetch(db="pubmed", id=pmid_str, rettype="medline", retmode="text")
records = Medline.parse(handle)

abstract_dict = {}

for record in records:     
    for x in record.keys():         
        if x == "AB":             
            abstract_dict[record['PMID']] = record['AB']       
handle.close()

actives_df = pd.DataFrame(list(abstract_dict.items()), columns=['pmid', 'abstract'])

print("Generating sample PMIDs")
pmid_ints = list(map(int,actives_df['pmid'].tolist()))
sample = random.sample(range(min(pmid_ints),max(pmid_ints)), 2*len(pmid_ints))
# check len(list(set(sample) - set(pmid_ints))) = len(set(sample))
sample = list(map(str, sample))

print("Fetching abstracts for random sample")
handle = Entrez.efetch(db="pubmed", id=sample, rettype="medline", retmode="text")
records = Medline.parse(handle)

abstract_dict = {}
for record in records:     
    for x in record.keys():         
        if x == "AB":             
            abstract_dict[record['PMID']] = record['AB']      
handle.close()

results = pd.DataFrame(list(abstract_dict.items()), columns=['pmid', 'abstract'])
sample_df = results.sample(n=len(pmid_ints))

sample_text_lst = sample_df.abstract.tolist()

print('Vectorizing abstract training data')    
useful_abstracts = list(actives_df['abstract'])
random_abstracts = list(sample_df['abstract'])
useful_tuples = [("hit", x) for x in useful_abstracts]
random_tuples = [("swing", x) for x in random_abstracts]
abstract_set = useful_abstracts + random_abstracts
classified_set = useful_tuples + random_tuples
random.shuffle(classified_set)

def find_features(document):
    words = re.findall(r'\w+', document)
    features = {}
    for w in word_features:
        features[w] = (w in words)
    return features

print('Finding informative features in curated abstracts')
all_words_in_set = []
for i in range(len(abstract_set)):
    words = re.findall(r'\w+', abstract_set[i])
    all_words_in_set.append(words)
all_words_in_set_lst = [val for sublist in all_words_in_set for val in sublist if len(val) > 3]
word_features = [x for x,y in collections.Counter(all_words_in_set_lst).most_common(int(math.sqrt(len(all_words_in_set_lst))))]
featuresets = [(find_features(abstr), category) for (category, abstr) in classified_set]

print('Training classifiers with 10-fold cross-validation')
MNB_classifier = SklearnClassifier(MultinomialNB())
BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
SGDClassifier_classifier = SklearnClassifier(SGDClassifier(loss='hinge', penalty='l2', alpha=0.0001, l1_ratio=0.15, max_iter=10, tol=None))
SVC_classifier = SklearnClassifier(SVC())
LinearSVC_classifier = SklearnClassifier(LinearSVC())
knn_classifier = SklearnClassifier(KNeighborsClassifier(3))
DTree_classifier = SklearnClassifier(DecisionTreeClassifier(max_depth=5))
RF = SklearnClassifier(RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1))
MLP = SklearnClassifier(MLPClassifier(alpha=1))
AdaBoost = SklearnClassifier(AdaBoostClassifier())
#GaussianNB = SklearnClassifier(GaussianNB())
#QDA = SklearnClassifier(QuadraticDiscriminantAnalysis())
NuSVC_classifier = SklearnClassifier(NuSVC())

classifiers = [MNB_classifier,
               BernoulliNB_classifier,
               LogisticRegression_classifier,
               SGDClassifier_classifier,
               SVC_classifier,
               LinearSVC_classifier,
               NuSVC_classifier,
               knn_classifier,
               DTree_classifier,
               RF,
               MLP,
               AdaBoost]
               
num_folds = 10

active_subset = []
inactive_subset = []
for i in range(len(featuresets)):
    if featuresets[i][1] == 'hit':
        active_subset.append(featuresets[i])
    else:
        inactive_subset.append(featuresets[i])

active_subset_size = int(len(active_subset)/num_folds)
inactive_subset_size = int(len(inactive_subset)/num_folds)
subset_size = int(len(featuresets)/num_folds)

accuracies = []
confusion_matrices = []

for c in classifiers:
    accuracy_lst = []
    precision_act_lst = []
    recall_act_lst = []
    precision_inact_lst = []
    recall_inact_lst = []
    true_positives = 0
    false_negatives = 0
    false_positives = 0
    true_negatives = 0  

    c_name = re.search(r'\((.*)\(', str(c)).group(1)
    for i in range(num_folds):
      
        # preserving inherent imbalance (in this case should be somewhat balanced)
        training_this_round = inactive_subset[:i*inactive_subset_size] + inactive_subset[(i+1)*inactive_subset_size:] + active_subset[:i*active_subset_size] + active_subset[(i+1)*active_subset_size:]
        testing_this_round = inactive_subset[i*inactive_subset_size:][:inactive_subset_size] + active_subset[i*active_subset_size:][:active_subset_size]
        # forcing 50:50 split
#            training_this_round = random.sample(inactive_subset, 15) + random.sample(active_subset, 15)
#            testing_this_round = random.sample(inactive_subset, 4) + random.sample(active_subset, 4)
        # undersampling
#        inactive_training = inactive_subset[:i*inactive_subset_size] + inactive_subset[(i+1)*inactive_subset_size:]
#        training_len = len(active_subset) - active_subset_size
#        training_this_round = random.sample(inactive_training, training_len) + active_subset[:i*active_subset_size] + active_subset[(i+1)*active_subset_size:]
#        inactive_testing = inactive_subset[i*inactive_subset_size:(i+1)*inactive_subset_size]
#        testing_this_round = random.sample(inactive_testing, active_subset_size) + active_subset[i*active_subset_size:(i+1)*active_subset_size]
        random.shuffle(training_this_round)
        random.shuffle(testing_this_round)        
        c.train(training_this_round)
        accuracy_lst.append(nltk.classify.accuracy(c, testing_this_round))
        refsets = collections.defaultdict(set)
        testsets = collections.defaultdict(set)
        for i, (feats,label) in enumerate(testing_this_round):
            refsets[label].add(i)
            observed = c.classify(feats)
            testsets[observed].add(i)
        ref = dict(list(refsets.items()))
        test = dict(list(testsets.items()))
        precision_act_lst.append(precision(refsets['hit'], testsets['hit']))
        recall_act_lst.append(recall(refsets['hit'], testsets['hit']))
        precision_inact_lst.append(precision(refsets['swing'], testsets['swing']))
        recall_inact_lst.append(recall(refsets['swing'], testsets['swing']))
        for i in range(len(testing_this_round)):
            if i in refsets['hit'] and i in testsets['hit']:
                true_positives += 1
            elif i in refsets['hit'] and i in testsets['swing']:
                false_negatives += 1
            elif i in refsets['swing'] and i in testsets['hit']:
                false_positives += 1
            else:
                true_negatives += 1
    precision_act_result = [0 if x is None else x for x in precision_act_lst]
    precision_inact_result = [0 if x is None else x for x in precision_act_lst]
    data = {'active':(true_positives,false_negatives), 'inactive':(false_positives,true_negatives)}              
    accuracies.append((c_name,
                       "10-fold Cross-validated Accuracy: " + str(round(mean(accuracy_lst),3)),
                       "Precision (active): " + str(round(mean(precision_act_result),3)),
                       "Recall (active): " + str(round(mean(recall_act_lst),3)),
                       "Precision (inactive): " + str(round(mean(precision_inact_result),3)),
                       "Recall (inactive): " + str(round(mean(recall_inact_lst),3))
                       ))
    confusion_matrices.append((c_name,pd.DataFrame(data, index=['active','inactive'])))
    
cmap=plt.cm.RdYlGn              
print("Plotting classifier accuracies")
for i in range(len(confusion_matrices)):
    fig = plt.figure()
    
    ax = fig.add_subplot(111)
    fig.subplots_adjust(top=0.85)
    df_confusion = confusion_matrices[i][1]
    ax.text(0,0,df_confusion['active']['active'],fontweight='bold',ha='center', va='center', fontsize=15) #color="green",
    ax.text(0,1,df_confusion['active']['inactive'],fontweight='bold',ha='center', va='center', fontsize=15) #color="red",
    ax.text(1,0,df_confusion['inactive']['active'],fontweight='bold',ha='center', va='center', fontsize=15) #color="green",
    ax.text(1,1,df_confusion['inactive']['inactive'],fontweight='bold',ha='center', va='center', fontsize=15) #color="red",
    ax.matshow(df_confusion, cmap=cmap)
    tick_marks = np.arange(len(df_confusion.columns))
    plt.xticks(tick_marks, df_confusion.columns)#, rotation=45)
    plt.yticks(tick_marks, df_confusion.index)
    ax.set_ylabel("Predicted")
    ax.set_xlabel("Observed")
    ax.set_title(confusion_matrices[i][0])
    plt.show()

print("Choosing best classifiers")
classifiers_gt90 = []
n_abstracts = len(classified_set)

for i in range(len(confusion_matrices)):    
    wrong = confusion_matrices[i][1]['active']['inactive'] + confusion_matrices[i][1]['inactive']['active']
    if wrong/n_abstracts < 0.1:
        classifiers_gt90.append(confusion_matrices[i][0])
                 
print("Choosing PMIDs for classification")
##  you may already have a list of PMIDs you'd like to check, in which case
##  input them as above
val_sample = random.sample(range(min(pmid_ints),max(pmid_ints)), 1000*len(pmid_ints))
# check len(list(set(sample) - set(pmid_ints))) = len(set(sample))
val_sample = list(map(str, val_sample))
# ! remove training/testing set
for item in actives_pmids:
    while item in val_sample: val_sample.remove(item)
    
for item in sample:
    while item in val_sample: val_sample.remove(item)

print("Fetching abstracts for PMIDs")    
handle = Entrez.efetch(db="pubmed", id=val_sample, rettype="medline", retmode="text")
records = Medline.parse(handle)

abstract_dict = {}

print("Fetching test abstracts")
for record in records:     
    for x in record.keys():         
        if x == "AB":             
            abstract_dict[record['PMID']] = record['AB'] 
#        if x == "MH":
#            mesh_dict[record['PMID']] = record['MH']
        #if x == "RN":             
            #rn_dict[record['PMID']] = record['RN']        
handle.close()

val_results = pd.DataFrame(list(abstract_dict.items()), columns=['pmid', 'abstract'])
val_results_text_lst = val_results.abstract.tolist()
    
print('Classifying new abstracts')
classifications = []
for i in range(len(val_results)):    
    votes = []        
    for c in classifiers_gt90:            
        features = find_features(val_results['abstract'][i])            
        vote = c.classify(features)            
        votes.append(vote)            
    try:                
        consensus = mode(votes)                
        choice_votes = votes.count(consensus)                
        conf = choice_votes / len(votes)                
        classifications.append((val_results['pmid'][i],consensus,conf))            
    except:                
        classifications.append((val_results['pmid'][i],"no consensus"))                

abstract_classified_df = pd.DataFrame(classifications, columns=['pmid','abstract_class','confidence'])
abstract_classified_df.groupby(['abstract_class']).size()  

validate_me = pd.merge(val_results, abstract_classified_df, on='pmid')
len(validate_me)
len(val_results)
validate_me.to_csv(my_file_location)        