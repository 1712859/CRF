from numpy.core.fromnumeric import around


f = open("C:\\Users\\WIN10\\Desktop\\CRF\\CRF++-0.58\\train_1.data", 'r', encoding='UTF-8')
data = f.readlines()
raed = open("C:\\Users\\WIN10\\Desktop\\CRF\\craw\\craw_vinmec\\error.data", 'r', encoding='UTF-8')
dataero = raed.readlines()
dataero.sort()
dataerror = []
for item in dataero:
    if(len(item)>1):
        temp = item.split()
        dataerror.append(temp)
all_data = []
list = []
# for item in data:
#     if(len(item) < 2):
#         if(len(list) != 0):
#             all_data.append(list)
#             list = []
#     else:
#         temp = item.split()
#         list.append(temp)

for item in data:
        temp = item.split()
        all_data .append(temp)
write = open("C:\\Users\\WIN10\\Desktop\\CRF\\CRF++-0.58\\check.data", 'w', encoding='UTF-8')
count = 1
count2 = 1
check = []
for item in all_data:
    for item1 in all_data:
        if (len(item) >1 and len(item1) >1):
            if(item[0] not in check):
                if(item[0] == item1[0] and item[1] == item1[1]and item[2] != item1[2] and item[2] == "B-TC" and item1[2] == "OTH" ):
                    haha = 1
                    for item2 in dataerror:
                        if(item1[0] == item2[0] and item1[1] == item2[1] and item1[2] == item2[2] and count2 == int(item2[3])):
                            haha = 0
                            break
                    if(haha == 1):
                        check.append(item[0])
                        print(str(count)+ " - "+ item[2] + " - " +item[0]+ " = " +item1[0] + "\t"+ item1[2] + "\t" +item1[1] + "\t" +item1[0] + "\t" +str(count2))
                        write.writelines(str(count)+ " - "+ item[2] + " - " +item[0]+ " = " + item1[0] + "\t" +item1[1] + "\t" +item1[2] + "\t" +str(count2) + "\n")
        count2 += 1
    count += 1
    count2 = 1

write1 = open("C:\\Users\\WIN10\\Desktop\\CRF\\CRF++-0.58\\checkB-TC.data", 'w', encoding='UTF-8')
for a in check:
    write1.writelines(a + "\n")


