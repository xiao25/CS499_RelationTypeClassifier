__author__ = 'ztx'
import nltk


filename = "diabetes_insulin.txt"
reference = "../pid/diabetes_insulin.txt"
entity1 = 'diabetes'
entity2 = 'insulin'
output = 'diabetes_insulin_new.txt'

def findStr(term,cv,entity):

     if(term != ''):
        test = term.split(' ')
        if(test[0] == ''):
            term = term[1:]
        if(test[len(test)-1] == ''):
            term = term[:-1]
            if(len(term) != 1):
                cv = cv.replace(term,entity)


     return cv


fd = open(filename,"r")
fouput = open(output,"w")
with open(reference,"r") as fd_r:
    data = fd_r.read()
data = data.split('\n')
entity1_lst = data[1].split("|")
entity2_lst = data[2].split("|")


count = 0
for cv in fd:

    for term in entity1_lst:
        cv_new = findStr(term,cv,entity1)
        if(cv_new != cv):
            cv = cv_new
            break

    for term in entity2_lst:

        cv_new = findStr(term,cv,entity2)
        if(cv_new != cv):
            cv = cv_new
            break

    count += 1
    fouput.write("%s"%cv)

fouput.close()
fd.close()



