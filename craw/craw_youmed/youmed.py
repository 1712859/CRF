
import requests
from bs4 import BeautifulSoup
import json
link_web_craw = "https://youmed.vn/tin-tuc/trieu-chung-benh/"

def get_link_benh(link_web):
    response = requests.get(link_web)
    soup = BeautifulSoup(response.content, "html.parser")
    div = soup.findAll('div', {"class":"letter-section"})
    links = []
    for a in div:
        data = a.findAll('li')
        for i in data:
            link = i.find('a')
            links.append(link.attrs["href"])
    return links


thanhPhanBaiViet = {
#     "Tổng quan bệnh": ["bệnh lý là","bệnh là"],
    "Tổng quan bệnh": ["khái niệm","bệnh lý ... là","bệnh ... là","tổng quan","thông tin chung"],
    "Triệu chứng, biểu hiện bệnh": ["triệu chứng","biểu hiện","dấu hiệu","thường gặp","nhận biết","đặc điểm lâm sàng"],
    "Nguyên nhân gây bệnh": ["nguyên nhân","lây truyền", "thói quen gây hại","yếu tố tăng nguy cơ"],
    "Cách điều trị bệnh": ["điều trị","phương pháp","khắc phục"],
    "Cách phòng ngừa bệnh": ["phòng ngừa","phòng bệnh","nên","không nên","hạn chế","thói quen","duy trì","có thể áp dụng","bí quyết","biện pháp","cải thiện"],
    "Đối tượng mắc bệnh": ["đối tượng","đối tượng nguy cơ","những ai"],
    "Các biện pháp chẩn đoán": ["chẩn đoán","xét nghiệm"],
    "Biến chứng của bệnh": ["biến chứng"]
}

def timTieuDeNoiDung(soup):
    contents_body = soup.find("div", class_="content-body prose")
    contents = contents_body.findAll("h2")
    titles = []
    for item in contents:
        titles.append(item.text)

    return titles

def catNoiDungTag(soup):
    contents_body = soup.find("div", class_="content-body prose")
    contents = contents_body.findAll(["h2","h3","h4","h5","h6","li","p"])    
    noiDungTag = {"tieu_de": "", "noidung":"", "key":""}
    list_noidung = []
    count = 0
    list_tieude = timTieuDeNoiDung(soup)
    for i in contents:
        if (i.name == 'h2'):
            if(i.text in list_tieude):
                if(count != 0):
                    list_noidung.append(noiDungTag)
                    noiDungTag = {"tieu_de": "", "noidung":"", "key":""}
                noiDungTag["tieu_de"] = i.text
                noiDungTag["noidung"] = ""
                count += 1
        else:
            if(i.name == "p"):
                if(len(i.find_parents("li")) != 0):
                    continue
                else:
                    noiDungTag["noidung"] +=  i.text 
            else:
                noiDungTag["noidung"] +=  i.text 
    list_noidung.append(noiDungTag)
    return list_noidung












response = requests.get("https://youmed.vn/tin-tuc/buou-cuong-giap/")
soup = BeautifulSoup(response.content, "html.parser")

a = timTieuDeNoiDung(soup)
for i in a:
    print(i)