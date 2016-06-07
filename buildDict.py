from gensim.models import Word2Vec
from nltk.stem.porter import PorterStemmer
import nltk.data
from nltk.corpus import stopwords

def generate_dict():
    post_dict = {}
    neg_dict = {}
    cachedStopWords = stopwords.words("english")
    fd = open("/Users/ztx/PycharmProjects/New_CS499/Corpus","r")
    stemmer = PorterStemmer()
    sentences = []
    for line in fd:
        words_parts = line.split(" ")
        words = []
        pos_dict = nltk.pos_tag(words_parts)
        for i in range(len(words_parts)):
            word = words_parts[i]
            if word not in cachedStopWords and pos_dict[i][1] in ["VB", "VBD", "VBG","VBN","VBP","VBZ"]:
                words.append(stemmer.stem(word))
        if words != []:
            sentences.append(words)
    fd.close()

    model = Word2Vec(sentences,size=100, window=5, min_count=2)
    # model = Word2Vec(sentences,min_count=1)


    postive_lst = [stemmer.stem('treat'),stemmer.stem('help'),stemmer.stem('decrease')]
    negative_lst = [stemmer.stem('induce'),stemmer.stem('cause'),stemmer.stem('produce'),stemmer.stem('stimulate')]
    # (iteration,score)
    for pos in postive_lst:
        post_dict[pos] = (1,100)

    step = 2
    while(step <=10):
        word = model.most_similar(positive=postive_lst, negative= negative_lst,topn=60)
        postive_lst = []
        for (x,score) in word:
            postive_lst.append(x)
            if x not in post_dict.keys():
                post_dict[x] = (step,score*100)
        step += 1



    negative_lst= [stemmer.stem('treat'),stemmer.stem('help'),stemmer.stem('decrease')]
    postive_lst= [stemmer.stem('induce'),stemmer.stem('cause'),stemmer.stem('produce'),stemmer.stem('stimulate')]
    # (iteration,score)
    for pos in postive_lst:
        neg_dict[pos] = (1,100)

    step = 2
    while(step <=12):
        word = model.most_similar(positive=postive_lst, negative= negative_lst,topn=60)
        postive_lst = []
        for (x,score) in word:
            postive_lst.append(x)
            if x not in neg_dict.keys():
                neg_dict[x] = (step,score*100)
        step += 1

    return (post_dict,neg_dict)