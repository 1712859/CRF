import numpy as np


# đường đẫn từ thư mục của thuật toán CRF++-0.58 lưu file output.data
ten_file_du_lieu1 = "C:\\Users\\WIN10\\Desktop\\CRF++-0.58\\output.data"

def getTrieuChungBenh1(ten_file_du_lieu):
    f = open(ten_file_du_lieu, 'r', encoding='UTF-8')
    du_lieu_input = f.readlines()
    output = []
    temp = {'trieu_chung':'','thoi_gian':''}
    count = 0
    for a in du_lieu_input:
        row = a.split()
        rows = np.array(row)
        if (len(rows)==3):
            if (rows[2] == "B-TC"):
                count +=1
            if (count <= 1):
                if(rows[2] in ["B-TC","I-TC"]):
                    temp["trieu_chung"] += rows[0].replace("_"," ") + " "
                if(rows[2] in ["B-TG","I-TG"]):
                    temp["thoi_gian"] += rows[0].replace("_"," ") + " "
            else:
                count = 1
                output.append(temp)
                # print(temp["trieu_chung"])
                temp = {'trieu_chung': rows[0].replace("_"," ") + " ",'thoi_gian':''}
    return output            


# getTrieuChungBenh1(ten_file_du_lieu)
data1 = getTrieuChungBenh1(ten_file_du_lieu1)
print("tách từng từ: "+ str(len(data1)) + "\n")
for a in data1:
    print(a["trieu_chung"] )