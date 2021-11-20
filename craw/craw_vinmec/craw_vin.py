import requests
from bs4 import BeautifulSoup
import json
import pymongo
import lib

# myclient = pymongo.MongoClient("mongodb://localhost:27017/")

myclient = pymongo.MongoClient("mongodb+srv://admin:admin123@cluster.vfpxs.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

mydb = myclient["db_benh"]
mycol = mydb["benhs"]

# tạo webcraw vào DB
web = mydb["webs"]
web_vinmec = {"name":"Vinmec.com", "link_web_craw":"https://www.vinmec.com/vi/benh/", "uu_tien": 2,"day_create": lib.getdate(), "day_update":lib.getdate(), "status": 1}
webcraw = web.find_one({"name": "Vinmec.com"})
if (webcraw == None):
    resporn_web = web.insert_one(web_vinmec)
    id_web = resporn_web.inserted_id
else:
    id_web = webcraw["_id"]


link_web_craw = web_vinmec["link_web_craw"]

# defining the api-endpoint 
API_ENDPOINT = "http://127.0.0.1:8000/crf_get_trieu_chung"

def craw(url):
    list_benh = lib.get_link_benh(url)
    link_craw = mydb["link_craw"]
    for item in list_benh:
        linkcraw = link_craw.find_one({"link": item})
        if (linkcraw == None):
            Benh = ""
            benh = {}
            response = requests.get(item)
            soup = BeautifulSoup(response.content, "html.parser")
            Benh = lib.XacDinhBenh(soup)
            print(item)
            print(Benh)
            NoidungBenh = lib.XacDinhNoiDung(soup)
            benh["ten_benh"] = Benh
            noi_dung_khac = []
            for i in NoidungBenh:
                # Triệu chứng
                if(i["key"] == "Triệu chứng, biểu hiện bệnh"):
                    benh["trieu_chung"] = []
                    noidung = lib.create_thongtin(i, id_web, item)
                    benh["trieu_chung"].append(noidung)
                    
                    # input = { "noi_dung" : i["noidung"] }
                    # data = json.dumps(input)
                    # r = requests.post(url=API_ENDPOINT, data = data, headers={"Content-Type" : "application/json"})
                    # output = r.json()
                    # if(len(output["data"]) > 0):
                    #     benh["danh_sach_trieu_chung"] = []
                    #     for i in output["data"]:
                    #         data_TC = {"trieu_chung": " ".join(str(i["trieu_chung"]).split()), "thoi_gian":i["thoi_gian"]}
                    #         benh["danh_sach_trieu_chung"].append(data_TC )
                
                # Tổng quan bệnh
                elif(i["key"] == "Tổng quan bệnh"):
                    benh["tong_quan"] = []
                    noidung = lib.create_thongtin(i, id_web, item)
                    benh["tong_quan"].append(noidung)
                
                # Nguyên nhân gây bệnh
                elif(i["key"] == "Nguyên nhân gây bệnh"):
                    benh["nguyen_nhan"] = []
                    noidung = lib.create_thongtin(i, id_web, item)
                    benh["nguyen_nhan"].append(noidung)
                
                # Cách điều trị bệnh
                elif(i["key"] == "Cách điều trị bệnh"):
                    benh["cach_dieu_tri"] =[]
                    noidung = lib.create_thongtin(i, id_web, item)
                    benh["cach_dieu_tri"].append(noidung)
                
                # Cách phòng ngừa bệnh
                elif(i["key"] == "Cách phòng ngừa bệnh"):
                    benh["cach_phong_ngua"] = []
                    noidung = lib.create_thongtin(i, id_web, item)
                    benh["cach_phong_ngua"].append(noidung)
                
                # Đối tượng mắc bệnh
                elif(i["key"] == "Đối tượng mắc bệnh"):
                    benh["doi_tuong_mac_benh"] = []
                    noidung = lib.create_thongtin(i, id_web, item)
                    benh["doi_tuong_mac_benh"].append(noidung)
                
                # Các biện pháp chẩn đoán
                elif(i["key"] == "Các biện pháp chẩn đoán"):
                    benh["bien_phap_chuan_doan"] = []
                    noidung = lib.create_thongtin(i, id_web, item)
                    benh["bien_phap_chuan_doan"].append(noidung)
                
                # # Đường lây truyền
                # elif(i["key"] == "Đường lây truyền"):
                #     benh["duong_lay_truyen"] = []
                #     noidung = lib.create_thongtin(i, id_web, item)
                #     benh["duong_lay_truyen"].append(noidung)
                
                # nội dung khác
                else: 
                    noidung = lib.create_thongtin(i, id_web, item)
                    noi_dung_khac.append(noidung)
            
            if(Benh != None):
                # loại bở khoảng trống thừa
                Benh=" ".join(str(Benh).split())
                # kiểm tra trùng tên bệnh
                data_check = mycol.find_one({"ten_benh": Benh})
                benh["day_create"] = lib.getdate()
                benh["day_update"] = lib.getdate()
                benh["status"] = 1
                if(data_check == None):
                    resporn_benh = mycol.insert_one(benh)
                    noi_dung_khacs = mydb["noi_dung_khacs"]
                    id_benh = resporn_benh.inserted_id
                    for i in noi_dung_khac:
                        i["id_benh"] = id_benh
                        noi_dung_khacs.insert_one(i)
                else:
                    continue  
            link_craw.insert_one({"link":item,"day_create": lib.getdate()})  
                        
craw(link_web_craw)