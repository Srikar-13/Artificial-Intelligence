###################################
# CS B551 Fall 2022, Assignment #3
#
# Your names and user ids: 
# Nithin Varadharajan : nvaradha@iu.edu
# Saiabhinav Chekka : schekka@iu.edu
# Sai Kalluri : saik@iu.edu
#
# (Based on skeleton code by D. Crandall)
#


import random
import math

import numpy as np

from copy import deepcopy


# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#
class Solver:

    def __init__(self):


        self.total = 0

        self.POS_list = ['noun', 'adj', 'adv', 'adp', 'conj', 'det','num', 'pron', 'prt', 'verb', 'x', '.']

        self.LOW_PROB = 1e-10 

        self.word_cnt = {}
        self.POS_cnt = {}

        self.inital_cnt = {}
        self.emission_cnt = {}
        self.transition_cnt = {}

        self.emission_count_2 = {}
        self.emission_pair_count = {}

        self.transition_count_2 = {}
        self.transition_pair_count = {}

        self.prior_probs = {}
        self.initial_probs = {}
        self.emission_probs = {}
        self.transition_probs = {}
   
        self.transition_prob_2 = {}

        self.emission_prob_2 = {}


    # Calculate the log of the posterior probability of a given sentence
    #  with a given part-of-speech labeling. Right now just returns -999 -- fix this!
    def posterior(self, model, sentence, label):

        result = 0.0

        if model == "Simple":
            
            temp = 0
            for word_i in range(len(sentence)): # for every word index

                if (sentence[word_i] , label[word_i]) in self.emission_probs:
                    temp = self.emission_probs[(sentence[word_i] , label[word_i])] 
                else:
                    temp = self.LOW_PROB

                result += math.log(temp) + math.log(self.prior_probs[label[word_i]])


            return result
        elif model == "HMM":
            
            # 0 case
            result += math.log(self.emission_probs.get((sentence[0] , label[0]), self.LOW_PROB)) + math.log(self.prior_probs[label[0]])

            for word_i in range(1, len(sentence)): 

                temp_emission = self.emission_probs.get((sentence[word_i] , label[word_i]), self.LOW_PROB)

                temp_transition = self.transition_probs.get((label[word_i-1] , label[word_i]), self.LOW_PROB)

                result += math.log(temp_emission) + math.log(temp_transition)

            return result
        elif model == "Complex":

            for word_i in range(len(sentence)):

                if word_i == 0:
                    result += math.log(self.emission_probs.get((sentence[word_i] , label[word_i]), self.LOW_PROB))
                else:
                    result += math.log(self.emission_prob_2.get((sentence[word_i] , label[word_i-1], label[word_i]), self.LOW_PROB))

                if word_i == 0:
                    result += math.log(self.prior_probs[label[word_i]])
                elif word_i == 1:
                    result += math.log(self.transition_probs.get((label[word_i-1] , label[word_i]), self.LOW_PROB))
                else:
                    result += math.log(self.transition_prob_2[(label[word_i-2],label[word_i-1],label[word_i])])
     
            return result
        else:
            print("Unknown algo!")

    # Do the training!
    #
    def train(self, data):

        for line in data: # for every sentence
            for word_i in range(len(line[0])): # for every word index

                self.total += 1 

                # get cnts

                # update word cnt dict
                if line[0][word_i] not in self.word_cnt:
                    self.word_cnt[line[0][word_i]] = 1
                else:
                    self.word_cnt[line[0][word_i]] += 1

                # update POS cnt dict
                if line[1][word_i] not in self.POS_cnt:
                    self.POS_cnt[line[1][word_i]] = 1
                else:
                    self.POS_cnt[line[1][word_i]] += 1

                # update emission cnt dict
                if (line[0][word_i] , line[1][word_i]) not in self.emission_cnt:
                    self.emission_cnt[(line[0][word_i] , line[1][word_i])] = 1
                else:
                    self.emission_cnt[(line[0][word_i] , line[1][word_i])] += 1

            
                # check if first position
                if word_i == 0:
                    # first word so update initial cnt for POS
                    if line[1][word_i] not in self.inital_cnt:
                        self.inital_cnt[line[1][word_i]] = 1
                    else:
                        self.inital_cnt[line[1][word_i]] += 1
                else:
                    # if non-first POS is not in initial cnt set it to 0
                    if line[1][word_i] not in self.inital_cnt:
                        self.inital_cnt[line[1][word_i]] = 0

                    # only non-first POS have a transition cnt
                    if (line[1][word_i - 1] , line[1][word_i]) not in self.transition_cnt:
                        self.transition_cnt[(line[1][word_i - 1] , line[1][word_i])] = 1
                    else:
                        self.transition_cnt[(line[1][word_i - 1] , line[1][word_i])] += 1

       
                    # emission 2
                    if (line[0][word_i] ,line[1][word_i - 1],line[1][word_i]) not in self.emission_count_2:
                        self.emission_count_2[(line[0][word_i] ,line[1][word_i - 1],line[1][word_i])] = 1
                    else:
                        self.emission_count_2[(line[0][word_i] ,line[1][word_i - 1],line[1][word_i])] += 1


                    if (line[1][word_i - 1],line[1][word_i]) not in self.emission_pair_count:
                        self.emission_pair_count[(line[1][word_i - 1],line[1][word_i])] = 1
                    else:
                        self.emission_pair_count[(line[1][word_i - 1],line[1][word_i])] += 1


                # transition 2
                if word_i>=2:

                    # only non-first POS have a transition cnt
                    if (line[1][word_i - 2],line[1][word_i - 1],line[1][word_i]) not in self.transition_count_2:
                        self.transition_count_2[(line[1][word_i - 2],line[1][word_i - 1],line[1][word_i])] = 1
                    else:
                        self.transition_count_2[(line[1][word_i - 2],line[1][word_i - 1],line[1][word_i])] += 1


                    if (line[1][word_i - 2],line[1][word_i - 1]) not in self.transition_pair_count:
                        self.transition_pair_count[(line[1][word_i - 2],line[1][word_i - 1])] = 1
                    else:
                        self.transition_pair_count[(line[1][word_i - 2],line[1][word_i - 1])] += 1

                    

        # get probs

        # get prior probs of each POS
        for POS_key in self.POS_cnt:
            self.prior_probs[POS_key] = self.POS_cnt[POS_key] / float(self.total)

        # get emission probs
        for e_key in self.emission_cnt:
            self.emission_probs[e_key] = self.emission_cnt[e_key] / float(self.POS_cnt[e_key[1]])
        # set all other possible emissions to a low number
        for word_key in self.word_cnt:
            for pos_key in self.POS_cnt:
                if (word_key , pos_key) not in self.emission_probs:
                    self.emission_probs[(word_key , pos_key)] = self.LOW_PROB

        # get emission probs 2
        for e_key in self.emission_count_2:
            self.emission_prob_2[e_key] = self.emission_count_2[e_key] / float(self.emission_pair_count[(e_key[1],e_key[2])])
        # set all other possible emissions to a low number
        for word_key in self.word_cnt:
            for pos_key in self.POS_cnt:
                for pos_key7 in self.POS_cnt:
                    if (word_key , pos_key, pos_key7) not in self.emission_prob_2:
                        self.emission_prob_2[(word_key , pos_key, pos_key7)] = self.LOW_PROB

        # get transition probs
        for t_key in self.transition_cnt:
            self.transition_probs[t_key] = self.transition_cnt[t_key] / float(self.POS_cnt[t_key[0]])
        # set all other possible transitions to a low number
        for pos_key1 in self.POS_cnt:
            for pos_key2 in self.POS_cnt:
                if (pos_key1 , pos_key2) not in self.transition_probs:
                    self.transition_probs[(pos_key1 , pos_key2)] = self.LOW_PROB


        for t_key in self.transition_count_2:
            self.transition_prob_2[t_key] = self.transition_count_2[t_key] / float(self.transition_pair_count[(t_key[0],t_key[1])])
        # set all other possible transitions to a low number
        for pos_key1 in self.POS_cnt:
            for pos_key2 in self.POS_cnt:
                for pos_key3 in self.POS_cnt:
                    if (pos_key1 , pos_key2, pos_key3) not in self.transition_prob_2:
                        self.transition_prob_2[(pos_key1 , pos_key2, pos_key3)] = self.LOW_PROB

        # get initial probs
        for initial_key in self.inital_cnt:
            if (self.inital_cnt[initial_key] == 0): # if it was set to 0
                self.initial_probs[initial_key] = self.LOW_PROB
            else:
                self.initial_probs[initial_key] = self.inital_cnt[initial_key] / float(self.POS_cnt[initial_key])


    # Functions for each algorithm. Right now this just returns nouns -- fix this!
    #
    def simplified(self, sentence):
        result = []
        temp = {}
        for word in sentence:
            for POS_key in self.POS_cnt:
                if (word , POS_key) in self.emission_probs:
                    temp[POS_key] = self.emission_probs[(word , POS_key)] * self.prior_probs[POS_key]
                else:
                    temp[POS_key] = self.LOW_PROB

            result.append(max(temp, key=temp.get))

        return result

    def hmm_viterbi(self, sentence):

        V_table = {}
        which_table = {}

        for pos in self.POS_list:
            V_table[pos] = [0] * len(sentence)

            which_table[pos] = [0] * len(sentence)


        for pos in self.POS_list:
            V_table[pos][0] = self.initial_probs[pos] * self.emission_probs.get((sentence[0] , pos), self.LOW_PROB)

        
        for i in range(1, len(sentence)):
            for pos in self.POS_list:
                (which_table[pos][i], V_table[pos][i]) =  max( [ (pos0, V_table[pos0][i-1] * self.transition_probs.get((pos0 , pos), self.LOW_PROB)) for pos0 in self.POS_list ], key=lambda l:l[1] ) 
                V_table[pos][i] *= self.emission_probs.get((sentence[i] , pos), self.LOW_PROB)

        viterbi_sequence = [""] * len(sentence)

        temp_list = [V_table[self.POS_list[pos_i]][len(sentence) - 1] for pos_i in range(len(self.POS_list)) ]
        viterbi_sequence[len(sentence) - 1] = self.POS_list[temp_list.index(max(temp_list))]

        for i in range(len(sentence) - 2, -1, -1):

            viterbi_sequence[i] = which_table[viterbi_sequence[i + 1]][i + 1]

        return viterbi_sequence


    def complex_mcmc(self, sentence):

        final_seq = []
        intial_pos_seq = self.simplified(sentence)
        sample_list = []  # store samples
        num_iterations = 40
        burn_in = 8

        # Gen step
        # for each iteration
        for j in range(num_iterations):
            # start with inital from previous model
            sample_pred = deepcopy(intial_pos_seq)
            # for every word
            for i in range(len(sentence)):
        
                probs_POS = []
                # for every POS
                for POS in self.POS_list:
                    # test that POS in this word
                    sample_pred[i] = POS
                    # get post prob for that POS seq
                    probs_POS.append(math.exp(self.posterior("Complex", sentence, sample_pred)))

                if(sum(probs_POS) == 0): # if all POS probs come to 0, just set it to noun
                    sample_pred[i] = self.POS_list[0]
                else: # noramlize the probabilities and sample one POS to set tthis word to
                    sample_pred[i] = np.random.choice(self.POS_list, p= list(map(lambda x: x/float(sum(probs_POS)), probs_POS)))

      
            if(j > burn_in): # after burn in 
                sample_list.append(sample_pred)

        # output step
        for i in range(len(sentence)):

            # column trasnpose
            temp_col = [row[i] for row in sample_list]

            # mode calc
            final_seq.append(max(set(temp_col), key=temp_col.count))

        return final_seq


    # This solve() method is called by label.py, so you should keep the interface the
    #  same, but you can change the code itself. 
    # It should return a list of part-of-speech labelings of the sentence, one
    #  part of speech per word.
    #
    def solve(self, model, sentence):
        if model == "Simple":
            return self.simplified(sentence)
        elif model == "HMM":
            return self.hmm_viterbi(sentence)
        elif model == "Complex":
            return self.complex_mcmc(sentence)
        else:
            print("Unknown algo!")

