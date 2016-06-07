import json
import matplotlib.pyplot as plt
import numpy as np
from operator import itemgetter

def readData(filename):
    with open(filename,'r') as file:
        json_str = file.read()

    dict = json.loads(json_str)
    return dict




Pattern = readData("pattern_DD.json")
Pattern_lst = [(pattern,len(sent_list)) for pattern,sent_list in Pattern.items()]

Pattern_lst = sorted(Pattern_lst, key = itemgetter(1),reverse=True)

print('\n\n')
patterns = []
frequencies = []
for (pattern,frequency) in Pattern_lst:
    print(pattern)
    patterns.append(pattern)
    frequencies.append(frequency)
    if len(patterns) == 10:
        break


N = 10
ind = np.arange(N)    # the x locations for the groups
width = 0.35       # the width of the bars: can also be len(x) sequence
ind += 1
p1 = plt.bar(ind, frequencies, width)
plt.xticks(ind+width/2, ['1','2','3','4','5','6','7','8','9','10'])
plt.title('Disease-Species')
plt.show()

