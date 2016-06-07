import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d


def readData(filenames,distances):

    query_list = []
    vps_list = [0,0,0,0]
    phrase_list = []
    for filename in filenames:
        phrases = []
        # (rel,feq,dist) in dist_list
        # dict[rel] = 3 means it is inside three
        dist_list = []
        # dict_rel = {}
        for i in xrange(len(distances)):
            dist = distances[i]
            finput = open('./D-C/'+filename+'_'+str(dist)+'.txt','r')
            count = 0
            for line in finput:
                parts = line.split("\t")
                (rel,feq) = (parts[0],int(parts[1]))
                dist_list.append((rel,feq,i))
                phrases.append(rel)
                # if rel in dict_rel.keys():
                #     dict_rel[rel] += 1
                # else:
                #     dict_rel[rel] = 1
                count += 1
            vps_list[i] += count
            finput.close()
        # dist_list2 = []
        # for (rel,feq,distance) in dist_list:
        #     if dict_rel[rel] == 4:
        #         dist_list2.append((rel,feq,distance))
        #         phrases.append(rel)

        phrases=list(set(phrases))
        phrase_list.append(phrases)
        query_list.append(dist_list)
    return (query_list,vps_list,phrase_list)


def plot(x,y,labels):
    label_dict = ['avg_nsc', 'wald_test']

    # Plot
    df = pd.DataFrame(dict(x=x, y=y, label=labels))
    groups = df.groupby('label')

    fig, ax = plt.subplots()


    ax.set_title("Relation between VP and Freq group by Dist")
    # ax.set_xticks(range(0,len(x),50))
    y = np.array(y)
    ax.set_ylim(0,y.max())

    marker = ['o','+','.','x']
    colors = ['#ff0080','#00FF80','#ff8000','#0080ff']
    for name, group in groups:
        f = interp1d(group.x, group.y, kind='cubic')

        xnew = np.linspace(group.x.min(), group.x.max(), num=group.x.size-1, endpoint=True)
        ax.plot(group.x, group.y, marker=marker[label_dict.index(name)], linestyle='', label=name,color=colors[label_dict.index(name)],ms=6)
        ax.plot(xnew,f(xnew),linestyle='-',label=name,color=colors[label_dict.index(name)],linewidth=2)

    ax.legend(numpoints=1)

    plt.xlabel("Rank")
    plt.ylabel("Relevant Percentage")
    plt.title("Hepatitis+Jaundice")
    plt.show()






