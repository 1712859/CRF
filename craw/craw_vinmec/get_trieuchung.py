import requests
from bs4 import BeautifulSoup
import json
import pymongo
import lib

# defining the api-endpoint 
API_ENDPOINT = "http://127.0.0.1:8000/crf_get_trieu_chung"

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

# myclient = pymongo.MongoClient("mongodb+srv://admin:admin123@cluster.vfpxs.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

mydb = myclient["db_benh"]
mycol = mydb["benhs"]

datas = mycol.find()

for itemp in datas:
    print(itemp["ten_benh"])
    trieu_chung = ""
    raw = []
    max = 0
    for item in itemp["trieu_chung"]:
        if (max < item["do_uu_tien"]):
            max = item["do_uu_tien"]
            raw = item["noi_dung"]
    for item in raw:
        trieu_chung = trieu_chung + item["content"]
    if(trieu_chung != ""):
        input = { "noi_dung" : trieu_chung }
        data = json.dumps(input)
        r = requests.post(url=API_ENDPOINT, data = data, headers={"Content-Type" : "application/json"})
        output = r.json()
        list_trieuchung = []
        if(len(output["data"]) > 0):
            for i in output["data"]:
                data_TC = {"trieu_chung": " ".join(str(i["trieu_chung"]).split()), "thoi_gian":i["thoi_gian"]}
                list_trieuchung.append(data_TC )

        output_final = lib.loai_lap(list_trieuchung)
        myquery = {"ten_benh": itemp["ten_benh"]}
        newvalues = { "$set": { "danh_sach_trieu_chung" : output_final}}
        mycol.update_one(myquery, newvalues)




