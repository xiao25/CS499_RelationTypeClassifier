from nltk.corpus import wordnet as wn

def generate_dict(pos_seed):
    pos_dict = {}
    pos_result_step = []
    for step in range(12):
        for pos in pos_seed:
            pos_result_step = []
            for synset in wn.synsets(pos):
                for lemma in synset.lemmas():
                    name = lemma.name()
                    if name not in pos_dict.keys():
                        pos_dict[name] = step+1
                        pos_result_step.append(name)
        pos_seed = pos_result_step
    return pos_dict

