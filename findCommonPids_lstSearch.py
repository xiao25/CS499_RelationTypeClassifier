__author__ = 'ztx'

import json

from nltk.corpus import stopwords
import gc
cachedStopWords = stopwords.words("english")


entity_1s = ['mice']
entity_2s = ['plague']

#TODO change here
indexfilename1 = "species2pubtator.json"
indexfilename2 = "disease2pubtator.json"



def readData(filename):
    with open('./Data/'+filename,'r') as file:
        json_str = file.read()

    dict = json.loads(json_str)
    return dict


# find all pids which contains entityname and return the set
def findPids(entityname,dict,keylists):
    keylist = []
    keylist.append(entityname)
    result = []
    for key_tuple, value in dict.items():
        if entityname in key_tuple:
            result += value
            key_tuple = str(key_tuple).replace("(","").replace(")","").replace("u","").replace("'","").replace("|","")
            keylist += key_tuple.split(",")

    keylists.append(keylist)
    return result



def writeToFile(pid_intersect,keySet1,keySet2,i):

    if(len(pid_intersect)>0):
        f = open('Data/pid/'+entity_1s[i]+'_'+entity_2s[i]+'.txt','w')
        for pid in pid_intersect:
            f.write(str(pid)+" ")
        f.write('\n')

        for key in keySet1:
            if key != "":
                f.write(str(key)+'|')
        f.write("\n")

        for key in keySet2:
            if key != "":
                f.write(str(key)+'|')
        f.write("\n")

        f.close()
    else:
        print('empty')

def intersection(pidList1,pidList2):
    result = []
    for term in pidList1:
        if term in pidList2 and term not in result:
            result.append(term)
    return result


def main():



    keylist1s = []
    keylist2s = []
    pidList1s = []
    pidList2s = []
    pid_dict1 = readData(indexfilename1)

    for entity_1 in entity_1s:
        pidList1 = findPids(entity_1,pid_dict1,keylist1s)
        pidList1s.append(pidList1)
    del pid_dict1
    gc.collect()

    print("finish 1")
    pid_dict2 = readData(indexfilename2)
    for entity_2 in entity_2s:
        pidList2 = findPids(entity_2,pid_dict2,keylist2s)
        pidList2s.append(pidList2)

    print("finish 2")
    del pid_dict2
    gc.collect()

    for i in range(len(pidList2s)):
        pidList1 = pidList1s[i]
        pidList2 = pidList2s[i]
        pid_intersect = intersection(pidList1,pidList2)
        writeToFile(pid_intersect,keylist1s[i],keylist2s[i],i)

if __name__ == "__main__":
    main()