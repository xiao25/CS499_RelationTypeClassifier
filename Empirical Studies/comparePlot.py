import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

def getList(filename):
    lst = []
    with open(filename,'r') as finput:
        for line in finput:
            lst.append(float(line))
    return lst

def prepareData():
    xs = getList('Xs')
    y1 = getList('Y1')
    y2 = getList('Y2')

    x = []
    y = []
    labels = []
    for i in xrange(len(xs)):
        x.append(xs[i])
        y.append(y1[i])
        labels.append('RelationSearch')

    for i in xrange(len(xs)):
        x.append(xs[i])
        y.append(y2[i])
        labels.append('OPENIE')

    return (x,y,labels)

def plot(x,y,labels):
    label_dict = ['RelationSearch', 'OPENIE']


    df = pd.DataFrame(dict(x=x, y=y, label=labels))

    groups = df.groupby('label')

    # Plot

    fig, ax = plt.subplots()

    # ax.set_xticklabels(xsticks)
    ax.set_title("Relation between VP and Freq group by Dist")
    ax.set_xticks(range(0,30,5))
    y = np.array(y)
    ax.set_ylim(0,1)
    # ax.set_autoscaley_on(False)
    marker = ['o','*']
    colors = ['#ff0080','#0099CC']
    for name, group in groups:
        f = interp1d(group.x, group.y, kind='cubic')
        xnew = np.linspace(group.x.min(), group.x.max(), num=group.x.size-1, endpoint=True)
        ax.plot(group.x, group.y, marker=marker[label_dict.index(name)], linestyle='', label=name,color=colors[label_dict.index(name)],ms=8)
        # ax.plot(xnew,f(xnew),linestyle='-',label=name,color=colors[label_dict.index(name)],linewidth=2)
        xs = getList('Xs')
        ax.plot(xs,f(xs),linestyle='-',label=name,color=colors[label_dict.index(name)],linewidth=2)

    ax.legend(numpoints=1)

    plt.xlabel("Top K")
    plt.ylabel("Precision")
    plt.title("Precision@K")
    plt.show()




# (query_list,vps_list,phrase_list) = readData(["aminophylline_asthma","methotrexate_arthritis","theophylline_asthma"],[0,3,5,7])
(x,y,label) = prepareData()
plot(x,y,label)

