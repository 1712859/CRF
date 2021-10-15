import requests
from bs4 import BeautifulSoup

root_url = 'https://youmed.vn/tin-tuc/trieu-chung-benh/'
path_urlsBenhtxt = 'C:/Users/WIN10/Desktop/urlsBenh.txt'

def read_urltxt(path):
    urllink = {}
    try:
        with open(path, 'r') as f:
            data = f.read().strip()
            splits = data.split('\n')
            for url in splits:
                itemurl = url.split('|')
                if urllink.get(itemurl[1]) == None:
                    urllink[itemurl[1]] =itemurl[0]
                elif urllink.get(itemurl[1]) != None :
                    continue
            f.close()
        return urllink
    except IOError:
        return -1

def crawlTenBenh(root_url,path_urlsBenhtxt): 
    urls = read_urltxt(path_urlsBenhtxt)
    response = requests.get(root_url)
    soup = BeautifulSoup(response.content, "html.parser")
    Benh = []
    contents = soup.findAll("div", class_="letter-section")
    f = open("urlsBenh.txt", "a")
    for content in contents:
        for i in content.findAll('li'):
            s = str((i.find('a')).get('href'))
            if urls == -1:
                f.write('0'+'|'+ s +'\n') 
            elif (urls != -1) and (urls.get(s) == None):
                f.write('0'+'|'+ s +'\n') 
            if (Benh.count((i.text).strip().lower()) == 0) and ((i.text).strip() != "Back to top"):
                Benh.append((i.text).strip().lower())
    f.close()
    return Benh

Benh = crawlTenBenh(root_url,path_urlsBenhtxt)


thanhPhanBaiViet = {
    "Tổng quan bệnh": ["khái niệm","bệnh lý ... là","bệnh ... là"],
    "Triệu chứng, biểu hiện bệnh": ["triệu chứng","biểu hiện","dấu hiệu","biến chứng","thường gặp","nhận biết"],
    "Nguyên nhân gây bệnh": ["nguyên nhân","lây truyền", "thói quen gây hại","yếu tố tăng nguy cơ"],
    "Cách điều trị bệnh": ["điều trị","phương pháp","khắc phục"],
    "Cách phòng ngừa bệnh": ["phòng ngừa","phòng bệnh","nên","không nên","hạn chế","thói quen","duy trì","có thể áp dụng","bí quyết","biện pháp","cải thiện"],
    "Đối tượng mắc bệnh": ["đối tượng","đối tượng nguy cơ","những ai"],
    "Các biện pháp chẩn đoán": ["chẩn đoán","xét nghiệm"]    
}

def tieuDe(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser") 
    tieuDe=[]
    content_header = soup.find("div", class_= "content-header")
    article_header = content_header.find("h1")
    tieuDe.append(article_header.text)
    contents = soup.findAll("ul", class_="toc_list")  
    for content in contents:
        for i in content.findAll('li'):
            if (tieuDe.count(i.text) == 0):
                tieuDe.append((i.text).strip()) 
    return tieuDe

def timBenh(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.select(".article-header > h1")  
    content = soup.find("div", class_="content-body") 
    isBenh = -1
    tieuDeBaiViet = tieuDe(url)     
    for benh in Benh:
        for tieude in tieuDeBaiViet:
            if ((tieude.lower()).find(benh.lower()) != -1):
                isBenh = 1
                return benh

    if isBenh == -1:
        noiDung=""  
        texts = content.findAll("p")
        for text in texts:
            noiDung = noiDung + "\n" + text.text
        noiDung = noiDung + "\n"
        demTanXuat = {}
        for benh in Benh:
            if ((noiDung.lower()).find(benh.lower()) != -1):
                if demTanXuat.get(benh) == None:
                    demTanXuat[benh] = (noiDung.lower()).count(benh.lower())
                else:
                    demTanXuat[benh] = (noiDung.lower()).count(benh.lower())
        for benh in demTanXuat.keys():
            if demTanXuat.get(benh) == max(demTanXuat.values()):
                isBenh = 1
                return benh
        if isBenh == -1:
            print("Bài viết không đề cập đến tên bệnh")
            return -1

def timTieuDeNoiDung(url):
    tieuDes = tieuDe(url)
    tieuDeNoiDung = []    
    for key in thanhPhanBaiViet.keys():
        for item in thanhPhanBaiViet.get(key):
            for tieude in tieuDes:                
                if ((tieude.lower()).find(item.lower()) != -1):
                    if tieuDeNoiDung.count(key) == 0:
                        tieuDeNoiDung.append(key)
                elif (tieude.lower()).find(benh.lower() + " là") != -1:
                    if tieuDeNoiDung.count("Tổng quan bệnh") == 0:
                        tieuDeNoiDung.append("Tổng quan bệnh")
    return tieuDeNoiDung

def catNoiDungTag(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    contents_body = soup.find("div", class_="content-body")
    contents = contents_body.findAll(["h2","h3","h4","h5","h6","p","ul"])    
    noiDungTag = {}
    temp = 0
    for i in contents:
        if (i.findAll(["picture","noscript","figure","em"]) != []):
            continue
        if (i.name == 'h2'):
            temp+=1
        if temp != 0:
            if noiDungTag.get(temp) == None:
                noiDungTag[temp] = [i]
            else:
                noiDungTag.get(temp).append(i)
        else:    
            continue
    return noiDungTag

def timNoiDung(url):
    benh = timBenh(url)
    tieuDeNoiDung = timTieuDeNoiDung(url)   
    noiDungTag = catNoiDungTag(url)  
       
    noiDungBaiViet={}

    for num in noiDungTag.keys():
        for tag in noiDungTag.get(num):
            if (tag.name == "h2"):
                for key in tieuDeNoiDung:
                    for item in thanhPhanBaiViet.get(key):
                        if ((tag.text.lower()).find(item.lower()) != -1) :
                            if (noiDungBaiViet.get(key) == None):
                                noiDungBaiViet[key] = noiDungTag[num]
                                break
                            else:
                                (noiDungBaiViet.get(key)).extend(noiDungTag.get(num))
                                break
                        if ((tag.text).lower()).find(benh.lower() + " là") != -1:
                            if (noiDungBaiViet.get("Tổng quan bệnh") == None):
                                noiDungBaiViet["Tổng quan bệnh"] = noiDungTag[num]
                                break
                            else:
                                break
                break
    return noiDungBaiViet

def crawlUrls(root_url,path_urlsBenhtxt):
    Benh = crawlTenBenh(root_url,path_urlsBenhtxt)
    urls = read_urltxt(path_urlsBenhtxt)
    for url in urls:
        print(url)
        if urls.get(url) == '0':
            benh=timBenh(url)
            urls[url] = '1'
        elif urls.get(url) == '1':
            print("Đã đọc link rồi\n")
    f = open("urlsBenh.txt", "w")
    for url in urls:
        f.write(urls.get(url)+'|'+ url +'\n') 
    f.close()


urls_done = crawlUrls(root_url,path_urlsBenhtxt)