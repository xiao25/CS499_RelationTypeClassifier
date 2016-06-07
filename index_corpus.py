


import os
import json
def indexing(input):

    index_dict = {}
    corpus = open(input,"r")
    count = 0
    offset = 0
    for line in corpus:
        if count%2 == 0:
            pid = line.split("\r\n")
            pid = long(pid[0])
        else:
            index_dict[pid] = offset
        count += 1
        offset += len(line)


    dict_write = open("./data/index_dict/index_corpus.json","w")

    json.dump(index_dict,dict_write)
    dict_write.close()




indexing("/Users/ztx/Desktop/CS499/allTitileAbs_1_to_1052")