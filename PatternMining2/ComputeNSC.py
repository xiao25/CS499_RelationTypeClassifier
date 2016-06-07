import json
import itertools
import numpy as np

def readData(filename):
    with open(filename,'r') as file:
        json_str = file.read()

    dict = json.loads(json_str)
    return dict


Pattern_Entity = readData("pattern_entity2.json")
Pattern = readData("pattern2.json")
Entity = readData("entity2.json")



def encryptKeys(pattern,entity1,entity2):
    if entity2 == None:
        return entity1 + pattern
    if entity1 > entity2:
        return entity1 + entity2 + pattern
    else:
        return entity2 + entity2 + pattern

patterns = []
alpha = 0.9
pattern_N = len(Pattern.keys())
pattern_rand = np.random.random(pattern_N)
pattern_rand /= pattern_rand.sum()
keys = Pattern.keys()
Xs = []

for (E1,E2) in itertools.combinations(Entity, 2):
    feature = []
    for i in xrange(pattern_N):
        pattern = keys[i]
        NSC_E1_P_key = encryptKeys(pattern,E1,None)
        NSC_E2_P_key = encryptKeys(pattern,E2,None)
        NSC_E1_E2_P_key = encryptKeys(pattern,E1,E2)

        NSC_E1_P = Pattern_Entity[NSC_E1_P_key] if NSC_E1_P_key in Pattern_Entity else 0
        NSC_E2_P = Pattern_Entity[NSC_E2_P_key] if NSC_E2_P_key in Pattern_Entity else 0
        NSC_E1_E2_P = Pattern_Entity[NSC_E1_E2_P_key] if NSC_E1_E2_P_key in Pattern_Entity else 0

        dividen = NSC_E1_P + NSC_E2_P
        NSC = NSC_E1_E2_P*2.0/dividen if dividen != 0 else 0

        # NSC = NSC * alpha + (1-alpha)*pattern_rand[i]
        feature.append(NSC)


    Xs.append(feature)


foupt = open("Xs2.txt","w")
for feature in Xs:
    feature_str = ','.join(map(str,feature))
    foupt.write(feature_str+'\n')
foupt.close()