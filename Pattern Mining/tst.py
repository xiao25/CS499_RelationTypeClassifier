import os
import json
entity = []

for filename in os.listdir('/Users/ztx/PycharmProjects/New_CS499/Pattern Mining/Corpus'):
    parts = filename.split('_')
    entity.append(parts[1].lower())
    entity.append(parts[2].replace(".txt",'').lower())


set_E = list(set(entity))
output = open("EntityName.json","w")
json.dump(set_E,output)