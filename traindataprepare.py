__author__ = 'ztx'

import json
filename = "depression_ibuprofen.txt.json"
def main():

    with file("Data/sentimentJson/"+filename) as f:
        jsonstr = f.read()

    dict = json.loads(jsonstr)

    postive = []
    negative = []
    neutral = []
    for key,value in dict.items():
        if "Positive" in key:
            postive += value
        elif "Negative" in key:
             negative += value
        else:
            neutral += value

    output = open("relationTrain/trainData/trainData.txt","a")
    for sent in postive:
        output.write("promote\t%s"%sent)
    for sent in negative:
        output.write("induce\t%s"%sent)
    for sent in neutral:
        output.write("unknown\t%s"%sent)

    output.close()

if __name__ == "__main__":
    main()