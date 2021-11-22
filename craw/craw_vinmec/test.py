    
def sosanh(a,b):
    if(a["trieu_chung"] == b["trieu_chung"]):
        if(a["thoi_gian"] == b["thoi_gian"]):
            return 1
        else:
            return 2
    return 3

data = [
    {
      "trieu_chung": "đau",
      "thoi_gian": ""
    },
    {
      "trieu_chung": "đau",
      "thoi_gian": ""
    },
    {
      "trieu_chung": "nhức mỏi",
      "thoi_gian": ""
    },
    {
      "trieu_chung": "tê vùng bị tổn thương",
      "thoi_gian": ""
    },
    {
      "trieu_chung": "khó chịu",
      "thoi_gian": ""
    },
    {
      "trieu_chung": "da xanh nhợt nhạt",
      "thoi_gian": ""
    },
    {
      "trieu_chung": "lạnh da",
      "thoi_gian": ""
    },
    {
      "trieu_chung": "đau chân",
      "thoi_gian": "khi nghỉ ngơi "
    },
    {
      "trieu_chung": "đau rút ở vùng hông",
      "thoi_gian": ""
    },
    {
      "trieu_chung": "chân bị tê",
      "thoi_gian": ""
    },
    {
      "trieu_chung": "yếu",
      "thoi_gian": "khi so sánh với chân khác "
    },
    {
      "trieu_chung": "da xanh nhợt nhạt",
      "thoi_gian": ""
    },
    {
      "trieu_chung": "lạnh da",
      "thoi_gian": ""
    },
    {
      "trieu_chung": "móng chân chậm phát triển",
      "thoi_gian": ""
    },
    {
      "trieu_chung": "rối loạn cương dương",
      "thoi_gian": "khi đang nghỉ "
    },
    {
      "trieu_chung": "đau",
      "thoi_gian": ""
    },
    {
      "trieu_chung": "tê chân",
      "thoi_gian": ""
    },
    {
      "trieu_chung": "thiếu máu cục bộ chi",
      "thoi_gian": ""
    },
    {
      "trieu_chung": "nhiễm trùng tay hay chân",
      "thoi_gian": ""
    },
    {
      "trieu_chung": "thiếu máu",
      "thoi_gian": "khi bị thương "
    },
    {
      "trieu_chung": "đau tim",
      "thoi_gian": ""
    }
  ]

data_final = []
for item in data:
    if(len(data_final) == 0):
        data_final.append(item)
    else:
        check = True
        for a in data_final: 
            if(sosanh(a,item) == 3):
                check = False
                
            elif(sosanh(a,item) == 2):
                item["thoi_gian"] = item["thoi_gian"] + " , " + a["thoi_gian"]
                check = False
            else:
                check = True
                break
        if(check == False):
            data_final.append(item)
for i in data_final:
    print(i)