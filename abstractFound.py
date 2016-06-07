__author__ = 'ztx'


import json






def search(corpus,queryfile,indexfile):
    global start

    # if os.path.isfile(indexfile):
    #     with file(indexfile) as f:
    #         jsonstr = f.read()
    #     wrapper = json.loads(jsonstr,object_hook=lambda d: {k: {long(i):value for i,value in v.items()} if isinstance(v,dict) else v for k, v in d.items()})
    #     start = wrapper["start"]
    #     index_dict = wrapper["index_dict"]
    # else:
    #     index_dict = {}

    with open(indexfile,"r") as content_file:
        index_dict = json.load(content_file)



    corpus = open(corpus,"r")

    query = open(queryfile,"r")
    for line in query:
        querylst = line.split(" ")
        break
    query.close()
    del querylst[-1]


    find_pos = []
    for pid in querylst:
        pid = str(pid);
        if pid in index_dict:
            linenum = index_dict[pid]
            find_pos.append(linenum)

    abstracts = []
    find_pos.sort()
    print(find_pos)
    #TODO change here
    writefile = open("Data/index_dict/result_mice_plague.txt","w")
    for offset in find_pos:
        corpus.seek(offset)
        abstract = corpus.readline()
        writefile.write(abstract+"\n")

    writefile.close()





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
    #TODO change here
    search("/Users/ztx/Desktop/CS499/allTitileAbs_1_to_1052","Data/pid/mice_plague.txt","./data/index_dict/index_corpus.json")


if __name__ == "__main__":
    main()