import statsmodels.api as sm
import numpy as np
import json
import operator

# TODO why the normalized_cov_params can give me negative value?

def readJSONData(filename):
    with open(filename,'r') as file:
        json_str = file.read()

    dict = json.loads(json_str)
    return dict

def readTextData(filename,lineNum):
    finput = open(filename,'r')
    Xs = []
    for line in finput:
        if (len(Xs) < lineNum):
            features = line.split(',')
            features = np.array(features).astype(np.float)
            Xs.append(features)
        else:
            break
    finput.close()
    return Xs

def readYsData(filename):
    finput = open(filename,'r')
    score = []
    for line in finput:
        score.append(int(line))
    finput.close()
    return score

def prepareYs(score,filename):
    Ys = []
    score_i = 0
    last = ''
    finput = open(filename,"r")
    for line in finput:

        parts = line.split('\t')
        if (last != '' and last != parts[2]):
            score_i += 1
        if score_i >= len(score):
            break

        if score[score_i] == 1:
            Ys.append(0.5)
        elif score[score_i] ==2:
            Ys.append(1)
        else:
            Ys.append(0)

        last = parts[2]
    return Ys


score = readYsData('Ys_CC')
Ys = prepareYs(score,"XMeaning_CC.txt")
Pattern = readJSONData("pattern_CC.json")
Xs= readTextData("Xs_CC.txt",len(Ys))
keys = Pattern.keys()


N = len(Xs)
pattern_N = len(Xs[0])


logit = sm.Logit(Ys,Xs)
result = logit.fit(method='powell')
print result.summary()


wald_score = result.params
variance = result.normalized_cov_params
wald_lst = []
for i in xrange(pattern_N):
    # print('{} sqaure / {} = '.format(wald_score[i],variance[i][i]))
    # if variance[i][i] < 0:
    #     print(variance[i][i])
    score = (wald_score[i]*wald_score[i])/variance[i][i]
    wald_lst.append((keys[i],score))
    # print(str(wald_score[i])+'\n')

result = sorted(wald_lst, key = operator.itemgetter(1),reverse=True)

foutput = open("pattern_wald_CC.txt","w")
for (pattern,score) in result:
    foutput.write(pattern+'\t'+str(score)+'\n')
foutput.close()
