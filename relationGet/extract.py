__author__ = 'ztx'

import json

def createObjList(input_lst):
    list = []
    count = 0
    sum = 0
    for value in input_lst:
        new_obj = {}
        values = value.split('\t',1)

        new_obj["detail"]  = values[1]
        new_obj["name"] = values[0]
        new_obj["language"] = "relation"
        new_obj["size"] =count*5
        sum += count*5
        list.append(new_obj)
        count += 1
    return (list,sum)

def readData():
    finput = open("aspirin_headache","r")
    finput2 = open("depression_ibuprofen.txt","r")

    label_list = {}
    for line in finput:
        parts = line.split("\t",1)
        sentence = parts[1]
        label = parts[0]
        sent = "aspirin\t"+sentence
        try:

            label_list[label].append(sent)
        except KeyError:
             label_list[label] = [sent]


    for line in finput2:
        parts = line.split("\t",1)
        sentence = parts[1]
        label = parts[0]
        sent = "ibuprofen\t"+sentence
        try:

            label_list[label].append(sent)
        except KeyError:
             label_list[label] = [sent]

    return label_list



label_list = readData()

object ={}
object["name"] = "headache"
object["language"] = "disease"
object["children"] = []

temp = 0

sum = 0
for key,value in label_list.items():
    new_obj = {}
    (result,child_sum) = createObjList(value)
    new_obj["name"] = key
    new_obj["language"] = key
    new_obj["children"] = result
    new_obj["size"] = child_sum
    sum += child_sum
    object["children"].append(new_obj)

object["size"] = sum


dict_write = open("test.json","w")
json.dump(object,dict_write)
dict_write.close()