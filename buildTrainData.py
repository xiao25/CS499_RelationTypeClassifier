__author__ = 'ztx'

import codecs
import nltk.data


from nltk.corpus import stopwords
cachedStopWords = stopwords.words("english")
corpus_name = "./data/index_dict/result_flu_children.txt"
filename = "flu_children.txt"
keySet1 = set()
keySet2 = set()
pid_intersect =[]
word_list = []
entity_1 = "flu"
entity_2 = "children"
b = 0.5

def readFromFile(filename):
     global keySet1,keySet2,pid_intersect
     f = codecs.open('Data/pid/'+filename,encoding='utf-8')
     pid_intersect = f.readline().replace('\n','')
     pid_intersect=pid_intersect.split(' ')
     pid_intersect = filter(None, pid_intersect)
     keySet1 = f.readline().replace('\n','')
     keySet1 = keySet1.split('|')
     keySet1 = filter(None, keySet1)
     keySet2 = f.readline().replace('\n','')
     keySet2 = keySet2.split('|')
     keySet2 = filter(None, keySet2)


def check(sent,keySet):
    for key in keySet:
        if key in sent:
            return True
    return False

def contextVectorExtractor(keySet1,keySet2,pid_intersect):


     contextVectors = []



     f = codecs.open(corpus_name,encoding='utf-8')
     while True:
         line_pid = f.readline().replace("\n","")
         if (line_pid == ""): break;
         line_abs = f.readline()
         if(line_pid in pid_intersect):
            # remove stop words and stem each word and split into sentences
            tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
            sentences = tokenizer.tokenize(line_abs)

            for sent in sentences:

                if(check(sent,keySet1) and check(sent,keySet2)):
                    sent = sent.replace("\n","")
                    contextVectors.append(sent)



     return contextVectors


def main():

    readFromFile(filename)
    contextVectors = contextVectorExtractor(keySet1,keySet2,pid_intersect)

    fwrite = open("./Data/04_12/"+filename,"w")
    for contextVector in contextVectors:
        try:
            fwrite.write("%s\n"%contextVector)
        except UnicodeEncodeError:
            pass
    fwrite.close()


if __name__ == "__main__":
    main()