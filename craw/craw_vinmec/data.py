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
    noiDungTag = {"tieu_de": "", "noidung":[], "key":""}
    list_noidung = []
    count = 0
    list_tieude = timTieuDeNoiDung(soup)
    for i in contents:
        content = {"type":"", "content":""}
        if (i.name == 'h2'):
            if(i.text in list_tieude):
                if(count != 0):
                    list_noidung.append(noiDungTag)
                    noiDungTag = {"tieu_de": "", "noidung":[], "key":""}
                noiDungTag["tieu_de"] = i.text
                noiDungTag["noidung"] = []
                count += 1
        else:
            if(i.name == "li"):
                content["type"] = "li"
                if(len(i.find_all("p")) != 0):
                    content["content"] = i.text
                    noiDungTag["noidung"].append(content)
            elif(i.name == "p"):
                content["type"] = "p"
                if(len(i.find_parents("li")) != 0):
                    continue
                else:
                    content["content"] = i.text
                    noiDungTag["noidung"].append(content)
            elif(i.name == "h3"):
                content["type"] = "h3"
                content["content"] = i.text
                noiDungTag["noidung"].append(content)
            elif(i.name == "h4"):
                content["type"] = "h4"
                content["content"] = i.text
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
    benh = h1.text.split(':')
    return benh[0]

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