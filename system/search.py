__author__ = 'ztx'

import os
import nltk
import operator
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import numpy as np
import math

n = 4
stops = set(stopwords.words("english"))


avglen = 0
b = 0.9
k = 6


def _score(freq,verb_phrase,pos_score,phrase_tuple):
    tf = (k+1)*freq*1.0/(freq+k*(1-b+b*avglen/(len(verb_phrase))))

    pos = np.log(pos_score)*0.8

    return (tf+pos,tf,pos,' '.join(phrase_tuple))

def _pos_score(start_pos,start,end,text,phrase):
     pos_score = 0.0
     if(start == -1 or end == -1):
            if(end == -1 and start == -1 ):
                pos_score = 6*len(phrase)

            else:
                temp = start if(start != -1) else end



                for i in xrange(len(phrase)):
                    cur = start_pos + i
                    word_dist = math.fabs(temp - cur)

                    rest = temp if(cur < temp) else (len(text) - temp)
                    pos_score +=  (10.0*(word_dist))/rest

     else:
            for i in xrange(len(phrase)):
                cur = start_pos + i
                if(cur> start and cur < end):
                    pos_score += 14
                elif(cur < start):
                    word_dist = start - cur
                    pos_score += 14.0*(1-(word_dist)/(start+1))
                elif(cur > end):
                    word_dist = cur - end
                    pos_score += 14.0*(1-(word_dist)/(len(text)-end)+1)

     return pos_score

def search_function(entity1,entity2):
    file_name = "../Data/04_12/"+entity1+"_"+entity2+"_new.txt"
    file_name_next = "../Data/04_12/"+entity2+"_"+entity1+"_new.txt"

    tokenizer = RegexpTokenizer('\w+')


    key_word_dict = {}
    fd = None
    if(os.path.exists(file_name)):
        fd = open(file_name,"r")

    elif(os.path.exists(file_name_next)):
        fd = open(file_name_next,"r")
    else:
        return -1
    sum = 0.0


    for cv in fd:


        # text = nltk.word_tokenize(cv)

        text = tokenizer.tokenize(cv)

        text = [w for w in text if (not w in stopwords.words('english')) and (len(w)>1)]
        try:
            start = text.index(entity1)
        except ValueError:
            start = -1
        try:
            end = text.index(entity2)
        except ValueError:
            end = -1
        pos_map = (end,start) if start > end else (start,end)

        pos_dict = dict(nltk.pos_tag(text))
        Fgram = nltk.ngrams(text,n)
        Tgram = nltk.trigrams(text)
        # Figram = nltk.ngrams(text,n+1)
        ngram = list(Fgram)+list(Tgram)




        for phrase in ngram:

            phrase = list(phrase)
            # remove entity
            try:
                phrase.remove(entity1)
            except ValueError:
                pass
            try:
                phrase.remove(entity2)
            except ValueError:
                pass
            if(phrase != []):
                start_pos = text.index(phrase[0])

                start = pos_map[0]
                end = pos_map[1]


                pos_score = _pos_score(start_pos,start,end,text,phrase)
                phrase_tuple = tuple(phrase)




                verb_phrase = []
                for word in phrase:
                    if('V' in pos_dict[word]):
                        verb_phrase.append(word)


                if(len(verb_phrase) != 0 and verb_phrase != entity1 and verb_phrase != entity2):
                    verb_phrase = tuple(verb_phrase)

                    try:
                        obj = key_word_dict[verb_phrase]
                        obj[0] += 1
                        obj[1] += pos_score
                        if(pos_score >obj[3]):
                            obj[3] = pos_score
                            obj[2] = phrase_tuple
                    except KeyError:

                        key_word_dict[verb_phrase] = [1,pos_score,phrase_tuple,pos_score]
                        sum += len(verb_phrase)
    global avglen
    avglen = sum*1.0/len(key_word_dict.keys())
    relation_score_dict = {}
    for verb_phrase,(freq,sum_score,phrase_tuple,max_score) in key_word_dict.items():
        pos_score = sum_score*1.0/freq
        relation_score_dict[verb_phrase]=_score(freq,verb_phrase,pos_score,phrase_tuple)



    ranked_res = sorted(relation_score_dict.items(),key=operator.itemgetter(1),reverse=True)
    fd.close()

    result = []
    for i in xrange(len(ranked_res)):
        result.append((' '.join(ranked_res[i][0]), ranked_res[i][1]))
        if(i > 98):
            break

    if(len(result) == 0):
        return -1

    return result






