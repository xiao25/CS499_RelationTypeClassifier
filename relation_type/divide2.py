import random
import os


entity_lst = []
flag = True
for filename in os.listdir("/Users/ztx/PycharmProjects/New_CS499/Data/pid"):
    fd = open("/Users/ztx/PycharmProjects/New_CS499/Data/pid/"+filename,"r")
    for line in fd:
        if flag:
            flag = False
        else:
            entity_lst += line.split("|")
    flag = True

setences = []
sent = open("DC_Corpus","r")
for line in sent:
    setences.append(line)
sent.close()

def find_sentence(x,R,y):
    global start
    while(start < len(setences)):
        count = 0
        if(x in setences[start]):
            count += 1
        if(y in setences[start]):
            count += 1
        if(R in setences[start]):
            count += 1
        if(count > 0):
            return start
        start += 1
    return -1

# x R y cof pos sentence
output = []
start = 0
fd = open("output.txt","r")
for line in fd:
    parts = line.split("\t")

    x = parts[2]
    R = parts[3]
    y = parts[4]
    sent_index = find_sentence(x,R,y)
    if sent_index == -1:
        print("error")
    if x in entity_lst or y in entity_lst:
        conf = parts[11]
        pos = parts[13]
        sentence = setences[sent_index]
        line_str = "\t".join([x,R,y,conf,pos,sentence])
        output.append(line_str)
fd.close()

list1 = []
list2 = []
i = 0
# while(i+1<len(output)):
#     list1.append(output[i])
#     list2.append(output[i+1])
#     i += 2
#
# file_write1 = open('Medicine_Disease2.txt',"w")
# for line in list2:
#     file_write1.write(line)
# file_write1.close()
#
# file_write2 = open('Medicine_Disease1.txt',"w")
# for line in list1:
#     file_write2.write(line);
# file_write2.close()

file_write2 = open('Medicine_Disease.txt',"w")
for line in output:
    file_write2.write(line);
file_write2.close()
