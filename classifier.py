__author__ = 'ztx'



from sklearn import svm
import numpy as np
from sklearn.decomposition import PCA
from sklearn.decomposition import SparsePCA
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import SelectFwe
from sklearn.feature_selection import chi2
from sklearn.feature_selection import SelectFdr
from sklearn.feature_selection import SelectFpr
from sklearn.pipeline import  FeatureUnion
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import pprint
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np
import random
import warnings
warnings.simplefilter("error")
# warnings.filterwarnings("ignore", 'Mean of empty slice.')
# warnings.filterwarnings("ignore", 'invalid value encountered in double_scalar')



labels_lst = ['therapy','inhibit','unknown','promote','induce']

def sepearteSentFeature(dataset,labels):
    sentences = []
    for line in dataset:
        parts = line.split("\t",1)
        index = labels_lst.index(parts[0])
        labels.append(index)
        sentences.append(parts[1])
    return sentences

def readTrain(filename):
    inputfile = open(filename,"r")

    instances = []
    for line in inputfile:
        instances.append(line)

    random.shuffle(instances)

    return instances

def featureVect(X_train,y, compoents,feature_para):

    bigram_vectorizer = CountVectorizer(ngram_range=(1,25),stop_words="english")
    X_2 = bigram_vectorizer.fit_transform(X_train).toarray()

    vectorizer = TfidfVectorizer(ngram_range=(1,25),stop_words="english")
    X_2_DFIDF=vectorizer.fit_transform(X_train).toarray()

    X = np.multiply(X_2,X_2_DFIDF)


    # This dataset is way to high-dimensional. Better do PCA:
    # pca = PCA(n_components=400)
    pca = SparsePCA(n_components=compoents[0])








    # Build estimator from PCA and Univariate selection:
    # ,("dfr",selection_fdr),("fwe",selection_fwe),("fpr",selection_fpr), ("univ_select", selection)
    feature_list = [("pca", pca)]
    feature_list += feature_para

    combined_features = FeatureUnion(feature_list)

    # Use combined features to transform dataset:
    X_features = combined_features.fit(X, y).transform(X)

    select_chi = chi2(X_2,y)

    ind = np.argpartition(select_chi[0],-compoents[1])[-compoents[1]:]
    selection_chi2 = X_2[:,ind]

    X_features = np.concatenate((X_features,selection_chi2),axis=1)



    return [X_features,combined_features,bigram_vectorizer,vectorizer,ind]

def Train(X,Y):
     # X = [[0], [1], [2], [3]]

    # clf = svm.SVC()

    clf = svm.SVC(C=0.8, cache_size=500,coef0=1,
    gamma=2, kernel='sigmoid', max_iter=-1, probability=True,
    random_state=None, shrinking=True, tol=0.001, verbose=False,class_weight = {0:2,1:2,2:1,3:10,4:10})

    # bdt = AdaBoostClassifier(clf)

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
    selection = SelectKBest(k=20)

    selection_fdr = SelectFdr(alpha = 0.05)

    selection_fwe = SelectFwe(alpha = 0.05)

    selection_fpr = SelectFpr(alpha = 0.05)


    lst = [("univ_select", selection),("dfr",selection_fdr)]
    compoents = [200,100]

    filename = "relationTrain/trainData/trainData.txt"
    instances = readTrain(filename)
    labels = []
    X = sepearteSentFeature(instances,labels)
    # ramdonly pick 1/3 as development and rest as training
    break_point = len(X)*2/3
    X_train_old = X[:break_point]
    train_labels = labels[:break_point]
    X_test_old =X[break_point:]
    test_labels = labels[break_point:]

    result = featureVect(X_train_old,train_labels,compoents,lst)

    X_train = result[0]

    classifier = Train(X_train,train_labels)

    # Test
    X_test_2 = result[2].transform(X_test_old).toarray()
    X_test_old = np.multiply(X_test_2,result[3].transform(X_test_old).toarray())
    X_test = result[1].transform(X_test_old)
    X_test = np.concatenate((X_test,X_test_2[:,result[4]]),axis=1)




    # Evaluation

    output_file = open("relationTrain/testData/predict_labels.txt","w")

    accu_matrix = np.zeros((5,5),dtype=np.int64)

    total = 0
    for i in range(len(X_test)):
        instance = X_test[i]
        predict_index = classifier.predict(instance)[0]
        predict = labels_lst[predict_index]
        output_file.write("%s\n"%predict)
        index1 = labels_lst.index(predict)
        index2 = test_labels[i]
        accu_matrix[index1][index2] += 1
        if(test_labels[i] == "unknown"):
            total += 1
    output_file.close()

    print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in accu_matrix]))

    count = long(accu_matrix[0][0]+accu_matrix[0][1]+accu_matrix[1][0]+accu_matrix[1][1])
    count += long(accu_matrix[3][3]+accu_matrix[3][4]+accu_matrix[4][3]+accu_matrix[4][4])


    print("strict accuracy:"+str(float(np.trace(accu_matrix))/(len(X_test))))
    print("Loose accuracy:"+str(float(count)/(len(X_test)-total)))


    # plot graph

    #
    # # Plot the decision boundary. For that, we will assign a color to each
    # # point in the mesh [x_min, m_max]x[y_min, y_max].
    # figure = plt.figure()
    # cm = plt.cm.RdBu
    # cm_bright = ListedColormap(['#FF0000', '#0000FF'])
    # ax = plt.subplot(1, 1 + 1, 1)
    #
    # X = np.concatenate((X_train,X_test),axis=0)
    #
    # X = X[:2]
    # h = .02  # step size in the mesh
    # #
    # #
    # x_min, x_max = X[:, 0].min() - .5, X[:, 0].max() + .5
    # y_min, y_max = X[:, 1].min() - .5, X[:, 1].max() + .5
    # xx, yy = np.meshgrid(np.arange(x_min, x_max, h),np.arange(y_min, y_max, h))
    # temp = np.c_[xx.ravel(), yy.ravel()]
    #
    # clf = svm.SVC(C=0.8, cache_size=500,coef0=1,
    # gamma=2, kernel='sigmoid', max_iter=-1, probability=True,
    # random_state=None, shrinking=True, tol=0.001, verbose=False,class_weight = {0:2,1:2,2:1,3:10,4:10})
    #
    #
    #
    # classifier= clf.fit(X, labels)
    # # if hasattr(classifier, "decision_function"):
    # #     Z = classifier.decision_function(temp)
    # # else:
    # Z = classifier.predict_proba(temp)[:, 1]
    # Z = Z.reshape(xx.shape)
    # # Put the result into a color plot
    #
    #
    # ax.contourf(xx, yy, Z, cmap=cm, alpha=.8)
    #
    # # Plot also the training points
    #
    #
    # ax.scatter(X_train[:, 0], X_train[:, 1], c=train_labels, cmap=cm_bright)
    # # and testing points
    # ax.scatter(X_test[:, 0], X_test[:, 1], c=test_labels, cmap=cm_bright,
    #            alpha=0.6)
    #
    # ax.set_xlim(xx.min(), xx.max())
    # ax.set_ylim(yy.min(), yy.max())
    # ax.set_xticks(())
    # ax.set_yticks(())
    # ax.set_title("SVM")
    # plt.show()
















if __name__ == "__main__":
    main()