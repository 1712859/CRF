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

<!-- chạy code  -->
<!-- trong thư mục đã có đủ hết các file cần tải ở trên -->

<!-- install thư viện -->
Thư viện cần tải

pip install vncorenlp
pip install fastapi
pip install pydantic
pip install uvicorn
pip install requests
pip install bs4
pip install json

<!-- run code -->
Các bước chạy server để chạy code

Bước 1: chuyển đường dẫn dưới termial sang thử mục vncorenlp trong thử mục
Bước 2: chạy dòng lệnh: java -Xmx2g -jar VnCoreNLPServer.jar VnCoreNLP-1.1.jar -p 9001 -a "wseg,pos,parse"
Bước 3: Mở mộc terminal khác cd đến thư mục api trong thử mục
Bước 4: Chạy dong lệnh: uvicorn main:app --reload

<!-- train dữ liệu bằng -->

<!-- test dữ liệu -->

