__author__ = 'ztx'

import os
import json
import os.path

start = 0

filename = "kidney_methicillin"


def indexing(corpus,index_dict,query):
    global  start;
    corpus.seek(start,0)
    while(corpus.tell() < os.fstat(corpus.fileno()).st_size):
        pid = long(corpus.readline())
        temp =  corpus.tell()
        abstract = corpus.readline()

        index_dict[pid] =temp
        if(pid == query):
            start = corpus.tell()
            return abstract

    start = corpus.tell()+1
    return ""





def search(corpus,queryfile,indexfile):
    global start

    if os.path.isfile(indexfile):
        with file(indexfile) as f:
            jsonstr = f.read()
        wrapper = json.loads(jsonstr,object_hook=lambda d: {k: {long(i):value for i,value in v.items()} if isinstance(v,dict) else v for k, v in d.items()})
        start = wrapper["start"]
        index_dict = wrapper["index_dict"]
    else:
        index_dict = {}



    corpus = open(corpus,"r")

    with file(queryfile) as f:
        querycont = f.read()
    querylst = querycont.split(" ")

    abstracts = []
    for query in querylst:
        query = long(query);
        if query in index_dict.keys():
            linenum = index_dict[query]
            corpus.seek(linenum,0)
            abstract = corpus.readline()
            abstracts.append((query,abstract))
        else:
            abstract= indexing(corpus,index_dict,query)
            if(abstract!=""):
                 abstracts.append((query,abstract))


    writefile = open("./data/index_dict/result_"+filename+".txt","w")
    for (query,abstract) in abstracts:
        writefile.write("%s\n%s"%(query,abstract))

    writefile.close()

    dict_write = open("./data/index_dict/indexing.json","w")
    wrapper = {}
    wrapper["start"] = start
    wrapper["index_dict"] = index_dict
    json.dump(wrapper,dict_write)
    dict_write.close()






class FileLineWrapper(object):
    def __init__(self, f):
        self.f = f
        self.line = 0
        self.fileno = self.f.fileno

    def close(self):
        return self.f.close()
    def seek(self,start,pos):
        return self.f.seek(start,pos)
    def readline(self):
        self.line += 1
        return self.f.readline()
    def tell(self):
        return self.f.tell()




def main():
    search("/Users/ztx/Desktop/CS499/allTitileAbs_1_to_1052","Data/index_dict/query.txt","./data/index_dict/indexing.json")


if __name__ == "__main__":
    main()