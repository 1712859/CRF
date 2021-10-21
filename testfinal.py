from vncorenlp import VnCoreNLP
annotator = VnCoreNLP(address="http://127.0.0.1", port=9001) 
import numpy as np
import os


# đường đẫn đến file rawdata
file_data_raw ="C:\\Users\\WIN10\\Desktop\\crf\\rawdata.txt"

# đường đã đến file trả kết quả (gẫn đến thư mục của thuận toán CRF++-0.58)
file_out_khong_tag1 = "C:\\Users\\WIN10\\Desktop\\crf\\CRF++-0.58\\test.data"

# đường đẫn từ thư mục của thuật toán CRF++-0.58 lưu file output.data
ten_file_du_lieu1 = "C:\\Users\\WIN10\\Desktop\\crf\\CRF++-0.58\\output.data"

def themdauchamcau(ten_file):
    f = open(ten_file, 'r', encoding='UTF-8')
    du_lieu_input = f.readlines()
    data = []
    for a in du_lieu_input:
        int_ = len(a)
        b = ""
        if (int_ >2):
            if (a[int_-2] not in [".",";","!","?"]):
                b = a[:(int_ -1)] + "."
            else:
                b = a
        data.append(b)
    f.close
    with open(ten_file, mode='w', encoding="utf-8" ) as file:
        for b in data:
            file.writelines(b + "\n")

def tao_file_dư_lieu3(ten_file_du_lieu, ten_file_output):
    f = open(ten_file_du_lieu, 'r', encoding='UTF-8')
    du_lieu_input = f.read()
    doc = annotator.annotate(du_lieu_input) 
    with open(ten_file_output, mode='w', encoding="utf-8" ) as file:
            for cau in doc["sentences"]:
                for tu in cau:
                    tab = "\t"
                    if (len(tu["form"]) <= 15):
                        tab += "\t"
                    if (len(tu["form"]) <= 7):
                        tab += "\t"
                    if(tu["form"] in [".",";","!","?","\n"]):
                        file.writelines("\n")
                    elif(["form"] not in [")",">","/",":", ",", "\"","`","(","<","”","“"]):
                        file.writelines((tu["form"]).lower() + tab + tu["posTag"] + "\n")

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

themdauchamcau(file_data_raw)

tao_file_dư_lieu3(file_data_raw, file_out_khong_tag1)

# os.system('cmd /k "cd C:\\Users\\WIN10\\Desktop\\crf\\CRF++-0.58 && crf_test -m model test.data > output.data && cd C:\\Users\\WIN10\\Desktop\\crf && python c:/Users/WIN10/Desktop/crf/gettrieuchung.py"')
os.system("cd C:\\Users\\WIN10\\Desktop\\crf\\CRF++-0.58 && crf_test -m model test.data > output.data && cd C:\\Users\\WIN10\\Desktop\\crf ")

data1 = getTrieuChungBenh1(ten_file_du_lieu1)
print("tách từng từ: "+ str(len(data1)) + "\n")
for a in data1:
    print(a)

    
