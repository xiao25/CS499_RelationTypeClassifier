import os
import json




finput = open("/Users/ztx/Desktop/UIUC Courses/CS499/allTitileAbs_1_to_1052",'r')

count = 1
Corpus = []
for line in finput:
    if count%2 == 0 and count %7 == 0:
        Corpus.append(line)
    count += 1

    if count > 100000:
        break

foupt = open("/Users/ztx/PycharmProjects/New_CS499/Pattern Mining/Corpus/chunk_corpus.txt","w")
for line in Corpus:
    foupt.write(line)
foupt.close()
