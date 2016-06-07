


def readFile(filename):

    patterns = []
    initial = True
    max = min  = -1
    with open(filename,'r') as finout:
        for line in finout:
            parts = line.split('\t')
            score = float(parts[1])
            if initial:
                max = min = float(parts[1])
                initial = False
            else:

                max = score if score > max else max
                min = score if score < min else min

            patterns.append((parts[0],score))

    range = max - min

    foutput = open('pattern_DC3.txt','w')
    for (pattern, score) in patterns:
        new_score = (score - min)/range
        foutput.write("%s\t%s\n"%(pattern,new_score))

    foutput.close()

readFile('/Users/ztx/PycharmProjects/New_CS499/Pattern Mining/pattern_nsc_DC2.txt')