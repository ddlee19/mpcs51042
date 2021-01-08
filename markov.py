'''
MPCS 51042 S'20: Markov models and hash tables

YOUR NAME HERE
'''
from hash_table import Hashtable
from math import log

HASH_CELLS = 57

# Recommended load factor and growth factor for the assignment
TOO_FULL = 0.5
GROWTH_RATIO = 2

class Markov:
    
    def __init__(self, k, txt, state):
        '''
        Constructor of Markov instance. Uses hash table or dictionary as its
        internal state to represent Markov model.

        Params:
            k: value of succeeding chars to use
            txt: string of text to create the model with
            state: 0 - uses hash table class to represent model
                   1 - uses built-in dictionary to represent model
        '''

        self._k = k
        self._txt = txt
        self._state = state

        if state == 0:
            #Create 2 models, 1 for k succeeding chars and another for k+1
            self._model_k = Hashtable(HASH_CELLS, 0, TOO_FULL, GROWTH_RATIO)
            self._model_k_1 = Hashtable(HASH_CELLS, 0, TOO_FULL, GROWTH_RATIO)

        else:
            self._model_k = {}
            self._model_k_1 = {}

        for i in range(len(txt)):
            
            #Temp vars to hold succeeding chars
            k_succeeding = ''
            k_1_succeeding = ''

            #Iterate k+1 times to get k+1 succeeding chars
            for j in range(i, i+k+1):
                
                #Create copy of index j
                curr_idx = j

                #If j is greater than or equal to length of txt, wrap-around
                if curr_idx >= len(txt):
                    curr_idx = curr_idx - len(txt)

                #Append succeeding characters to temp variables
                k_1_succeeding += txt[curr_idx]

                #If at k+1, don't append for k succeeding chars
                if j < i+k:
                    k_succeeding += txt[curr_idx]

            #Insert or update table with k and k+1 succeeding chars as key
            if k_succeeding in self._model_k:
                self._model_k[k_succeeding] += 1
            else:
                self._model_k[k_succeeding] = 1

            if k_1_succeeding in self._model_k_1:
                self._model_k_1[k_1_succeeding] += 1
            else:
                self._model_k_1[k_1_succeeding] = 1

    def log_probability(self, new_txt):
        '''
        Takes new string and returns the log prob that the modeled speaker uttered it.

        Params:
            new_txt: new string
        '''

        #Sets to hold k, k+1 succeeding characters
        char_set = set()

        #Sum of log likelihood
        likelihood_sum = 0.0

        for i in range(len(new_txt)):
        
            #Temp vars to hold succeeding chars
            k_succeeding = ''
            k_1_succeeding = ''

            #Iterate k+1 times to get k+1 succeeding chars
            for j in range(i, i + self._k + 1):
                
                #Create copy of index j
                curr_idx = j

                #If j is greater than or equal to length of txt, wrap-around
                if curr_idx >= len(new_txt):
                    curr_idx = curr_idx - len(new_txt)

                #Append succeeding characters to temp variables
                k_1_succeeding += new_txt[curr_idx]

                #If at k+1, don't append for k succeeding chars
                if j < i + self._k:
                    k_succeeding += new_txt[curr_idx]

            #Only add to likelihood sum if combo of k and k+1 succeeding chars not already in char_set
            if (k_succeeding, k_1_succeeding) in char_set:
                continue

            else:

                #Add to char_set
                char_set.add(k_succeeding)
                char_set.add(k_1_succeeding)

                #Calculate log likelihood:
                m = 0
                n = 0
                s = len(set(self._txt))

                #Check if k succeeding chars are in model
                if k_succeeding in self._model_k:
                    n = self._model_k[k_succeeding]

                #Check if k+1 succeeding chars are in model
                if k_1_succeeding in self._model_k_1:
                    m = self._model_k_1[k_1_succeeding]

                likelihood_sum += log((m + 1)/(n + s))

        return likelihood_sum


def identify_speaker(speech1, speech2, speech3, order, state):
    '''
    Learns models for the speakers that uttered the first two strings. Then calculates
    the normalized log probabilities that the two speakers uttered the third string,
    and returns these two probabilities in a tuple.

    Params:
        speech1: first speech
        speech2: second speech
        speech3: speech whose speaker is unknown
        order (k): num of succeeding characters
        state: represents whether the Markov model object should use hash table or dict

    Returns:
        Tuple of two probabilities (first being the prob of the first speaker).
    '''

    #Create markov models
    model1 = Markov(order, speech1, state)
    model2 = Markov(order, speech2, state)

    #Calculate probabilities
    prob1 = model1.log_probability(speech3)/len(speech3)
    prob2 = model2.log_probability(speech3)/len(speech3)

    #Tuple to return
    return_tup = ()

    if prob1 > prob2:
        return_tup = (prob1, prob2, "A")

    else:
        return_tup = (prob1, prob2, "B")

    return return_tup