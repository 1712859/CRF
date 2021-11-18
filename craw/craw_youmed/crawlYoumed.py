import requests
import re
from bs4 import BeautifulSoup
from bs4.element import Comment
import string
import pickle
import math

from urllib.parse import urlparse
from requests import ReadTimeout, ConnectTimeout, HTTPError, Timeout, ConnectionError

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

def read_urltxt(path):
    Url_Benh = {}
    try:
        with open(path, 'r', encoding="utf-8") as f:
            data = f.read().strip()
            if len(data) == 0:
                return -1
            splits = data.split('\n')
            for url in splits:
                itemurl = url.split('|')
                if Url_Benh.get(itemurl[0]) == None and len(itemurl) == 2:
                    Url_Benh[itemurl[0]] = itemurl[1]
                elif Url_Benh.get(itemurl[0]) != None :
                    continue
            f.close()
        return Url_Benh
    except IOError:
        return -1

def timTieuDeNoiDung(soup,benh):
 
    tieuDes=[]
    content_header = soup.find("div", class_= "content-header")
    article_header = content_header.find("h1")
    tieuDes.append(article_header.text)
    contents = soup.findAll("ul", class_="toc_list")  
    for content in contents:
        for i in content.findAll('li'):
            if (tieuDes.count(i.text) == 0):
                tieuDes.append((i.text).strip())
  
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


def catNoiDungTag(soup):
    contents_body = soup.find("div", class_="content-body")
    contents = contents_body.findAll(["h2","h3","h4","h5","h6","p","li","span"])    
    noiDungTag = {}
    temp = 0
    taghtml = ["h2","h3","h4","h5","h6","p","li","span"]
    for i in contents:
        if (i.name == 'h2'):
            temp+=1
        if temp != 0:
            if noiDungTag.get(temp) == None:
                noiDungTag[temp] = [i]
            else:
                if(len(i.find_parents("li")) != 0):
                    continue
                else:
                    noiDungTag.get(temp).append(i)
        else:    
            continue
        if (i.findAll(["picture","noscript","figure","em"]) != []):
            continue
    return noiDungTag


def catNoiDungTagh3(listcontent):  
    noiDungTagh3 = {}
    temp = 0
    for i in listcontent:
        if (i.name == 'h3'):
            temp+=1
        if temp != 0:
            if noiDungTagh3.get(temp) == None:
                noiDungTagh3[temp] = [i]
            else:
                noiDungTagh3.get(temp).append(i)
        else:    
            continue
    return noiDungTagh3

def timNoiDung(url,benh):

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    ####
        

    
    tieuDeNoiDung = timTieuDeNoiDung(soup,benh)
    
    noiDungTag = catNoiDungTag(soup)  
    
    noiDungBaiViet={}
    
    taghtml = ["h2","h3","h4","h5","h6","p","li","span"]
    
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
        
        
        
    if noiDungBaiViet.get("Triệu chứng, biểu hiện bệnh") == None or len(noiDungBaiViet.get("Triệu chứng, biểu hiện bệnh")) ==0:
        vetTrieuChung = ["có các triệu chứng","có những triệu chứng","có triệu chứng","triệu chứng:","triệu chứng sau:","triệu chứng như:", "triệu chứng là","triệu chứng bệnh","dấu hiệu"]
        for num in noiDungTag.keys():
            dem=0
            tagh3 = catNoiDungTagh3(noiDungTag.get(num))
            
            if (len(tagh3) == 0):                
                for tag in noiDungTag.get(num):
                    for item in vetTrieuChung:
                        if (tag.text.lower()).find(item.lower()) != -1:
                            if (noiDungBaiViet.get("Triệu chứng, biểu hiện bệnh") == None):
                                noiDungBaiViet["Triệu chứng, biểu hiện bệnh"] = noiDungTag[num]
                                dem=1
                                break
                            else:
                                (noiDungBaiViet.get("Triệu chứng, biểu hiện bệnh")).extend(noiDungTag.get(num))
                                dem=1
                                break
                    if dem!=0:
                        break
            else:
                for numh3 in tagh3.keys():
                    for tag in tagh3.get(numh3):
                        for item in vetTrieuChung:
                            if (tag.text.lower()).find(item.lower()) != -1:
                                if (noiDungBaiViet.get("Triệu chứng, biểu hiện bệnh") == None):
                                    noiDungBaiViet["Triệu chứng, biểu hiện bệnh"] = tagh3[numh3]
                                    dem=1
                                    break
                                else:
                                    (noiDungBaiViet.get("Triệu chứng, biểu hiện bệnh")).extend(tagh3.get(numh3))
                                    dem=1
                                    break
                        if dem!=0:
                            break
    return noiDungBaiViet



def crawlUrls(root_url,path_urlsBenhtxt,path_TrieuChungBenh,path_UrlKhongTrieuChung):
    
    urls_benh_done = read_urltxt(path_urlsBenhtxt)
    urls_KhongTrieuChung = read_urltxt(path_UrlKhongTrieuChung)
    if urls_KhongTrieuChung == -1:
        f = open(path_UrlKhongTrieuChung,'w', encoding="utf-8")
        f.write('\n') 
        f.close()
        
    response = requests.get(root_url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    Benh_URL = {}
    contents = soup.findAll("div", class_="letter-section")
    for content in contents:
        for i in content.findAll('li'):
            url = str((i.find('a')).get('href'))
            tenbenh = str((i.text).strip())
            if Benh_URL.get(url) == None:
                if urls_benh_done == -1:
                    Benh_URL[url] = tenbenh
                elif (urls_benh_done != -1) and (urls_benh_done.get(url) == None):
                    Benh_URL[url] = tenbenh

                    print("Bệnh mới:",tenbenh," url:", url)
                else:
                    continue
            elif Benh_URL.get(url) != None :
                continue
    if len(Benh_URL) == 0:
        print("Đã crawl tất cả các bệnh!\n")
        return 1
    print("Benh_url", Benh_URL)

    for url in Benh_URL.keys():
        benh = Benh_URL.get(url)
        print("\n\n////////////////////////////////////////////////////////////////////////////////////////////////////////") 
        print("/////////////////////////////////////////////////////////////////////////////////////////////////////////") 
        print("Bài viết đề cập đến bệnh: ",benh)
        print("------------------------------------------------------------------------\n") 
        noiDung = timNoiDung(url,benh)
       
        
        if noiDung.get("Triệu chứng, biểu hiện bệnh") == None:
            print("Bệnh không có triệu chứng: ",benh,", url:",url)

            if urls_KhongTrieuChung == -1:
                f = open(path_UrlKhongTrieuChung,'a', encoding="utf-8")
                f.write(url+'|'+benh+'\n') 
                f.close()
            elif urls_KhongTrieuChung != -1 and urls_KhongTrieuChung.get(url) == None :
                f = open(path_UrlKhongTrieuChung,'a', encoding="utf-8")
                f.write(url+'|'+benh+'\n') 
                f.close()
            else:
                continue
   
        else:
            f = open(path_TrieuChungBenh,'a', encoding="utf-8")
            f.write("\n\n\n### "+benh+'\n')
            f.write("### "+url+'\n')
            for i in noiDung.get("Triệu chứng, biểu hiện bệnh"):
                if (i.name != "h2"):
                    print("\n",i.text)
                    f.write(i.text +'\n')
            f.close()
            
            f = open(path_urlsBenhtxt, "a", encoding="utf-8")
            f.write(url+'|'+benh+'\n')
            f.close()
        


root_url = 'https://youmed.vn/tin-tuc/trieu-chung-benh/'
path_urlsBenhtxt = 'D:/5_specialized_subjects_1/DoAnTotNghiep/6-7 xử lý đoạn văn bản/Benh_Url.txt'
path_TrieuChungBenh = 'D:/5_specialized_subjects_1/DoAnTotNghiep/6-7 xử lý đoạn văn bản/TrieuChungBenh.txt'

path_UrlKhongTrieuChung = 'D:/5_specialized_subjects_1/DoAnTotNghiep/6-7 xử lý đoạn văn bản/UrlKhongTrieuChung.txt'
urls_done = crawlUrls(root_url,path_urlsBenhtxt,path_TrieuChungBenh,path_UrlKhongTrieuChung)
