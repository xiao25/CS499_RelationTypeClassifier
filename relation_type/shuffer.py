fd = open("Medicine_Disease.txt", "r")
list = []
for line in fd:
    list.append(line)
fd.close()


fd = open("label","r")
label = []
for line in fd:
    label.append(line)
fd.close()

list1 = []
list2 = []
label1 = []
label2 = []
for i in range(len(list)):
    if(i % 2 == 0):
        list1.append(list[i])
        label1.append(label[i])
    else:
        list2.append(list[i])
        label2.append(label[i])

list = list1 + list2
label = label1 + label2



fd = open("Medicine_Disease_Shuffer", "w")
for line in list:
    fd.write(line)
fd.close()

fd = open("label_Shuffer", "w")
for line in label:
    fd.write(line)
fd.close()

