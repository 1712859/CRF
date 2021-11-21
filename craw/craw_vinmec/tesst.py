import requests
from bs4 import BeautifulSoup
import json
import pymongo
import lib


myclient = pymongo.MongoClient("mongodb://localhost:27017/")

# myclient = pymongo.MongoClient("mongodb+srv://admin:admin123@cluster.vfpxs.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

mydb = myclient["db_benh"]
mycol = mydb["benhs"]

data_check = mycol.find_one({"ten_benh": "Rối loạn tiền đình"})


