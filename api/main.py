
from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
from vncorenlp import VnCoreNLP
# annotator = VnCoreNLP(address="http://127.0.0.1", port=9001) 
annotator =  VnCoreNLP("../vncorenlp/VnCoreNLP-1.1.jar", annotators="wseg,pos,ner,parse", max_heap_size='-Xmx2g') 
import os
import numpy as np
app = FastAPI()

# đường đã đến file trả kết quả (gẫn đến thư mục của thuận toán CRF++-0.58)
file_out_khong_tag = "test.data"
# đường đẫn từ thư mục của thuật toán CRF++-0.58 lưu file output.data
ten_file_du_lieu1 = "output.data"
# thư mục chưa code thuật toán crf
dir = "..\\CRF++-0.58\\"

class Item(BaseModel):
    noi_dung: str

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
    os.system("crf_test -m model1 test.data > output.data")

    data_benh = getTrieuChungBenh(dir + ten_file_du_lieu1 )
    if(len(data_benh) == 0):
        return {"message":"Không tìm thấy triệu chứng", "data": data_benh}
    return {"message":"Thành công", "data": data_benh}

