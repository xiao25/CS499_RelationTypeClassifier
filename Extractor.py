__author__ = 'ztx'


from textblob import Blobber
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import json
import httplib
import urllib
import urllib2


def summary(filename):


    inputfile = open('Data/04_12/'+filename,"r")


    url = "https://community-sentiment.p.mashape.com/text/"
    headers={
    "X-Mashape-Key": "mOOjL9ktiYmshzNugdDe3jyADNwDp1bGQnTjsnFsX9gTWGxm8z",
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "application/json"
    };

    newdict = {}
    for sent in inputfile:

        params=urllib.urlencode({'txt':sent})
        req = urllib2.Request(url,params,headers)
        try:
            response = urllib2.urlopen(req)
            value = response.read()
            dict = json.loads(value)
            if dict['result']['sentiment'] == "Positive":
                newkey = "_Positive"
            elif dict['result']['sentiment'] == "Negative":
                newkey = "_Negative"
            else:
                 newkey = "_Neutral"

            if newkey in newdict.keys():
                newdict[newkey].append(sent)
            else:
                newdict[newkey] = [sent]
        except urllib2.URLError as e:
                print e.reason

    file_write = open('Data/sentimentJson/'+filename+".json","w")
    json.dump(newdict,file_write,indent = 4)
    file_write.close()













def main():

    summary("kidney_methicillin.txt")



if __name__ == "__main__":
    main()