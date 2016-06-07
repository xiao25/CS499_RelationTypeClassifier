import json
import itertools
import numpy as np
import operator

def readData(filename):
    with open(filename,'r') as file:
        json_str = file.read()

    dict = json.loads(json_str)
    return dict

def write2File(filename,obj):
    output = open(filename,"w")
    json.dump(obj,output,indent=4)

def chunkVP():
    global VP
    # VP_sorted = []
    # for (pattern,sent_ids) in VP.iteritems():
    #     VP_sorted.append((pattern,sent_ids,len(sent_ids)))
    result = sorted(VP.iteritems(), key = lambda t: len(t[1]),reverse=True)
    VP = result[:500]

Pattern = readData("pattern_DC2.json")
VP = readData("vp_DC2.json")
Entity = readData("entity_DC2.json")

chunkVP()

X_Meaning = []
patterns = []
alpha = 0.9
pattern_N = len(Pattern.keys())
pattern_rand = np.random.random(pattern_N)
pattern_rand /= pattern_rand.sum()
keys = Pattern.keys()
Xs = []

# for vp,vp_set in VP.iteritems():
for (vp,vp_set) in VP:
    print(vp)
    for (E1,E2) in itertools.combinations(Entity, 2):
        E1_set = set(Entity[E1])
        E2_set = set(Entity[E2])
        vp_set = set(vp_set)

        feature = []
        for i in xrange(pattern_N):
            pattern = keys[i]
            patterns.append(pattern)
            pattern_set = set(Pattern[pattern])
            E1_set_P = E1_set.intersection(pattern_set)
            E2_set_P = E2_set.intersection(pattern_set)
            vp_set_P = vp_set.intersection(pattern_set)
            NSC_E1_VP = E1_set_P.intersection(vp_set_P)
            NSC_E2_VP = E2_set_P.intersection(vp_set_P)
            NCS_E1_E2_VP = NSC_E1_VP.intersection(E2_set_P)
            dividen = len(NSC_E1_VP)+ len(NSC_E2_VP)
            NSC = len(NCS_E1_E2_VP)*2.0/dividen if dividen != 0 else 0
            # smooth with normalize to avoid sigular matrix
            NSC = NSC * alpha + (1-alpha)*pattern_rand[i]
            feature.append(NSC)
        if np.sum(feature) != (1-alpha):
        # if np.sum(feature) != 0:
            X_Meaning.append(("\t").join([E1,E2,vp]))
            Xs.append(feature)





foupt = open("XMeaning_DC2.txt","w")
for str_mean in X_Meaning:
    foupt.write(str_mean+'\n')
foupt.close()

foupt = open("Xs_DC2.txt","w")
for feature in Xs:
    feature_str = ','.join(map(str,feature))
    foupt.write(feature_str+'\n')
foupt.close()
