
from asyncio.windows_events import NULL
from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel

from vncorenlp import VnCoreNLP
import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from typing import Optional
import pymongo

import spacy
nlp = spacy.load('vi_core_news_lg')

import nltk, string
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download('punkt') # if necessary...

import time
annotator = VnCoreNLP(address="http://127.0.0.1", port=9001) 
import os
import numpy as np
app = FastAPI()

# đường đã đến file trả kết quả (gẫn đến thư mục của thuận toán CRF++-0.58)
file_out_khong_tag = "test1.data"
# đường đẫn từ thư mục của thuật toán CRF++-0.58 lưu file output.data
ten_file_du_lieu1 = "output1.data"
# thư mục chưa code thuật toán crf
dir = "..\\CRF++-0.58\\"

class Item(BaseModel):
    noi_dung: str


# KNN
df = pd.read_csv('./data1.csv')
X_train = df.drop(columns='Labels')
X_train = X_train.drop(X_train.columns[np.isnan(X_train).any()], axis=1)
y_train = df.Labels
b = []
a = X_train.values
for a in X_train.values:
    b.append(a.astype("int")) 


neigh = KNeighborsClassifier(n_neighbors=5, metric='manhattan')
neigh.fit(X_train, y_train)
# KNN

# so sanh
stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

def stem_tokens(tokens):
    return [stemmer.stem(item) for item in tokens]

'''remove punctuation, lowercase, stem'''
def normalize(text):
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))

vectorizer = TfidfVectorizer(tokenizer=normalize)
 
def cosine_sim(text1, text2):
    tfidf = vectorizer.fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0,1]

def bo_stopword(a):
    temp =  nlp(a)
    out = ""
    count = 1
    for i in temp:
        if (i.is_stop == False):
            if(count == 1):
                out += i.text.replace("_", " ")
            else:
                out += " " + (i.text).replace("_", " ")
            count += 1
    return out
# so sanh


def themdauchamcau(list_):
        data = ""
        for a in list_:
            int_ = len(a)
            b = ""
            if (int_ >2):
                if (a[int_-1] != "\n"):
                    if (a[int_-1] not in [".",";","!","?"]):
                        b = a + ".\n" 
                    else:
                        b = a
                else:
                    if (a[int_-2] not in [".",";","!","?"]):
                        b = a[:(int_ -1)] + ".\n" 
                    else:
                        b = a
            data = data +"\n"+ b
        return data

def tao_file_du_lieu(data_input):
    doc = annotator.annotate(data_input) 
    with open(dir + file_out_khong_tag, mode='w', encoding="utf-8" ) as file:
            for cau in doc["sentences"]:
                for tu in cau:
                    tab = "\t"
                    if (len(tu["form"]) <= 15):
                        tab += "\t"
                    if (len(tu["form"]) <= 7):
                        tab += "\t"
                    if(tu["form"] in [".",";","!","?","\n"]):
                        file.writelines("\n")
                    elif(["form"] not in [")",">","/",":", ",", "\"","`","(","<","”","“"]):
                        file.writelines((tu["form"]).lower() + tab + tu["posTag"] + "\n")

def getTrieuChungBenh(ten_file_du_lieu):
    f = open(ten_file_du_lieu, 'r', encoding='UTF-8')
    du_lieu_input = f.readlines()
    output = []
    temp = {'trieu_chung':'','thoi_gian':''}
    count = 0
    count_TG = 0
    for a in du_lieu_input:
        row = a.split()
        rows = np.array(row)
        if (len(rows)==3):
            if (rows[2] in ["B-TC","B-TCTL"]):
                count +=1
            if (rows[2] == "B-TG"):
                count_TG +=1
            if (count <= 1):
                if(rows[2] in ["B-TC","I-TC","B-TCTL","I-TCTL"]):
                    temp["trieu_chung"] += rows[0].replace("_"," ") + " "
                if(rows[2] in ["B-TG","I-TG"]):
                    if( count_TG  >1 and rows[2] == "B-TG"):
                        temp["thoi_gian"] += ", " + rows[0].replace("_"," ") + " "
                    else:
                        temp["thoi_gian"] +=rows[0].replace("_"," ") + " "
            else:
                count = 1
                count_TG = 0
                output.append(temp)
                temp = {'trieu_chung': rows[0].replace("_"," ") + " ",'thoi_gian':''}
    output.append(temp)     
    return output            

@app.post("/chan_doan/")
async def root(item: Item):
    du_lieu_input = item.noi_dung
    if (du_lieu_input == ""):
        
        raise HTTPException(status_code=400, detail="Dữ liệu truyền lên rỗng")
    
    

    du_lieu_input = du_lieu_input.split("\n")

    data_out = themdauchamcau(du_lieu_input)

    # tạo file dữ liệu test.data
    tao_file_du_lieu(data_out)

    os.chdir(dir)
    os.system("crf_test -m model1 test1.data > output1.data")

    data_benh = getTrieuChungBenh(dir + ten_file_du_lieu1 )

    if(len(data_benh) == 0):
        return {"message":"Không tìm thấy triệu chứng", "data": [] }
    else:
        row = []
        for a in data_benh:
            row.append((a["trieu_chung"]).strip())
        for i in row:
            if(i == ""):
                row .remove(i)
        X_input = np.array([1 if col in row else 0 for col in X_train.columns.to_list()]).reshape(1, -1)
        pred = []
        pred.append(y_train[neigh.kneighbors(X_input, return_distance=False)[0]])
        output = []
        for key in pred[0].items():
            print(key)

        for key, value in pred[0].items():
            output.append(value)

        myclient = pymongo.MongoClient("mongodb+srv://admin:admin123@cluster.vfpxs.mongodb.net/HealthAssistant?retryWrites=true&w=majority")
        mydb = myclient["HealthAssistant"]

        mycol = mydb["CRF_input"]

        CRF_input = {
            "noi_dung": item.noi_dung,
            "ket qua": output,
            "trieu_chung": row,
            "status": 1
        }
        resporn_benh = mycol.insert_one(CRF_input)

        return {"message":"Thành công", "data": output  }
    


@app.post("/crf_get_trieu_chung/")
async def root(item: Item):
    du_lieu_input = item.noi_dung
    if (du_lieu_input == ""):
        
        raise HTTPException(status_code=400, detail="Dữ liệu truyền lên rỗng")
    du_lieu_input = du_lieu_input.split("\n")

    data_out = themdauchamcau(du_lieu_input)

    # tạo file dữ liệu test.data
    tao_file_du_lieu(data_out)

    os.chdir(dir)
    os.system("crf_test -m model1 test1.data > output1.data")

    data_benh = getTrieuChungBenh(dir + ten_file_du_lieu1 )

    if(len(data_benh) == 0):
        return {"message":"Không tìm thấy triệu chứng"}
    return {"message":"Thành công", "data": data_benh}

@app.post("/knn_get_ill/")
async def root(item: Item):
    du_lieu_input = []
    du_lieu_input = item.noi_dung
    
    print(item.noi_dung)
    row = du_lieu_input.split(", ")
    for i in row:
        if(i == ""):
            row .remove(i)
    X_input = np.array([1 if col in row else 0 for col in X_train.columns.to_list()]).reshape(1, -1)
    pred = []
    pred.append(y_train[neigh.kneighbors(X_input, return_distance=False)[0]])
    output = []
    for key in pred[0].items():
        print(key)

    for key, value in pred[0].items():
        output.append(value)

    return {"message":"Thành công", "data": output  }

@app.get("/sosanh/")
async def root(noidung1: Optional[str] = None, noidung2: Optional[str] = None):
    noidung1 = bo_stopword(noidung1.lower())
    data = noidung2.split(" , ")
    max = 0
    out = ""
    for i in data:
        if(len(i) > 1):
            a = cosine_sim(noidung1,bo_stopword(i.lower()))
            if(max < a):
                max = a
                out = i
    return {"phan_tram" : round(max, 3), "content": out }

@app.get("/stopword/")
async def root(content: Optional[str] = None):
    print(content)
    noidung1 = bo_stopword(content.lower())
    return {"content": noidung1  }