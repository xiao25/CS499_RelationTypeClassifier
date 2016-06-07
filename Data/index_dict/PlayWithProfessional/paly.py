__author__ = 'ztx'

import nltk

finput = open("../result_flu_children.txt","r")
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
count = 0
for line in finput:
    if(count %2 != 0):

        sentences = tokenizer.tokenize(line)
        for sentence in sentences:
            if "test" in sentence:
                print(sentence)
    count += 1

