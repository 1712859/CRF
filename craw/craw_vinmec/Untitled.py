
import requests
from bs4 import BeautifulSoup
import json
import pymongo
import lib



item = "https://www.vinmec.com/vi/benh/can-thi-3119/"
id_web = ""
benh = lib.createbenh()
response = requests.get(item)
soup = BeautifulSoup(response.content, "html.parser")
NoidungBenh = lib.XacDinhNoiDung(soup)
NoidungBenh = NoidungBenh[2]
benh["ten_benh"] = lib.XacDinhBenh(soup)
print(item)
print(benh["ten_benh"])
noi_dung_khac = []
for i in NoidungBenh:
    # Triệu chứng
    if(i["key"] == "Triệu chứng, biểu hiện bệnh"):
        benh["trieu_chung"] = []
        noidung = lib.create_thongtin(i, id_web, item)
        benh["trieu_chung"].append(noidung)
        

        