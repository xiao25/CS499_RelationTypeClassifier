import json
import os
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
import nltk

st = LancasterStemmer()
text_window = 4
tokenizer = RegexpTokenizer('\w+')
# stops = set(stopwords.words("english"))



def readData(filename):
    with open(filename,'r') as file:
        json_str = file.read()

    dict = json.loads(json_str)
    return dict

def isEntity(word):
    # TODO check lower case or not
    return word in Entity or word in chemical_dict or word in disease_dict

def EMHelper(cur_i,words,pos_dict,pattern):
    if (cur_i-1 >= 0) and isEM(pos_dict,words[cur_i-1]):
        pattern = pattern + "EM" if pattern == "" else pattern + " EM"

    pattern = pattern +  "E" if pattern == "" else pattern + " E"
    if(cur_i+1 <len(words) and isEM(pos_dict,words[cur_i+1])):
       pattern += " EM"
    return pattern

def isVP(pos_dict,word):
    return ('VB' in pos_dict[word])

def isEM(pos_dict,word):
    return ('JJ' in pos_dict[word] or 'NN' in pos_dict[word])


def add2VP(vp,sent_id):
    if vp in VP.keys():
        if sent_id not in VP[vp]:
            VP[vp].append(sent_id)
    else:
        VP[vp] = [sent_id]

def add2Entity(entity,sent_id):
    if entity in Entity_Set.keys():
        if sent_id not in Entity_Set[entity]:
            Entity_Set[entity].append(sent_id)
    else:
        Entity_Set[entity] = [sent_id]

def findNextEntity(pattern,start,pos_dict,word_new,sent_id):
#     if find another entity after cur one within text window size then put it as a pattern
    vp_seen = False
    for i in xrange(text_window):
        if (start + i) < len(word_new):
            word = word_new[start + i]

            if (isEntity(word)):
                add2Entity(word,sent_id)
                pattern = EMHelper(start+i,word_new,pos_dict,pattern)

            elif (isVP(pos_dict,word_new[start+i])):
                vp_seen = True
                add2VP(word_new[start+i],sent_id)
                pattern += " VP"


    if vp_seen:
        if pattern in Pattern.keys():
            if sent_id not in Pattern[pattern]:
                Pattern[pattern].append(sent_id)
        else:
            parts = pattern.split(' ')
            num =0
            for part in parts:
                if part == 'E':
                    num +=1
            if  num >=2:
                Pattern[pattern] = [sent_id]
                seten = ' '.join(word_new)
                print(pattern+'\n'+seten)



def readFromCorpus(corpus_path):
    sent_id_unique = 0
    sent_dict = {}
    for filename in os.listdir(corpus_path):
        print(filename)
        fd = open(corpus_path+'/'+filename,"r")
        for abstract in fd:
            sentences = abstract.split(".")
            for sent_id in xrange(len(sentences)):
                sent_id_unique_str = filename + str(sent_id_unique)
                sentence = sentences[sent_id]
                words = tokenizer.tokenize(sentence)
                words_new = [unicode(word,errors = 'ignore').lower() for word in words]
                # words_new =[unicode(word,errors = 'ignore').lower() for word in words if word not in stops]

                pos_dict = dict(nltk.pos_tag(words_new))

                for cur_i in  xrange(len(words_new)):
                    if (isEntity(words_new[cur_i])):
                        entity = words_new[cur_i]
                        add2Entity(entity,sent_id_unique_str)
                        pattern = ""
                        pattern = EMHelper(cur_i,words_new,pos_dict,pattern)
                        findNextEntity(pattern,cur_i+1,pos_dict,words_new,sent_id_unique_str)
                    if (isVP(pos_dict,words_new[cur_i])):
                        vp = words_new[cur_i]
                        add2VP(vp,sent_id_unique_str)

                sent_dict[sent_id_unique] = sentence
                sent_id_unique += 1


    return sent_dict

def write2File(filename,obj):
    output = open(filename,"w")
    json.dump(obj,output)

Entity = readData('/Users/ztx/PycharmProjects/New_CS499/Pattern Mining/EntityName.json')
chemical_dict = readData('/Users/ztx/PycharmProjects/New_CS499/Data/chemical2pubtator.json')
disease_dict = readData('/Users/ztx/PycharmProjects/New_CS499/Data/disease2pubtator.json')



Pattern = {}
VP = {}
Entity_Set = {}
sent_dict = readFromCorpus('/Users/ztx/PycharmProjects/New_CS499/Pattern Mining/Corpus')

print("finish read")

write2File("pattern_DC2.json",Pattern)
write2File("vp_DC2.json",VP)
write2File("entity_DC2.json",Entity_Set)
write2File('sent_dict_DC2.json',sent_dict)
