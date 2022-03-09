import requests
from datetime import datetime
from bs4 import BeautifulSoup

link_web_vin = "https://www.vinmec.com"

def getdate():
    now = datetime.today()
    current_time = now.strftime("%d/%m/%Y %H:%M:%S")
    return current_time

thanhPhanBaiViet = {
    "Tổng quan bệnh": [ "tổng quan"],
    "Triệu chứng, biểu hiện bệnh": ["triệu chứng"],
    "Nguyên nhân gây bệnh": ["nguyên nhân"],
    "Cách điều trị bệnh": ["điều trị"],
    "Cách phòng ngừa bệnh": ["phòng ngừa",],
    "Đối tượng mắc bệnh": ["đối tượng"],
    "Các biện pháp chẩn đoán": ["chẩn đoán"],
    "Đường lây truyền": ["dường lây truyền"],
    "Biến chứng của bệnh": ["biến chứng"]    
}

def get_link_benh(link_web):
    response = requests.get(link_web)
    soup = BeautifulSoup(response.content, "html.parser")
    ul = soup.findAll("ul", {"class":"collapsible-target"})
    links = []
    for item in ul:
        a = item.findAll("a")
        for item1 in a:
            links.append(link_web_vin  + item1.attrs["href"])
    return links

def timTieuDeNoiDung(soup):
    contents_body = soup.find("div", class_="content")
    contents = contents_body.findAll("h2")
    titles = []
    for item in contents:
        titles.append(item.text)

    return titles[1:len(titles)]

def catNoiDungTag(soup):
    contents_body = soup.find("div", class_="content")
    contents = contents_body.findAll(["h2","h3","h4","h5","h6","li","p"])    
    noiDungTag = {"tieu_de": "" , "key":"", "noidung":[]}
    list_noidung = []
    count = 0
    list_tieude = timTieuDeNoiDung(soup)
    for i in contents:
        content = {"type":"", "content":""}
        if (i.name == "h2"):
            if((i.text).replace('\n', ' ').replace('\r', '') in list_tieude):
                if(count != 0):
                    list_noidung.append(noiDungTag)
                    noiDungTag = {"tieu_de": "" , "key":"", "noidung":[]}
                noiDungTag["tieu_de"] = (i.text).replace('\n', ' ').replace('\r', '')
                count += 1
        else:
            if(i.name == "li"):
                content["type"] = "li"
                if(len(i.find_all("li")) != 0):
                    if(len(i.find_all("p")) != 0):
                        list_a = i.find_all("p")
                        
                        content["type"] = "li"
                        content["content"] = list_a[0].text
                        noiDungTag["noidung"].append(content)
                    else:
                        continue
                else:
                    if(len(i.find_parents("li")) != 0):
                        content["type"] = "li1"
                        content["content"] = (i.text).replace('\n', ' ').replace('\r', '')
                        noiDungTag["noidung"].append(content)
                    else:
                        content["content"] = (i.text).replace('\n', ' ').replace('\r', '')
                        noiDungTag["noidung"].append(content)
            if(i.name == "p"):
                if((i.text).replace('\n', ' ').replace('\r', '') == "Xem thêm:"):
                    break
                else:
                    content["type"] = "p"
                    if(len(i.find_parents("li")) != 0):
                        continue
                    else:
                        content["content"] = (i.text).replace('\n', ' ').replace('\r', '')
                        noiDungTag["noidung"].append(content)
            else:
                  
                if(i.name == "h3"):
                    content["type"] = "h3"
                    content["content"] = (i.text).replace('\n', ' ').replace('\r', '')
                    noiDungTag["noidung"].append(content)
                elif(i.name == "h4"):
                    content["type"] = "h4"
                    content["content"] = (i.text).replace('\n', ' ').replace('\r', '')
                    noiDungTag["noidung"].append(content)
    list_noidung.append(noiDungTag)
    return list_noidung

def XacDinhNoiDung(soup):
    data = catNoiDungTag(soup)
    output = []
    for tieude in data:
        for key in thanhPhanBaiViet.keys():
            for item in thanhPhanBaiViet.get(key):
                if((tieude["tieu_de"].lower()).find(item.lower())!= -1):
                    tieude["key"] = key
        output.append(tieude)               
                            
                    
    return output

def XacDinhBenh(soup):
    contents= soup.find("div", class_="mask")
    h1 = contents.find("h1")
    benh = h1.text.split(":")
    return benh[0]

def create_thongtin(i, id_web, link_web):
    
    return  {
    "tieu_de":i["tieu_de"],
    "noi_dung":i["noidung"], 
    "do_uu_tien": 2, 
    "link_web": link_web, 
    "id_web": id_web ,
    "create_date": getdate(), 
    "update_date": getdate(),
    "create_user": "",
    "update_user": "",
    "status": 1 }

def createbenh():
    data = {
    "ten_benh":"",
    "trieu_chung":[],
    "nguyen_nhan":[], 
    "tong_quan":[], 
    "cach_dieu_tri":[], 
    "cach_phong_ngua":[], 
    "doi_tuong_mac_benh":[], 
    "bien_phap_chuan_doan":[], 
    "duong_lay_truyen":[], 
    "bien_chung":[],
    "danh_sach_trieu_chung": [],
    "create_date": "",
    "update_date": "",
    "create_user": "",
    "update_user": "",
    "status" : 1
    }
    
    return data

def update_thongtin(data):
    return{
               "tieu_de":data["tieu_de"],
                "noi_dung":data["noi_dung"],
                "do_uu_tien": data["do_uu_tien"], 
                "link_web": data["link_web"], 
                "id_web": data["id_web"],
                "create_date": data["create_date"],
                "update_date": data["update_date"],
                "create_user": data["create_user"],
                "update_user": data["update_user"],
                "status": data["status"]
            }

def update_benh(update_data,benh):

    if(len(benh["trieu_chung"]) !=0):
        for data in benh["trieu_chung"]:
            temp = update_thongtin(data)
            update_data["trieu_chung"].append(temp)
    
    if(len(benh["nguyen_nhan"]) !=0):
        for data in benh["nguyen_nhan"]:
            temp = update_thongtin(data)
            update_data["nguyen_nhan"].append(temp)
    
    if(len(benh["tong_quan"]) !=0):
        for data in benh["tong_quan"]:
            temp = update_thongtin(data)
            update_data["tong_quan"].append(temp)

    if(len(benh["cach_dieu_tri"]) !=0):
        for data in benh["cach_dieu_tri"]:
            temp = update_thongtin(data)
            update_data["cach_dieu_tri"].append(temp)
    
    if(len(benh["cach_phong_ngua"]) !=0):
        for data in benh["cach_phong_ngua"]:
            temp = update_thongtin(data)
            update_data["cach_phong_ngua"].append(temp)

    if(len(benh["doi_tuong_mac_benh"]) !=0):
        for data in benh["doi_tuong_mac_benh"]:
            temp = update_thongtin(data)
            update_data["doi_tuong_mac_benh"].append(temp)
    
    if(len(benh["bien_phap_chuan_doan"]) !=0):
        for data in benh["bien_phap_chuan_doan"]:
            temp = update_thongtin(data)
            update_data["bien_phap_chuan_doan"].append(temp)
    
    if(len(benh["duong_lay_truyen"]) !=0):
        for data in benh["duong_lay_truyen"]:
            temp = update_thongtin(data)
            update_data["duong_lay_truyen"].append(temp)

    if(len(benh["bien_chung"]) !=0):
        for data in benh["bien_chung"]:
            temp = update_thongtin(data)
            update_data["bien_chung"].append(data)

    return  update_data
    
def sosanh(a,b):
    if(a["trieu_chung"] == b["trieu_chung"]):
        if(a["thoi_gian"] == b["thoi_gian"]):
            return 1
        else:
            return 2
    return 3

def loai_lap(data):
    data_final = []
    for item in data:
        if(len(data_final) == 0):
            data_final.append(item)
        else:
            check = True
            for a in data_final: 
                out = sosanh(a,item)
                if(out == 3):
                    check = False
                elif(out == 2):
                    item["thoi_gian"] = item["thoi_gian"] + " , " + a["thoi_gian"]
                    check = False
                else:
                    check = True
                    break
            if(check == False):
                data_final.append(item)

    count = 0
    for out in data_final:
        for out1 in data_final:
            if(out["trieu_chung"] == out1["trieu_chung"] and out["thoi_gian"] != out1["thoi_gian"]):
                data_final.remove(out1)
                if(out["thoi_gian"] == ""):
                    data_final[count]["thoi_gian"] =  out1["thoi_gian"]
                elif(out1["thoi_gian"] == ""):
                    data_final[count]["thoi_gian"] = out["thoi_gian"]
                else: 
                    data_final[count]["thoi_gian"] = out["thoi_gian"] + " , " + out1["thoi_gian"]
        count +=1
    return data_final