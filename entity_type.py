
from nltk.corpus import stopwords

def build_entity_type(filename,type):
    cachedStopWords = stopwords.words("english")
    dict = {}
    fd = open(filename,"r")
    count = True
    for line in fd:
        if(count):
            count = False
        parts = line.split("\t")
        section = parts[2].split("|")
        word = section[0].lower()
        if word not in cachedStopWords:
            dict[word] = type
    return dict


