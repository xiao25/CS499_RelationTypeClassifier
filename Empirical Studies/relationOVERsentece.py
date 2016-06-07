import nltk
import operator
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords


stops = set(stopwords.words("english"))

def readData(filename):
    finput = open(filename,"r")


    abstract_list = []
    for abstract in finput:
        sentences = abstract.split(". ")
        abstract_list.append(sentences)

    finput.close()
    return abstract_list

def add2Dict(relation_dict,verb_phrases):
    for VP in verb_phrases:
        if VP in relation_dict.keys():
            relation_dict[VP] += 1
        else:
            relation_dict[VP] = 1

def write2File(relations,outfile):
    sorted_relations = sorted(relations.items(), key=operator.itemgetter(1),reverse=True)
    foutput = open(outfile,"w")
    for (rel,freq) in sorted_relations:
        foutput.write(rel+"\t"+str(freq)+"\n")

    print(len(sorted_relations))
    foutput.close()

def checkEntityInSent(entity,pointer,abstract,sent_index):
    if sent_index + pointer < len(abstract) and entity in abstract[sent_index + pointer]:
        return True
    elif sent_index - pointer >= 0 and entity in abstract[sent_index - pointer]:
        return True
    return False

def getRelation(entity1,entity2,distance,abstract_list):
    relation_dict = {}
    for abstract in abstract_list:

        for sent_index in xrange(len(abstract)):
            sentence = abstract[sent_index]
            VP = ""
            tokenizer = RegexpTokenizer('\w+')
            words = tokenizer.tokenize(sentence)
            words =[unicode(word.lower(), errors='ignore') for word in words]
            pos_dict = dict(nltk.pos_tag(words))
            verb_phrases = []
            entity1_count = False
            entity2_count = False
            for word in words:
                entity1_count = True if word == entity1 else entity1_count
                entity2_count = True if word == entity2 else entity2_count
                if word not in stops:
                    if "V"  in pos_dict[word] :
                        VP += word+" "
                    elif "NN" in pos_dict[word] and VP != '':
                        verb_phrases.append(VP)
                        VP = ''
        if entity1_count and entity2_count:
            add2Dict(relation_dict,verb_phrases)
        elif (entity2_count or entity1_count) and distance != 0:
        #check sentence before or after distance has missing entity
            for pointer in xrange(distance):
                if entity1_count and checkEntityInSent(entity2,pointer+1,abstract,sent_index):
                    add2Dict(relation_dict,verb_phrases)
                    break
                elif entity2_count and checkEntityInSent(entity1,pointer+1,abstract,sent_index):
                    add2Dict(relation_dict,verb_phrases)
                    break



    return relation_dict


# input = readData("/Users/ztx/PycharmProjects/New_CS499/Data/index_dict/result_theophylline_asthma.txt")
# relations = getRelation("theophylline","asthma",7,input)
# write2File(relations,"./output/theophylline_asthma_7.txt")


entities = [('children','ADHD'),('flu','children'),('mice','AIDS')]
dists = [0,3,5,7]
for (entity1,entity2) in entities:
    for dist in dists:
        input = readData("/Users/ztx/PycharmProjects/New_CS499/Data/index_dict/result_"+entity1+"_"+entity2+".txt")
        relations = getRelation(entity1,entity2,dist,input)
        write2File(relations,"./D-S/"+entity1+"_"+entity2+"_"+str(dist)+".txt")


