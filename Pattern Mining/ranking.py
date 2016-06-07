from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
import json
import nltk

st = LancasterStemmer()
text_window = 4
tokenizer = RegexpTokenizer('\w+')
stops = set(stopwords.words("english"))

Entity = ['theophylline','asthma']

def read2Data(pattern_lst):
    finput = open("pattern_nsc_DC.txt",'r')
    pattern = {}
    for line in finput:
        parts = line.split('\t')
        pattern[parts[0]] = []
        pattern_lst.append(parts[0])
    finput.close()
    return pattern

def readData(filename):
    with open(filename,'r') as file:
        json_str = file.read()

    dict = json.loads(json_str)
    return dict




def findSent(sentence,pattern):
    sentence = sentence.lower()
    # index1 = sentence.find(Entity[0].lower())
    # index2 = sentence.find(Entity[1].lower())
    #
    # if index1 != -1 and index2 != -1:
    #     start = index2  if index1 > index2 else index1
    #     end = index1+len(Entity[0]) if index1 > index2  else index2+len(Entity[1])
    #     return sentence[start:end]
    # return ""

    words = tokenizer.tokenize(sentence)
    words_new = []
    for word in words:
        try:
            word = unicode(word, 'utf-8',errors = 'ignore').lower()
            if word not in stops:
                words_new.append(word)
        except TypeError:
            print("coding error")
    pos_dict = dict(nltk.pos_tag(words_new))
    result = []
    parts = pattern.split(' ')
    cur_index = 0
    for part in parts:

        if cur_index >= len(words_new):
            break
        word = words_new[cur_index]
        if part == 'EM' and isEM(pos_dict,word):
            result.append(word)
        elif part == "VP" and isVP(pos_dict,word):
            result.append(word)
        elif part == "E" and isEntity(word):
            result.append(word)
        cur_index += 1
    if len(result) != len(parts):
        return ""
    return ' '.join(result)

def isEntity(word):
    # TODO check lower case or not
    return (word in Entity)

def isVP(pos_dict,word):
    return ('VB' in pos_dict[word])

def isEM(pos_dict,word):
    return ('JJ' in pos_dict[word] or 'NN' in pos_dict[word])



def ranking(Pattern,pattern_dict,pattern_lst,Sent_dict):
    filename = "result_"+Entity[0]+'_'+Entity[1]+'.txt'
    for pattern,sent_ids in Pattern.items():
        for sent in sent_ids:
            if filename in sent:
                parts = sent.split(".txt")
                sentid = parts[1]
                result = findSent(Sent_dict[sentid],pattern)
                if result != '':
                    pattern_dict[pattern].append(result)
                    parts = pattern.split(' ')
                    num =0
                    for part in parts:
                        if part == 'E':
                            num +=1
                    if 'VP' in pattern and num ==2:
                        print(pattern)
                        print(Sent_dict[sentid])
                        print("\n")

    foutput = open('./RankResult/'+'wald_'+filename,'w')
    for pattern in pattern_lst:
        content = '\n'.join(pattern_dict[pattern])
        foutput.write(pattern+":\n")
        foutput.write(content)
        foutput.write("\n\n")
    foutput.close()

pattern_lst = []
pattern_dict = read2Data(pattern_lst)
Sent_dict = readData('sent_dict_DC.json')
Pattern = readData('pattern_DC.json')
ranking(Pattern,pattern_dict,pattern_lst,Sent_dict)