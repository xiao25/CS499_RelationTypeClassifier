import operator
import math
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d

def plot(x,y,labels):
    df = pd.DataFrame(dict(x=x, y=y, label=labels))

    groups = df.groupby('label')

    # Plot

    fig, ax = plt.subplots()




    y = np.array(y)
    ax.set_ylim(0,1)
    ax.set_xlim(0,50)
    # ax.set_autoscaley_on(False)
    marker = ['o','^']
    colors = ['#ff8000','#0080ff']
    label_dict = ['Add_QS','Without_QS']
    for name, group in groups:
        f = interp1d(group.x, group.y, kind='cubic')



        ax.plot(group.x, group.y, marker=marker[label_dict.index(name)], linestyle='--', label=name,color=colors[label_dict.index(name)],ms=10)
        # ax.plot(xnew,f(xnew),linestyle='-',label=name,color=colors[label_dict.index(name)],linewidth=2)

    ax.legend(numpoints=1)

    plt.xlabel("Top K Result")
    plt.ylabel("@NDCG")
    plt.title("Query on ADHD-Children(D-S)")
    plt.show()




def readData(filename):

    finput = open(filename,'r')
    list = []
    for line in finput:


        parts = line.split('\t')
        rate = float(parts[1].replace('\n',''))
        list.append((parts[0],rate))
    return list

def compute(xs,ys,labels,input_rate,label):
    DCG = 0.0
    Ideal = 0.0
    for i in xrange(50):

        dividen = 1 if i == 0 else math.log(i+1)

        DCG += input_rate[i][1]/dividen
        if (i+1) < rate3:
            Ideal += 3.0/dividen
        else:
            Ideal += 2.0/dividen
        if (i+1)%10 == 0 or i == 3:
            xs.append((i+1))
            ys.append(DCG/Ideal)
            labels.append(label)
    return (xs,ys,labels)

# data_list = readData('/Users/ztx/PycharmProjects/New_CS499/Empirical Studies/baseline/total')
# sorted_data = sorted_relations = sorted(data_list, key=operator.itemgetter(1),reverse=True)

input_rate = readData('/Users/ztx/PycharmProjects/New_CS499/Empirical Studies/baseline/children_ADHD_With_top50.txt')
input_without = readData('/Users/ztx/PycharmProjects/New_CS499/Empirical Studies/baseline/witou_QS.txt')
rate3 = 42
xs = []
ys = []
labels = []

(xs,ys,labels) = compute(xs,ys,labels,input_rate,'Add_QS')
(xs,ys,labels) = compute(xs,ys,labels,input_without,'Without_QS')
plot(xs,ys,labels)