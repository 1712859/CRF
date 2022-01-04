import requests
from bs4 import BeautifulSoup
import json
import pymongo
import lib

# defining the api-endpoint 
API_ENDPOINT = "http://127.0.0.1:8000/crf_get_trieu_chung"

# myclient = pymongo.MongoClient("mongodb://localhost:27017/")

myclient = pymongo.MongoClient("mongodb+srv://admin:admin123@cluster.vfpxs.mongodb.net/HealthAssistant?retryWrites=true&w=majority")

mydb = myclient["HealthAssistant"]
mycol = mydb["TrieuChung"]
datas = mycol.find()

temp = {'value': '', 'synonyms': []}

data = []
for a in datas:
    temp["value"] = a["trieu_chung"]
    temp["synonyms"].append(a["trieu_chung"])
    data.append(temp)
    temp = {'value': '', 'synonyms': []}


file = open("c:\\Users\\rivoco\\Desktop\\CRF\\craw\\trieu_chung.json", mode='w', encoding="utf-8" )

file.writelines(str(data))
