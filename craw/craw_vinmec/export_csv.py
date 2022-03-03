import requests
from bs4 import BeautifulSoup
import json
import pymongo
import lib

myclient = pymongo.MongoClient("mongodb+srv://admin:admin123@cluster.vfpxs.mongodb.net/HealthAssistant?retryWrites=true&w=majority")

ten_file_du_lieu = ".\\api\\data1.csv"

mydb = myclient["HealthAssistant"]
benh = mydb["Benh"]
trieu_chung = mydb["TrieuChung"]
data1 = benh.find()
data2 = trieu_chung.find()

f = open(ten_file_du_lieu, 'w', encoding='UTF-8')

line1 = "Labels"
num = 0
data = []
for i in data2:
    line1 += "," + i["trieu_chung"].strip(',')
    data.append(i["trieu_chung"])
f.writelines(line1 + "\n")

lines = []
for a in data1:
    line = "" + a["ten_benh"].replace(",", "")
    if(a["danh_sach_trieu_chung"] != []):
        danh_sach = a["danh_sach_trieu_chung"]
        for ba in data:
            check = 0
            for da in danh_sach:
                if(ba == da["trieu_chung"]):
                    line += "," + str(da["point"] )
                    check = 0
                    break
                else:
                    check = 1
            if(check == 1):
                line += ",0"
        
        lines.append(line + "\n")

for item in lines:
    f.writelines(item)
