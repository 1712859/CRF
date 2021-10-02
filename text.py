from vncorenlp import VnCoreNLP
annotator = VnCoreNLP(address="http://127.0.0.1", port=9001) 
# đường đẫn đến file rawdata dữ liệu cần test (dữ liệu chưa tách từ)
# bắt buộc tạo file trước
file_data_raw ="C:\\Users\\WIN10\\Desktop\\rawdata.txt"
# đường đã đến file trả kết quả (gẫn đến thư mục của thuận toán CRF++-0.58)
file_out_khong_tag1 = "C:\\Users\\WIN10\\Desktop\\CRF++-0.58\\test.data"

def tao_file_dư_lieu3(ten_file_du_lieu, ten_file_output):
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

tao_file_dư_lieu3(file_data_raw, file_out_khong_tag1)