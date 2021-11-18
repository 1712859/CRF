import requests
from bs4 import BeautifulSoup
import json
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]

mycol = mydb["benhs"]

id_web = "617c150e3aa27c51e7496b44"


link_web_vin = "https://www.vinmec.com"
link_web_craw = "https://www.vinmec.com/vi/benh/"

# defining the api-endpoint 
API_ENDPOINT = "http://127.0.0.1:8000/crf_get_trieu_chung"

# hàm lây danh sách link bệnh được viết trên trang web
def get_link_benh(link_web):
    response = requests.get(link_web)
    soup = BeautifulSoup(response.content, "html.parser")
    ul = soup.findAll('ul', {"class":"collapsible-target"})
    links = []
    for item in ul:
        a = item.findAll('a')
        for item1 in a:
            links.append(link_web_vin  + item1.attrs["href"])
    return links

thanhPhanBaiViet = {
    "Tổng quan bệnh": [ "Tổng quan"],
    "Triệu chứng, biểu hiện bệnh": ["triệu chứng"],
    "Nguyên nhân gây bệnh": ["nguyên nhân"],
    "Cách điều trị bệnh": ["điều trị"],
    "Cách phòng ngừa bệnh": ["phòng ngừa",],
    "Đối tượng mắc bệnh": ["đối tượng"],
    "Các biện pháp chẩn đoán": ["chẩn đoán"]    
}

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
    noiDungTag = {"tieu_de": "", "noidung":"", "key":"", "list":[]}
    list_noidung = []
    count = 0
    list_tieude = timTieuDeNoiDung(soup)
    for i in contents:
        content = {"type":"", "content":""}
        if (i.name == 'h2'):
            if(i.text in list_tieude):
                if(count != 0):
                    list_noidung.append(noiDungTag)
                    noiDungTag = {"tieu_de": "", "noidung":"", "key":"", "list":[]}
                noiDungTag["tieu_de"] = i.text
                noiDungTag["noidung"] = ""
                count += 1
        else:
            if(i.name == "li"):
                content["type"] = "li"
                if(len(i.find_all("p")) != 0):
                    content["content"] = i.text
                    noiDungTag["list"].append(content)
                    noiDungTag["noidung"] +=  i.text + "\n"
            if(i.name == "p"):
                content["type"] = "p"
                if(len(i.find_parents("li")) != 0):
                    continue
                else:
                    noiDungTag["noidung"] +=  i.text + "\n"
                    content["content"] = i.text
                    noiDungTag["list"].append(content)
            else:
                noiDungTag["noidung"] +=  i.text + "\n"
                if(i.name == "h3"):
                    content["type"] = "h3"
                    content["content"] = i.text
                    noiDungTag["list"].append(content)
                elif(i.name == "h4"):
                    content["type"] = "h4"
                    content["content"] = i.text
                    noiDungTag["list"].append(content)
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
    benh = h1.text.split(':')
    return benh[0]

def craw(url):
    list_benh = get_link_benh(url)
    link_craw = mydb["link_craw"]
    for item in list_benh:
        linkcraw = link_craw.find_one({"link": item})
        if (linkcraw == None):
            print(item)
            link_craw.insert_one({"link":item})
            benh = {}
            response = requests.get(item)
            soup = BeautifulSoup(response.content, "html.parser")
            Benh = XacDinhBenh(soup)
            print(Benh)
            NoidungBenh = XacDinhNoiDung(soup)
            benh["ten_benh"] = Benh
            for i in NoidungBenh:
                # Triệu chứng
                if(i["key"] == "Triệu chứng, biểu hiện bệnh"):
                    benh["trieu_chung"] = []
                    trieu_chung = {"noi_dung":i["list"], "do_uu_tien": 1, "link_web": item, "id_web": id_web ,"status": 1}
                    benh["trieu_chung"].append(trieu_chung)
                    input = { "noi_dung" : i["noidung"] }
                    data = json.dumps(input)
                    r = requests.post(url=API_ENDPOINT, data = data, headers={"Content-Type" : "application/json"})
                    output = r.json()
                    if(len(output["data"]) > 0):
                        benh["danh_sach_trieu_chung"] = []
                        for i in output["data"]:
                            data_TC = {"trieu_chung": i["trieu_chung"], "thoi_gian":i["thoi_gian"]}
                            benh["danh_sach_trieu_chung"].append(data_TC )
                
                # Tổng quan bệnh
                elif(i["key"] == "Tổng quan bệnh"):
                    benh["tong_quan"] = []
                    trieu_chung = {"noi_dung":i["list"], "do_uu_tien": 1, "link_web": item, "id_web": id_web ,"status": 1}
                    benh["tong_quan"].append(trieu_chung)
                
                # Nguyên nhân gây bệnh
                elif(i["key"] == "Nguyên nhân gây bệnh"):
                    benh["nguyen_nhan"] = []
                    trieu_chung = {"noi_dung":i["list"], "do_uu_tien": 1, "link_web": item, "id_web": id_web ,"status": 1}
                    benh["nguyen_nhan"].append(trieu_chung)
                
                # Cách điều trị bệnh
                elif(i["key"] == "Cách điều trị bệnh"):
                    benh["cach_dieu_tri"] =[]
                    trieu_chung = {"noi_dung":i["list"], "do_uu_tien": 1, "link_web": item, "id_web": id_web ,"status": 1}
                    benh["cach_dieu_tri"].append(trieu_chung)
                
                # Cách phòng ngừa bệnh
                elif(i["key"] == "Cách phòng ngừa bệnh"):
                    benh["cach_phong_ngua"] = []
                    trieu_chung = {"noi_dung":i["list"], "do_uu_tien": 1, "link_web": item, "id_web": id_web ,"status": 1}
                    benh["cach_phong_ngua"].append(trieu_chung)
                
                # Đối tượng mắc bệnh
                elif(i["key"] == "Đối tượng mắc bệnh"):
                    benh["doi_tuong_mac_benh"] = []
                    trieu_chung = {"noi_dung":i["list"], "do_uu_tien": 1, "link_web": item, "id_web": id_web ,"status": 1}
                    benh["doi_tuong_mac_benh"].append(trieu_chung)
                
                # Các biện pháp chẩn đoán
                elif(i["key"] == "Các biện pháp chẩn đoán"):
                    benh["bien_phap_chuan_doan"] = []
                    trieu_chung = {"noi_dung":i["list"], "do_uu_tien": 1, "link_web": item, "id_web": id_web ,"status": 1}
                    benh["bien_phap_chuan_doan"].append(trieu_chung)
                
                # nội dung khác
                else:
                    benh["noi_dung_khac"] =[] 
                    trieu_chung = {"tieu_de":i["tieu_de"],"noi_dung":i["list"], "do_uu_tien": 1, "link_web": item, "id_web": id_web ,"status": 1}
                    benh["noi_dung_khac"].append(trieu_chung)
            
        # loại bở khoảng trống thừa
        Benh=" ".join(str(Benh).split())
        # kiểm tra trùng tên bệnh
        data_check = mycol.find_one({"ten_benh": Benh})
        if(data_check == None):
            mycol.insert_one(benh)

craw(link_web_craw)

# demo (không sài)
def craw_TC(url):
    list_benh = get_link_benh(url)
    f = open("C:\\Users\\WIN10\\Desktop\\vinmec2.txt", mode='w', encoding="utf-8" )
    with open("C:\\Users\\WIN10\\Desktop\\vinmec_TC2.txt", mode='w', encoding="utf-8" ) as file_link:
        for item in list_benh:
            print(item)
            response = requests.get(item)
            soup = BeautifulSoup(response.content, "html.parser")
            Benh = XacDinhBenh(soup)
            print(Benh)
            NoidungBenh = XacDinhNoiDung(soup)
            file_link.writelines("####" + Benh +"\n")
            file_link.writelines("## " + item +"\n")
            f.writelines("####" + Benh +"\n")
            f.writelines("## " + item +"\n")
            for i in NoidungBenh:
                if(i["key"] == "Triệu chứng, biểu hiện bệnh"):
                    f.writelines(i["noidung"] +"\n\n")
                    input = { "noi_dung" : i["noidung"] }
                    data = json.dumps(input)
                    r = requests.post(url=API_ENDPOINT, data = data, headers={"Content-Type" : "application/json"})
                    output = r.json()
                    if(len(output["data"]) > 0):
                        
                        for i in output["data"]:
                            file_link.writelines( str(i["trieu_chung"]) + " - " + str(i["thoi_gian"])  +"\n")
                            
    craw_TC(link_web_craw)







 