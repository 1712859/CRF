*tải code thuật toán crf

- truy cập link: https://drive.google.com/drive/folders/0B4y35FiV1wh7fngteFhHQUN2Y1B5eUJBNHZUemJYQV9VWlBUb3JlX0xBdWVZTWtSbVBneU0?resourcekey=0-NW5cPRv1Xr2-Vfo_xlDTLQ&usp=sharing
tải bản CRF++-0.58
- giải nén file CRF++-0.58

*tải code sử lý ngôn ngữ tự nhiên

- truy cập link: https://github.com/18520339/vietnamese-pos-tagging
Download tập tin CoreNLP.zip, giải nén
- tải java sjk 

- mở cmd chạy lệnh: 
	+ cd <dịa chỉ thư mục mới giải nén tập tin CoreNLP.zip>
	+ java -Xmx2g -jar VnCoreNLPServer.jar VnCoreNLP-1.1.jar -p 9001 -a "wseg,pos,parse"
- mở cmd thứ 2 chạy lệnh:
	+ pip install vncorenlp

các bước để trích xuất dữ liệu:
B1: tải tất cả nội dung cần train vào file rawdata.txt

B2: chạy code file train.py để tạo file train

B3: mở file train.data mới tạo và gắn thẻ cho từng từ

B4: chuyển file template, train.data bào thư mục CRF++-0.58 giải nén ở trên

B5: mở cmd và trỏ thư mục CRF++-0.58. chạy câu lệnh: crf_learn.exe template train.data model

B6: tạo file datatest.txt, copy nội dung văn bản cần trích xuất triệu chứng vào file datatest.txt

B7: chạy file test.py.

B8: mở cmd và trỏ thư mục CRF++-0.58. chạy câu lệnh: crf_test -m model test.data > output.data

B9: chạy file gettrieuchung.py

