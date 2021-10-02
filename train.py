from vncorenlp import VnCoreNLP
annotator = VnCoreNLP(address="http://127.0.0.1", port=9001) 

# đường đẫn đến file rawdata (dữ liệu chưa tách từ)
# bắt buộc tạo file trước
file_data_raw ="C:\\Users\\WIN10\\Desktop\\data\\4\\rawdata.txt"

# đường đã đến file trả kết quả (gẫn đến thư mục của thuận toán CRF++-0.58)
file_out_khong_tag = "C:\\Users\\WIN10\\Desktop\\data\\4\\train1.data"

def themdauchamcau(ten_file):
    f = open(ten_file, 'r', encoding='UTF-8')
    du_lieu_input = f.readlines()
    data = []
    for a in du_lieu_input:
        int_ = len(a)
        b = ""
        if (int_ >2):
            if (a[int_-2] not in [".",";","!","?"]):
                b = a[:(int_-1)] + " ."
            else:
                b = a
        data.append(b)
    f.close
    with open(ten_file, mode='w', encoding="utf-8" ) as file:
        for b in data:
            file.writelines(b + "\n")

def tao_file_dư_lieu1(ten_file_du_lieu, ten_file_output):
    f = open(ten_file_du_lieu, 'r', encoding='UTF-8')
    du_lieu_input = f.read()
    doc = annotator.annotate(du_lieu_input) 
    with open(ten_file_output, mode='w', encoding="utf-8" ) as file:
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

themdauchamcau(file_data_raw)
tao_file_dư_lieu1(file_data_raw, file_out_khong_tag)



