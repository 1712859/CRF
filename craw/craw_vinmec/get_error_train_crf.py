from sqlite3 import adapters
from numpy.core.fromnumeric import around


f = open(".\\CRF++-0.58\\train_1.data", 'r', encoding='UTF-8')
data = f.readlines()
raed = open(".\\craw\\craw_vinmec\\error.data", 'r', encoding='UTF-8')
dataero = raed.readlines()
dataero.sort()
# sap xep lai file error
a = open(".\\craw\\craw_vinmec\\error.data", 'w', encoding='UTF-8')
for i in dataero:
    a.writelines(i)

dataerror = []
for item in dataero:
    if(len(item)>1):
        temp = item.split()
        dataerror.append(temp)
all_data = []
list = []

for item in data:
        temp = item.split()
        all_data .append(temp)
write = open(".\\craw\\craw_vinmec\\check.data", 'w', encoding='UTF-8')
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
                        print(str(count)+ " - "+ item[2] + " - " +item[0]+ " = " +item1[0] + "\t"+ item1[2]  + "\t" +str(count2))
                        write.writelines(str(count)+ " - "+ item[2] + " - " +item[0]+ " = " + item1[0] + "\t" +item1[1] + "\t" +item1[2] + "\t" +str(count2) + "\n")
        count2 += 1
    count += 1
    count2 = 1

write1 = open(".\\craw\\craw_vinmec\\checkB-TC.data", 'w', encoding='UTF-8')
for a in check:
    write1.writelines(a + "\n")
