import wordNetSyn
import buildDict
from sklearn import linear_model
from sklearn import svm
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import math
import nltk
import entity_type


# from pystruct.learners import OneSlackSSVM
# from pystruct.models import ChainCRF


chem_dict = entity_type.build_entity_type("chemical2pubtator","chemical")
disea_dict = entity_type.build_entity_type("disease2pubtator","disease")


pos_seed = ["heal","treatment","cure","remedy","therapy","ease","relief","alleviate",'comfort',"help"]
neg_seeds = ['induce','cause','produce','stimulate','make','generate','lead to','bring about','motivate','promote']

pos_dict = wordNetSyn.generate_dict(pos_seed)
neg_dict = wordNetSyn.generate_dict(neg_seeds)

(pos_dict_word2vec, neg_dict_word2vec) = buildDict.generate_dict()


def check_flip(sentence):
    flip_words = ["not","without","no",'neither','never','nix']
    res = 1
    for word in flip_words:
        if word in sentence:
            res *= -1
    return res

def check_distance(x,R,y,sentence):
    word_count = 0
    start_index = sentence.find(x)
    if start_index != -1:
        words = sentence[start_index:].split(' ')
        for word in words:
            if word in R:
                break
            else:
                word_count += 1*3
    start_index = sentence.find(y)
    if start_index != -1:
        words = sentence[:start_index].split(" ")
        for i in range(len(words)-1,-1,-1):
            if words[i] in R:
                break
            else:
                word_count += 1*5
    return word_count

def position_score(x,R,y,sentence):
    count1 = count2 = count3 = 0
    verb_score = 0
    gen_score = 0


    words = sentence.split(" ")
    po_dict = nltk.pos_tag(words)

    start_index = end_index = -1
    rp_start = rp_end = -1
    rps = R.split(" ")
    for i in range(len(words)):
        word = words[i]
        if word in x:
            start_index = i
        elif word in y:
            end_index = i
        elif word in rps[0]:
            rp_start = i
        elif word in rps[-1]:
            rp_end = i
    for i in range(len(words)):
        if i <=start_index:
            gen_score += 4*(start_index-i)
        elif i > end_index:
            gen_score += (end_index-i)*2
        elif word not in x and word not in y and word not in R:
            gen_score += 3*(min(abs(i-rp_start),abs(i-rp_end)))

        word = words[i]
        if po_dict[i][1] in ["VB", "VBD", "VBG","VBN","VBP","VBZ"]:
            if i < start_index or i >  end_index:
                count3 += 1
            elif word in R:
                count1 += 1
            else:
                count2 += 1

    verb_score = count2*3 + count1*5 - count3*8

    return (gen_score,verb_score)


def entity_score(x,R,y,sentence):
    words = sentence.split(" ")
    count = 0
    score = 0
    if x in disea_dict.keys() and y in chem_dict.keys():
        score = -1
    elif y in disea_dict.keys() and x in chem_dict.keys():
        score = 1
    elif x in chem_dict.keys() or y in disea_dict.keys():
        score = 0.5

    for word in words:
        if word in disea_dict.keys() or word in chem_dict.keys():
            count += 1

    return count*score



def readTrain(filename,labels,label_file):

    inputfile = open(filename,"r")
    # x R y cof pos sentence
    sentences = []
    for line in inputfile:
        parts = line.split("\t")
        sentences.append(parts)
    inputfile.close()

    inputfile = open(label_file,"r")
    for line in inputfile:
        label = line.replace("\n","")
        labels.append(float(label))

    return sentences

def featureVect(corpus):
    # feature vector includes: 1.pos/neg/unkown(word2vec) 2.score(word2vec) 3.pos/neg/unkown(wordNet) 4.distance 5.pos of R is verb or not 6.how many flip words inside
    # 7.length of p, has a range 8.word distance between R and x,y 9. two entity word distance between R 10.how many Disease/Chemical entity inside and their's distance score
    # 11.unigram model with TFIDF

    custom_X = []
    corpus_str = []
    for line in corpus:
        feature = []
        f1 = 0
        f2 = 0
        f3 = 0
        f4 = 1/14
        f5 = 0
        if(len(line) == 7):
            line.remove('')
        if(len(line) !=6):
            print(line)
        (x,R,y,cof,pos,sentence) = line
        corpus_str.append(x+R+y)
        words_R = R.split(" ")
        po_dict = nltk.pos_tag(words_R)
        for i in range(len(words_R)):
            word = words_R[i]
            if word in pos_dict_word2vec.keys():
                f1 += 1
                (step,score) = pos_dict_word2vec[word]
                f2 += 1/step * 100 + score
                if po_dict[i][1] in ["VB", "VBD", "VBG","VBN","VBP","VBZ"]:
                    f5 += 1
            elif word in neg_dict_word2vec.keys():
                f1 += -1
                (step,score) = neg_dict_word2vec[word]
                f2 -= 1/step * 100 + score
                if po_dict[i][1] in ["VB", "VBD", "VBG","VBN","VBP","VBZ"]:
                    f5 += 1
            if word in pos_dict.keys():
                f3 += 1
                f4 += 100/pos_dict[word]
                if po_dict[i][1] in ["VB", "VBD", "VBG","VBN","VBP","VBZ"]:
                    f5 += 1
            elif word in neg_dict.keys():
                f3 += -1
                f4 -= 100/neg_dict[word]
                if po_dict[i][1] in ["VB", "VBD", "VBG","VBN","VBP","VBZ"]:
                    f5 += 1


        feature =[f1,f2,f3,f4]
        feature.append(check_flip(sentence))

        if len(words_R)<2:
            feature.append(3)
        elif len(words_R) < 5:
            feature.append(2)
        else:
            feature.append(1)

        feature.append(check_distance(x,R,y,sentence))
        (score1,score2) = position_score(x,R,y,sentence)

        feature.append(score1)
        feature.append(score2)

        feature.append(entity_score(x,R,y,sentence))

        custom_X.append(feature)
    custom_X = np.asarray(custom_X)
    bigram_vectorizer = CountVectorizer(ngram_range=(1,1),stop_words="english")
    X_2 = bigram_vectorizer.fit_transform(corpus_str).toarray()

    vectorizer = TfidfVectorizer(ngram_range=(1,1),stop_words="english")
    X_2_DFIDF=vectorizer.fit_transform(corpus_str).toarray()

    X = np.multiply(X_2,X_2_DFIDF)

    X = np.append(custom_X, X, axis=1)

    return custom_X

def Train(X,Y):
     # X = [[0], [1], [2], [3]]
    # clf = MultinomialNB()
    # clf = svm.SVC()

    # clf = svm.SVC(C=1.0, cache_size=10, class_weight=None, coef0=0.5, degree=4,
    # gamma=2, kernel='sigmoid', max_iter=-1, probability=True,
    # random_state=None, shrinking=True, tol=0.001, verbose=False)
    # Y =   np.asarray(Y,dtype="float64")

    # clf = linear_model.LogisticRegression()
    clf = linear_model.LinearRegression()

    clf.fit(X,Y)
    # lin_clf = svm.LinearSVC(C=1.0, class_weight=None, dual=False, fit_intercept=True,
    # intercept_scaling=1, loss='squared_hinge', max_iter=-1,
    # multi_class='ovr', penalty='l1', random_state=None, tol=0.01,
    # verbose=0)
    # lin_clf.fit(X, Y)


    # clf.fit(X,Y)

    # model = ChainCRF()
    # ssvm = OneSlackSSVM(model=model, C=.1, inference_cache=50, tol=0.1, verbose=3)
    # ssvm.fit(X, Y)
    return clf

def main():
    filename = "Medicine_Disease_Shuffer"
    label_file = "label_Shuffer"
    labels = []
    corpus = readTrain(filename,labels,label_file)



    X = featureVect(corpus)

    X_train = X[:36]
    X_test = X[36:]

    classifier = Train(X_train,labels[:36])
    test_labels = labels[36:]
#     test

    output_file = open("predict_labels.txt","w")

    count = 0
    rough_count = 0
    recall = 0
    rough_count2 = 0
    for i in range(len(X_test)):
        instance = X_test[i]
        # print(np.count_nonzero(instance))
        predict_score= classifier.predict(instance)

        print(predict_score)
        output_file.write("%s\n"%predict_score)
        label = test_labels[i]
        predict_score = float(predict_score[0])

        if predict_score * label >= 0:
            rough_count += 1
            if math.fabs(predict_score-label) <= 0.3:
                count += 1
        if label > 0:
            recall += 1
        if predict_score>0 and label > 0:
            rough_count2 += 1
    output_file.close()
    print("Accuracy is :"+str(float(count)/len(X_test)))
    print("Rough Accuracy is :"+str(float(rough_count)/len(X_test)))
    print("Recall  is :"+str(float(rough_count2)/recall))













if __name__ == "__main__":
    main()