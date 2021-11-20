import requests
from datetime import datetime
from bs4 import BeautifulSoup

link_web_vin = "https://www.vinmec.com"

def getdate():
    now = datetime.today()
    current_time = now.strftime("%d/%m/%Y %H:%M:%S")
    return current_time

thanhPhanBaiViet = {
    "Tổng quan bệnh": [ "Tổng quan"],
    "Triệu chứng, biểu hiện bệnh": ["triệu chứng"],
    "Nguyên nhân gây bệnh": ["nguyên nhân"],
    "Cách điều trị bệnh": ["điều trị"],
    "Cách phòng ngừa bệnh": ["phòng ngừa",],
    "Đối tượng mắc bệnh": ["đối tượng"],
    "Các biện pháp chẩn đoán": ["chẩn đoán"],
    "Đường lây truyền": ["Đường lây truyền"],
    "Biến chứng của bệnh": ["biến chứng"]    
}

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

def create_thongtin(i, id_web, link_web):
    return  {"tieu_de":i["tieu_de"],
    "noi_dung":i["list"], 
    "do_uu_tien": 1, 
    "link_web": link_web, 
    "id_web": id_web ,
    "day_create": getdate(), 
    "day_update":getdate(),
    "status": 1 }

    