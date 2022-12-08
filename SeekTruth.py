# SeekTruth.py : Classify text objects into two categories
#
# PLEASE PUT YOUR NAME AND USER IDs HERE
#
# Based on skeleton code by D. Crandall, October 2021
#

import sys
import string
import re
import math
# from collections import defaultdict
from decimal import Decimal

def load_file(filename):
    objects=[]
    labels=[]
    with open(filename, "r") as f:
        for line in f:
            parsed = line.strip().split(' ',1)
            labels.append(parsed[0] if len(parsed)>0 else "")
            objects.append(parsed[1] if len(parsed)>1 else "")
    return {"objects": objects, "labels": labels, "classes": list(set(labels))}


# classifier : Train and apply a bayes net classifier
#
# This function should take a train_data dictionary that has three entries:
#        train_data["objects"] is a list of strings corresponding to reviews
#        train_data["labels"] is a list of strings corresponding to ground truth labels for each review
#        train_data["classes"] is the list of possible class names (always two)
#
# and a test_data dictionary that has objects and classes entries in the same format as above. It
# should return a list of the same length as test_data["objects"], where the i-th element of the result
# list is the estimated classlabel for test_data["objects"][i]
#
# Do not change the return type or parameters of this function!
#
# reference : https://www.youtube.com/watch?v=O2L2Uv9pdDA 

def word_probability(word, set_words,l):
    # startcount with 1 to avoid making the total probability 0 due to unappeared words
    # Adding laplace smoothing adding a hyper parameter alpha to increase the accuracy
    alpha=0.5
    count=1
    if word in set_words.keys():
        count=set_words[word]
    
    return Decimal(Decimal((count+alpha)) / Decimal(l+2*alpha))
    #2 since we have 2 classes "Deceptive" or "Truthful"

def classifier(train_data, test_data):
    T = train_data["classes"][0]
    D = train_data["classes"][1]
    # print(T,D)
    set_words = {T: {'key':0}, D: {'key':0}}
    # stopword = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
    #             'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'all', 'just', 'being',
    #             'over', 'both', 'through', 'yourselves', 'its', 'before', 'herself', 'had', 'should', 'to', 'only',
    #             'under', 'ours', 'has', 'do', 'them', 'his', 'very', 'they', 'not', 'during', 'now', 'him', 'nor',
    #             'did', 'this', 'she', 'each', 'further', 'where', 'few', 'because', 'doing', 'some', 'are', 'our',
    #             'ourselves', 'out', 'what', 'for', 'while', 'does', 'above', 'between', 'be', 'we', 'who', 'were',
    #             'here', 'hers', 'by', 'on', 'about', 'of', 'against', 'or', 'own', 'into', 'yourself', 'down', 'your',
    #             'from', 'her', 'their', 'there', 'been', 'whom', 'too', 'themselves', 'was', 'until', 'more', 'himself',
    #             'that', 'but', 'don', 'with', 'than', 'those', 'he', 'me', 'myself', 'these', 'up', 'will', 'below',
    #             'can', 'theirs', 'my', 'and', 'then', 'is', 'am', 'it', 'an', 'as', 'itself', 'at', 'have', 'in', 'any',
    #             'if', 'again', 'no', 'when', 'same', 'how', 'other', 'which', 'you', 'after', 'most', 'such', 'why',
    #             'off', 'yours', 'so', 'the', 'having', 'once', 'jobs', 'job', 'amp', 'im', '_']
    # stopword = ['a','about','above', 'after','again','against','ain','all', 'am', 'an', 'and', 'any', 'are', 'aren', "aren't",'as', 'at', 'be','because','been','before','being','below', 'between','both', 'but', 'by', 'can', 'couldn', "couldn't", 'd', 'did', 'didn', "didn't", 'do', 'does', 'doesn', "doesn't", 'doing', 'don', "don't", 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', 'hadn', "hadn't", 'has', 'hasn', "hasn't", 'have', 'haven', "haven't", 'having', 'he', 'her','here', 'hers', 'herself', 'him', 'himself', 'his', 'how', 'i', 'if', 'in', 'into', 'is','isn', "isn't", 'it', "it's", 'its', 'itself', 'just', 'll', 'm', 'ma', 'me', 'mightn', "mightn't", 'more', 'most', 'mustn', "mustn't", 'my', 'myself', 'needn', "needn't", 'no', 'nor', 'not', 'now', 'o', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 're', 's','same', 'shan', "shan't", 'she', "she's", 'should',"should've", 'shouldn', "shouldn't", 'so', 'some', 'such', 't', 'than', 'that', "that'll", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', 'these', 'they', 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 've', 'very', 'was', 'wasn', "wasn't", 'we', 'were', 'weren', "weren't", 'what', 'when', 'where', 'which', 'while', 'who', 'whom', 'why', 'will', 'with', 'won', "won't", 'wouldn', "wouldn't", 'y', 'you', "you'd", "you'll", "you're", "you've", 'your', 'yours', 'yourself','yourselves']

    Count_DEC = 0
    Count_TRU = 0

    # vocabulary = []
    # for i in range(0, len(train_data["labels"])):
    #     lines = train_data["objects"][i].lower().translate({ ord(c): None for c in "._!()-,;*&^%$#@~?/:{[}]" }).strip().split(' ')
    #     for word in lines:
    #         vocabulary.append(word)
    
    total_DEC=0
    total_TRU=0
    for i in range(0, len(train_data["labels"])):
        word_list = train_data["objects"][i].lower().translate({ ord(c): None for c in "._!()-,;*&^%$#@~?/:{[}]'`|\+*" }).strip().split(' ')
        # word_list = [word for word in
        #          [re.sub(r'[^\w\s]', r'', word) for word in train_data["objects"][i].lower().split()]
        #         if word not in stopword]
        
        if train_data["labels"][i]==T:
            for w in word_list:
                if w in set_words[T].keys():
                    set_words[T][w]+=1
                else :
                    set_words[T][w]=1
            Count_TRU+=1
            total_TRU+=len(word_list)
        elif train_data["labels"][i]==D:
            for w in word_list:
                if w in set_words[D].keys():
                    set_words[D][w]+=1
                else :
                    set_words[D][w]=1
            Count_DEC+=1
            total_DEC+=len(word_list)
            
    # print(set_words[T])
   

    probability_of_A = Decimal(Count_DEC / len(train_data["labels"]))
    probability_of_B = Decimal(Count_TRU / len(train_data["labels"]))
   
    # print(probability_of_A,probability_of_B)
    out_list = []
    
    for line in test_data["objects"]:
        curr_prob_A = probability_of_A
        curr_prob_B = probability_of_B

        for word in line.lower().translate({ ord(c): None for c in "._!()-,;*&^%$#@~?/:{[}]'`|\+*" }).strip().split(' '):
        # line_list=[word for word in
        #          [re.sub(r'[^\w\s]', r'', word) for word in train_data["objects"][i].lower().split()]]
        # for word in line_list:
            # print(word)
            curr_prob_A *= Decimal(word_probability(word, set_words[T],total_TRU))
            curr_prob_B *= Decimal(word_probability(word, set_words[D],total_DEC))
        # print(curr_prob_A,curr_prob_B)
        if curr_prob_A / curr_prob_B > 1:
            out_list.append(T)
        else:
            out_list.append(D)
    return out_list
   

    # This is just dummy code -- put yours here!
    # return [test_data["classes"][0]] * len(test_data["objects"])


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("Usage: classify.py train_file.txt test_file.txt")

    (_, train_file, test_file) = sys.argv
    # Load in the training and test datasets. The file format is simple: one object
    # per line, the first word one the line is the label.
    train_data = load_file(train_file)
    test_data = load_file(test_file)
    if(sorted(train_data["classes"]) != sorted(test_data["classes"]) or len(test_data["classes"]) != 2):
        raise Exception("Number of classes should be 2, and must be the same in test and training data")

    # make a copy of the test data without the correct labels, so the classifier can't cheat!
    test_data_sanitized = {"objects": test_data["objects"], "classes": test_data["classes"]}

    results= classifier(train_data, test_data_sanitized)

    # calculate accuracy
    correct_ct = sum([(results[i] == test_data["labels"][i]) for i in range(0, len(test_data["labels"])) ])
    print("Classification accuracy = %5.2f%%" % (100.0 * correct_ct / len(test_data["labels"])))
