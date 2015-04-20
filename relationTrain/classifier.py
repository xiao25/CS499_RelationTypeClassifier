__author__ = 'ztx'
from sklearn import svm
import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.lda import LDA
from sklearn.qda import QDA


labels_lst = ['therapeutic','improve','unknown','affect','induce']

def readTrain(filename,labels):
    inputfile = open(filename,"r")

    sentences = []
    for line in inputfile:
        parts = line.split("\t",1)
        index = labels_lst.index(parts[0])
        labels.append(index)
        sentences.append(parts[1])
    return sentences

def featureVect(corpus):
    bigram_vectorizer = CountVectorizer(ngram_range=(1,10),stop_words="english")
    X_2 = bigram_vectorizer.fit_transform(corpus).toarray()

    vectorizer = TfidfVectorizer(ngram_range=(1,10),stop_words="english")
    X_2_DFIDF=vectorizer.fit_transform(corpus).toarray()

    X = np.multiply(X_2,X_2_DFIDF)

    return X

def Train(X,Y):
     # X = [[0], [1], [2], [3]]

    # clf = svm.SVC()

    clf = svm.SVC(C=1.0, cache_size=10, class_weight=None, coef0=0.5, degree=4,
    gamma=2, kernel='sigmoid', max_iter=-1, probability=True,
    random_state=None, shrinking=True, tol=0.001, verbose=False)
    clf.fit(X, Y)
    # lin_clf = svm.LinearSVC(C=1.0, class_weight=None, dual=False, fit_intercept=True,
    # intercept_scaling=1, loss='squared_hinge', max_iter=-1,
    # multi_class='ovr', penalty='l1', random_state=None, tol=0.01,
    # verbose=0)
    # lin_clf.fit(X, Y)

    # clf = GaussianNB()
    # clf.fit(X,Y)
    return clf

def main():
    filename = "./trainData/trainData.txt"
    labels = []
    sentences = readTrain(filename,labels)

    filename = "./testData/testData.txt"
    labels_test = []

    sentences_test = readTrain(filename,labels_test)
    corpus = sentences + sentences_test

    X = featureVect(corpus)

    X_train = X[:len(sentences)]
    X_test = X[len(sentences):]

    classifier = Train(X_train,labels)

#     test

    output_file = open("predict_labels.txt","w")

    count = 0
    for i in range(len(X_test)):
        instance = X_test[i]
        # print(np.count_nonzero(instance))
        predict_index = classifier.predict(instance)
        predict = labels_lst[predict_index]
        print(predict)
        output_file.write("%s\n"%predict)
        if predict_index == labels_test[i]:
            count += 1
    output_file.close()
    print("Accuracy is :"+str(float(count)/len(X_test)))













if __name__ == "__main__":
    main()