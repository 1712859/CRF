import pymongo


# myclient = pymongo.MongoClient("mongodb://localhost:27017/")

myclient = pymongo.MongoClient("mongodb+srv://admin:admin123@cluster.vfpxs.mongodb.net/HealthAssistant?retryWrites=true&w=majority")

mydb = myclient["HealthAssistant"]
mycol = mydb["Benh"]

file = open("ketqua.txt", mode='w', encoding="utf-8" )

data = {
  "rối loạn tiền đình": ["giảm khả năng chú ý","choáng váng","chóng mặt","giảm chú ý","giảm khả năng tập trung","hoa mắt", "khó tập trung","không thể bước đi","lo lắng quá mức","mất định hướng không gian","nhạy cảm với ánh sáng","nhìn mờ","quay cuồng", "rối loạn thị giác","rối loạn thính giác", "ù tai", "dễ ngã"],
  "bệnh lao phổi": ["chán ăn","đau ngực","đổ mồ hôi trộm","gầy sút","ho","ho có đờm","ho khan","ho ra máu","khó thở","mệt mỏi","ớn lạnh","sốt nhẹ"],
  "tê bì tay chân": ["chân bị mất cảm giác","chóng mặt","chuột rút ở tay chân","co giật","đau đầu dữ dội","đau mỏi cổ vai gáy","đau nhức âm ỉ bắp tay","dễ nhầm lẫn","hay quên","khó thở","mất kiểm soát bàng bàng quang","nóng bỏng tứ chi","tay chân mất cảm giác","tê /dị cảm mặt trong cánh tay","tê bì một bên","tê buốt lan dọc cánh tay","tê chân","tê kiểu châm chích","tê liệt","bị tê chân kéo dài"],
  "viêm đại tràng": ["buồn đại tiện liên tục","co thắt đại tràng","cứng bụng","đau","đau bụng","đau bụng quặn từng cơn","đau bụng từng lúc","đau dọc theo khung đại tràng","đau thắt bụng dưới","đau từng đoạn","đi ngoài phân lỏng có máu","gầy sút nhanh","mệt mỏi","bị táo bón","phân có màu như máu cá","phân khô","phân lẫn máu","phân lỏng","phân toàn nước","sốt","táo bón","tiêu chảy","tiêu lỏng"],
  "cường lách": ["bướu miệng","cảm giác no sớm","cảm thấy đầy hơi","chảy máu","đánh trống ngực","đau vùng hạ sườn trái","dễ bị bầm tím","hồi hộp","lách to","mệt mỏi","người yếu ớt","sốt cao","thiếu máu","xanh xao"],
  "chấn thương lách": ["chảy máu", "đau ở phần trên bên trái của bụng", "hoa mắt", "lẫn lộn", "ngất xỉu", "đau"],
  "cận thị": ["thường xuyên chảy nước mắt","chỉ nhìn gần được","dụi mắt","hình ảnh nhìn xa thấy bị mờ","mỏi mắt","nheo mắt khi nhìn xa"],
  "căng cơ quá mức": ["bầm tím","bị sưng tấy","đau","gân cơ bị yếu"],
  "crohn": ["chậm lớn","chậm phát triển","chuột rút","có máu trong phân","đau","đau bụng","giảm cân","giảm thèm ăn","kém ăn","lỗ rò","loét","loét miệng","mệt mỏi","nứt hậu môn","rối loạn dưỡng da","sốt","suy dinh dưỡng","tắc ruột","thiếu máu","tiêu chảy","tiêu chảy liên tục","trẻ chậm lớn","viêm da","viêm đường ống mật","viêm gan"],
  "cúm": ["đau cơ bắp", "đau đầu", "đau họng", "ho khan", "mệt mỏi", "nghẹt mũi", "ớn lạnh", "sốt", "sốt trên 38 độ C", "viêm họng"],
  
  "chốc mép": ["bọng nước lớn","chứa nhiều dịch","đau","đau nhẹ","mụn nước xuất hiện trên da","ngứa","vết loét sâu"],
  "bệnh giãn tĩnh mạch chi dưới": ["búi tĩnh mạch nổi rõ","cảm giác tức nặng hai chân","chuột rút","đau bắp chân","huyết khối tĩnh mạch sâu","loét da chân","phù chân","tê rần ở hai chi dưới","loét da chân","vọt bẻ", "viêm tĩnh mạch"],
  "viêm xoang": ["chảy nước mũi","đau nhức đầu vùng trán","giảm khả năng cảm nhận mùi","hắt hơi","ho","không ngửi thấy mùi","nặng mặt","nghẹt mũi","sổ mũi","sốt"],
  "áp xe": ["đau","cảm giác nóng","đau tức vùng hạ sườn phải","hốc hác","lưỡi bẩn","mệt mỏi","môi khô","ớn lạnh","rét run","sốt","sốt cao","sốt cao rét run","sưng nề","sưng nề vùng da xung quanh","suy kiệt","toàn thân mệt mỏi"],
  "uốn ván": ["bồn chồn","bí tiểu","cơ bị căng cứng","co giật","co thắt cơ hàm nhẹ","cứng hàm","đại tiện mất kiểm soát","đau cơ","đau đớn khắp toàn thân","gãy xương","khó chịu","khó nuốt","mặt bị nhăn","ngừng thở","nhức đầu","nóng rát khi đi tiểu","sốt"],
  "giời leo": ["khô mắt","chảy nước mũi","chóng mặt","da đau rát","giảm thính lực một bên tai","hoa mắt","mất vị giác phần trước lưỡi","mệt mỏi","ngứa râm ran","sốt nhẹ","ù tai","xuất hiện mụn nước","yếu một bên mắt"],
  "co thắt thực quản": ["ăn uống khó khăn","buồn nôn","cảm giác buồn nôn","đau","đau khi ăn","đau tức ngực khi nuốt","gây sụt","gây sụt cân","ho","hôi miệng","khó nuốt","nôn mửa","ợ hơi","ợ nóng","thở khò khè"],
  "chóng mặt kịch phát lành tính": ["buồn nôn","cảm giác chóng mặt","choáng","chóng mặt","đau ngực","đứng không vững","mất cân bằng","mắt mờ","mất thị giác","mất ý thức","nghe kém","ngứa","nhịp tim nhanh","nói chuyện khó khăn","ói mửa","sốt 38 độ c","tê","té ngã","yếu cánh tay"],
  "cường kinh": ["máu kinh ra nhiều","máu ra nhiều","rong kinh"],
  "cơ tim phì đại": ["mệt mỏi","đau ngực","Đột tử","trống ngực và ngất"],

  "cơ tim": ["khó thở","ho","phù chi dưới","mệt mỏi","rối loạn nhịp tim","tim đập bất thường","đau tức ngực","đánh trống ngực","đánh trống ngực","cảm thấy chèn ép ở ngực","chóng mặt","cảm thấy choáng váng","ngất xỉu","đột quỵ","hình thành cục máu đông ở tâm thất trái","đột tử","suy tim","rối loạn nhịp tim","ngừng tim","ngất xỉu"],
  "chấn thương sụn chêm": ["đầu gối đau","có tiếng “nổ” khi sụn chêm bị rách","đầu gối sưng dần lên","vận động khó khăn","cảm giác mất linh hoạt gối","khớp gối bị kẹt","cảm giác có tiếng lục cục trong khớp","gặp khó khăn trong đi lại","khó co duỗi khớp gối","Cảm thấy đau nhức","đau nhẹ","sưng khớp gối","đau ở khe khớp","đau","đau ở bề mặt khớp gối","không thể duỗi thẳng khớp gối","cứng khớp","đau khớp gối","sưng nhẹ khớp gối"],
  "down": ["mắt xếch","mặt dẹt","trông khờ khạo","mũi nhỏ","hình dáng tai bất thường","đầu ngắn","gáy rộng","cổ ngắn","vai tròn","miệng trề ra","lưỡi dày thè ra ngoài","tay ngắn","cơ quan sinh dục không phát triển","dây chằng yếu","thiểu năng trí tuệ"],
  "đái rắt": ["số lần đi tiểu nhiều","sốt","đau lưng","đau bên hông","nôn mửa","ớn lạnh","tăng cảm giác thèm ăn","mệt mỏi","nước tiểu có máu"],
  "đổ mồ hôi trộm": ["đổ mồ hôi vào ban đêm","run","ớn lạnh","sốt","sụt cân không nguyên nhân","khô âm đạo","nóng bừng ban ngày","ho","tiêu chảy","đau khu trú"],
  
  }

sum = 0
ad = []
bd = []
kq = []
for key in data.keys():
  print(key)
  file.writelines("###" + key + "\n")
  data_check = mycol.find_one({"ten_benh": key})
  a = len(data[key])
  b = 0
  trieuchung = data[key]
  for item in data_check["danh_sach_trieu_chung"]:
    if(item["trieu_chung"] in trieuchung):
      b = b + 1
      file.writelines(item["trieu_chung"]+" -"+"\n")
    else:
      file.writelines(item["trieu_chung"]+"\n")
  if (a == 0):
    a = 1
  ad.append(a)
  bd.append(b)
  sum = sum + b/a
for i in ad:
  print(i)
print("____________")
for i in bd:
  print(i)
print("Tổng kết: " + str(sum/25*100))