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


def plot(query_list,vps_list,phrase_list):
    label_dict = ['dist0', 'dist3', 'dist5','dist7']
    for i in xrange(len(query_list)):
        dist_list = query_list[i]
        xsticks = phrase_list[i]

        foutput = open('./D-C/VP'+str(i)+'.txt',"w")
        for vp in xsticks:
            foutput.write(vp+'\n')
        foutput.close()

        x = []
        y = []
        labels = []

        for (rel,feq,i) in dist_list:
            x.append(xsticks.index(rel)+1)
            y.append(feq)
            labels.append(label_dict[i])

        df = pd.DataFrame(dict(x=x, y=y, label=labels))

        groups = df.groupby('label')

        # Plot

        fig, ax = plt.subplots()

        # ax.set_xticklabels(xsticks)
        ax.set_title("Relation between VP and Freq group by Dist")
        ax.set_xticks(range(0,len(xsticks),50))
        y = np.array(y)
        ax.set_ylim(0,y.max())
        # ax.set_autoscaley_on(False)
        marker = ['o','+','.','x']
        colors = ['#ff0080','#00FF80','#ff8000','#0080ff']
        for name, group in groups:
            f = interp1d(group.x, group.y, kind='cubic')

            xnew = np.linspace(group.x.min(), group.x.max(), num=group.x.size-1, endpoint=True)
            ax.plot(group.x, group.y, marker=marker[label_dict.index(name)], linestyle='', label=name,color=colors[label_dict.index(name)],ms=6)
            ax.plot(xnew,f(xnew),linestyle='-',label=name,color=colors[label_dict.index(name)],linewidth=2)

        ax.legend(numpoints=1)

        plt.xlabel("Verb Phrases")
        plt.ylabel("Frequence")
        plt.title("Dist VS Total # of VPs")
        plt.show()




    bar_width = 0.35
    index = np.arange(4)

    plt.bar(index, vps_list, bar_width,label='')
    plt.ylabel("VPs #")
    plt.xlabel("Sentence Dist")
    plt.xticks(index + bar_width, ('dist0', 'dist3', 'dist5', 'dist7'))
    plt.show()

(query_list,vps_list,phrase_list) = readData(["aminophylline_asthma","methotrexate_arthritis","theophylline_asthma"],[0,3,5,7])
plot(query_list,vps_list,phrase_list)

