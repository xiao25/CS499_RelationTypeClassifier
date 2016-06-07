import random
import numpy
import matplotlib.pyplot as plt
# import plotly.plotly as py  # tools to communicate with Plotly's server



# histogram,ax=plt.subplots()

# x = [0]*10+[5]*16+[10]*46+[15]*14+[20]*6+[25]*6
# y = [1]*0+[6]*5+[11]*37+[16]*4+[21]*3+[26]*3

x = [10,16,46,14,6,6]
y = [1,5,37,4,3,3,]
#
LABELS = ('Disease-Chemical','Disease-Gene','Disease-Species','Disease-Disease','Chemical-Species','Chemical-Chemical')
#
# bins = numpy.linspace(0, 30, 30)
#
# width = 0.8
# plt.bar([0,5,10,15,20,25],x, width,alpha=0.5,label='Entity-Relation Search')
# plt.xsticks([0,5.4,10,15,20,25]+width/2,LABELS)
# # plt.hist(y, bins, alpha=0.5,label='OpenIE')
#
#
# plt.xlabel("Query Entity Types")
# plt.ylabel("Recall")
# plt.legend(loc='upper right')
# plt.show()
#
# # plot_url = py.plot_mpl(histogram, filename='docs/histogram-mpl-same')

N = 6
menMeans = (20, 35, 30, 35, 27)
womenMeans = (25, 32, 34, 20, 25)
menStd = (2, 3, 4, 1, 2)
womenStd = (3, 5, 2, 3, 3)
ind = numpy.arange(N)    # the x locations for the groups
width = 0.35       # the width of the bars: can also be len(x) sequence

ind  = ind +5
p1 = plt.bar(ind, x, width, color='blue',label='Entity-Relation Search')
p1 = plt.bar(ind+width, y, width, color='grey',label= 'OpenIE')




plt.xticks(ind + width/2., LABELS)
plt.xlabel("Query Entity Type Pairs")
plt.ylabel("Number of Correct Relations Returned")
plt.legend(loc='upper right')
plt.show()