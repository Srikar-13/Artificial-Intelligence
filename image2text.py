#!/usr/bin/python
#
# Perform optical character recognition, usage:
#     python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png
# 
# Nithin Varadharajan : nvaradha@iu.edu
# Saiabhinav Chekka : schekka@iu.edu
# Sai Kalluri : saik@iu.edu
# (based on skeleton code by D. Crandall, Oct 2020)
#

from PIL import Image, ImageDraw, ImageFont
import sys
import math

CHARACTER_WIDTH=14
CHARACTER_HEIGHT=25

TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "


def load_letters(fname):
    im = Image.open(fname)
    px = im.load()
    (x_size, y_size) = im.size
    print(im.size)
    print(int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH)
    result = []
    for x_beg in range(0, int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH, CHARACTER_WIDTH):
        result += [ [ "".join([ '*' if px[x, y] < 1 else ' ' for x in range(x_beg, x_beg+CHARACTER_WIDTH) ]) for y in range(0, CHARACTER_HEIGHT) ], ]
    return result

def load_training_letters(fname):
    TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    letter_images = load_letters(fname)
    return { TRAIN_LETTERS[i]: letter_images[i] for i in range(0, len(TRAIN_LETTERS) ) }

#####
# main program
if len(sys.argv) != 4:
    raise Exception("Usage: python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png")

(train_img_fname, train_txt_fname, test_img_fname) = sys.argv[1:]
train_letters = load_training_letters(train_img_fname)
test_letters = load_letters(test_img_fname)

# get text data

# Read in training or test data file

exemplars = []
file = open(train_txt_fname, 'r')
for line in file:
    data = [w + ' ' for w in line.split()][::2] # will get each complete_sen with space and drop the POS tagging
    exemplars.append(data)


LOW_PROB = 1e-10 

total = 0

word_cnt = 0

prior_probs = {}
initial_probs = {}
char_cnt = {}
inital_cnt = {}

transition_cnt = {}
transition_probs = {}


for sentence in exemplars: 
    for word in sentence:

        word_cnt = word_cnt + 1

        for wchar_i in range(len(word)): 
            if word[wchar_i] in TRAIN_LETTERS:

                if wchar_i == 0:
                    if word[wchar_i] not in inital_cnt:
                        inital_cnt[word[wchar_i]] = 1
                    else:
                        inital_cnt[word[wchar_i]] += 1

                else:

                    if word[wchar_i] not in inital_cnt:
                        inital_cnt[word[wchar_i]] = LOW_PROB

    complete_sen = "".join(sentence)

    for char_i in range(len(complete_sen)): 

        if complete_sen[char_i] in TRAIN_LETTERS:

            total += 1 

            if complete_sen[char_i] not in char_cnt:
                char_cnt[complete_sen[char_i]] = 1
            else:
                char_cnt[complete_sen[char_i]] += 1


            if char_i == 0:
                pass

            else:

                if (complete_sen[char_i] in TRAIN_LETTERS and complete_sen[char_i - 1] in TRAIN_LETTERS):

                
                    if (complete_sen[char_i - 1] , complete_sen[char_i]) not in transition_cnt:
                        transition_cnt[(complete_sen[char_i - 1] , complete_sen[char_i])] = 1
                    else:
                        transition_cnt[(complete_sen[char_i - 1] , complete_sen[char_i])] += 1



# get prior probs of each char
for char_key in char_cnt:
    prior_probs[char_key] = char_cnt[char_key] / float(total)

 # get transition probs
for t_key in transition_cnt:
    transition_probs[t_key] = transition_cnt[t_key] / float(char_cnt[t_key[0]])
# set all other possible transitions to a low number
for letter1 in TRAIN_LETTERS:
    for letter2 in TRAIN_LETTERS:
        if (letter1 , letter2) not in transition_probs:
           transition_probs[(letter1 , letter2)] = LOW_PROB

 # get initial probs
for initial_key in inital_cnt:
    if (inital_cnt[initial_key] == 0): # if it was set to 0
        initial_probs[initial_key] = LOW_PROB
    else:
        initial_probs[initial_key] = inital_cnt[initial_key] / float(sum(inital_cnt.values()))  

for char_key in TRAIN_LETTERS:
    if char_key not in  initial_probs:
        initial_probs[char_key] = LOW_PROB

# get emission probs
emission_probs = {}

# first step is to get the black ratio for train and test

# loop through and get probs
for test_letter_to_test_i in range(len(test_letters)):

    emission_probs[test_letter_to_test_i] = {}

    # emission_probs[test_letter_to_test_i] = {} # dict of training letter probs

    for train_letter_to_test in train_letters:

        match = 0

        no_match = 0


        for row_match_index in range(len(test_letters[test_letter_to_test_i])):
            for col_match_index in range(len(test_letters[test_letter_to_test_i][row_match_index])):


                if (train_letters[train_letter_to_test][row_match_index][col_match_index]  ==   test_letters[test_letter_to_test_i][row_match_index][col_match_index]):    # matching values
            
                        match += 1
                else:

                        no_match += 1

      
        emission_probs[test_letter_to_test_i][train_letter_to_test] = ((0.75 ** match) * (0.25 ** no_match))
   
            
# simple
try:
    result = []
    temp = {}
    for test_letter_to_test_i in range(len(test_letters)):
        for characters in TRAIN_LETTERS:


            try:
                temp[characters] = emission_probs[test_letter_to_test_i][characters] 
            except KeyError:
                temp[characters] = LOW_PROB 
        

        result.append(max(temp, key=temp.get))

    result_simple = "".join(result)
except:
    result_simple = "Error Occurred!"

# viterbi
try:
    V_table = {}
    which_table = {}

    for char_key in TRAIN_LETTERS:
        V_table[char_key] = [0] * len(test_letters)

        which_table[char_key] = [0] * len(test_letters)


    for char_key in TRAIN_LETTERS:
        V_table[char_key][0] = math.log(initial_probs[char_key]) + math.log((emission_probs.get(0, LOW_PROB)).get(char_key, LOW_PROB))


    for i in range(1, len(test_letters)):
        for char_key in TRAIN_LETTERS:
            (which_table[char_key][i], V_table[char_key][i]) =  max( [ (char_key0, V_table[char_key0][i-1] + math.log(transition_probs.get((char_key0 , char_key), LOW_PROB))) for char_key0 in TRAIN_LETTERS ], key=lambda l:l[1] ) 
            V_table[char_key][i] += math.log(emission_probs.get(i, LOW_PROB).get(char_key, LOW_PROB))



    viterbi_sequence = [""] * len(test_letters)

    temp_list = [V_table[TRAIN_LETTERS[pos_i]][len(test_letters) - 1] for pos_i in range(len(TRAIN_LETTERS)) ]
    viterbi_sequence[len(test_letters) - 1] = TRAIN_LETTERS[temp_list.index(max(temp_list))]

    for i in range(len(test_letters) - 2, -1, -1):

        viterbi_sequence[i] = which_table[viterbi_sequence[i + 1]][i + 1]


    result_viterbi = "".join(viterbi_sequence)
except:
    result_viterbi = "Error Occurred!"



# The final two lines of your output should look something like this:
print("Simple: " + result_simple)
print("   HMM: " + result_viterbi) 


