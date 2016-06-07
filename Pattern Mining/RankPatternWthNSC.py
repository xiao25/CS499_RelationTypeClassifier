import numpy as np
import json
import operator


patternN = 0

def readJSONData(filename):
    with open(filename,'r') as file:
        json_str = file.read()

    dict = json.loads(json_str)
    return dict

def readTextData(filename):

    finput = open(filename,'r')
    Xs = []
    for line in finput:
        features = line.split(',')
        patternN = len(features)
        features = np.array(features).astype(np.float)
        Xs.append(features)
    finput.close()
    return Xs

Pattern = readJSONData("/Users/ztx/PycharmProjects/New_CS499/PatternMining2/pattern2.json")
Pattern = Pattern.keys()

patternN = len(Pattern)
Xs= readTextData("/Users/ztx/PycharmProjects/New_CS499/PatternMining2/Xs2.txt")


Xs = np.array(Xs)
pattern_lst = []
for col in xrange(patternN):
    sum = np.sum(Xs[:,col])
    pattern_lst.append((Pattern[col],sum))


result = sorted(pattern_lst, key = operator.itemgetter(1),reverse=True)

foutput = open("/Users/ztx/PycharmProjects/New_CS499/PatternMining2/pattern_nsc2.txt","w")
for (pattern,score) in result:
    foutput.write(pattern+'\t'+str(score)+'\n')
foutput.close()
