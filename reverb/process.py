
import operator

def helper(words,po_dict,output_dict,i):
    modifer = words[i]
    if modifer in output_dict:
        output_dict[modifer] += 1
    else:
        output_dict[modifer] = 1

#TODO change here
entity_pair = ["mice","plague"]
fd = open("/Users/ztx/Desktop/output","r")



relation_dict = {}
entity_dict = {}


chunk = []
for line in fd:
    parts = line.split("\t")
    length = len(parts)
    if (entity_pair[0] in parts[2]  and entity_pair[1] in parts[4]) or (entity_pair[0] in parts[4]  and entity_pair[1] in parts[2]):
        relation = parts[3]
        if relation in relation_dict:
            action_dict = relation_dict[relation]
        else:
            relation_dict[relation] = {}
            action_dict = relation_dict[relation]


        po_dict = parts[13].split(" ")
        words = parts[12].split(" ")
        chunk.append(parts[12])
        for i in range(len(words)):
            if po_dict[i] in  ["VB", "VBD", "VBG","VBN","VBP","VBZ"]:
                action = words[i]
                if action not in relation:
                    if action in action_dict:
                        action_dict[action] += 1
                    else:
                        action_dict[action] = 1

        if relation in entity_dict:
            modifer_dict = entity_dict[relation]
        else:
            entity_dict[relation] = {}
            modifer_dict = entity_dict[relation]

        index1 = -1
        index2 = -1
        for i in xrange(len(words)):
            if entity_pair[0] in words[i]:
                index1 = i-1
            if entity_pair[1] in words[i]:
                index2 = i-1

        while po_dict[index1] == "IN" and index1>=0:
            index1 -= 1

        while po_dict[index2] == "IN" and index2>=0:
            index2 -= 1

        if index1 >= 0 and po_dict[index1] in ["JJ","JJR","JJS","NN","NNS","NNP","NNPS"]:
            helper(words,po_dict,modifer_dict,index1)
        if index2 >= 0 and po_dict[index2] in ["JJ","JJR","JJS","NN","NNS","NNP","NNPS"]:
            helper(words,po_dict,modifer_dict,index2)








fd.close()
output = open("/Users/ztx/PycharmProjects/New_CS499/Data/Action/"+entity_pair[0]+"_"+entity_pair[1]+".txt","w")
for relation in relation_dict:
    action_dict = relation_dict[relation]
    sorted_action_dict =sorted(action_dict.items(), key=operator.itemgetter(1))
    output.write(relation+"\n")

    action_str = (" # ").join(action for (action,freq) in sorted_action_dict)
    output.write(action_str+"\n\n")

for chu in chunk:
    output.write(chu+"\n")
output.close()


output = open("/Users/ztx/PycharmProjects/New_CS499/Data/Entity_Modifier/"+entity_pair[0]+"_"+entity_pair[1]+".txt","w")
for relation in entity_dict:
    modifer_dict = entity_dict[relation]
    sorted_modifer_dict =sorted(modifer_dict.items(), key=operator.itemgetter(1))
    output.write(relation+"\n")
    modifer_str = (" # ").join(modifer for (modifer,freq) in sorted_modifer_dict)
    output.write(modifer_str+"\n\n")

for chu in chunk:
    output.write(chu+"\n")
output.close()


