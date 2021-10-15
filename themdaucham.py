# đường đẫn đến file rawdata
file_data_raw ="C:\\Users\\WIN10\\Desktop\\crf\\rawdata.txt"

def themdauchamcau(ten_file):
    f = open(ten_file, 'r', encoding='UTF-8')
    du_lieu_input = f.readlines()
    data = []
    for a in du_lieu_input:
        int_ = len(a)
        b = ""
        if (int_ >2):
            if (a[int_-2] not in [".",";","!","?"]):
                b = a[:(int_-1)] + " . "
            else:
                b = a
        data.append(b)
    f.close
    with open(ten_file, mode='w', encoding="utf-8" ) as file:
        for b in data:
            file.writelines(b + "\n")


themdauchamcau(file_data_raw)