<!-- install thư viện -->

pip install vncorenlp
pip install fastapi
pip install pydantic
pip install uvicorn

<!-- run code -->

Bước 1: chuyển đường dẫn dưới termial sang thử mục vncorenlp trong thử mục
Bước 2: chạy dòng lệnh: java -Xmx2g -jar VnCoreNLPServer.jar VnCoreNLP-1.1.jar -p 9001 -a "wseg,pos,parse"
Bước 3: Mở mộc terminal khác cd đến thư mục api trong thử mục
Bước 4: Chạy dong lệnh: uvicorn main:app --reload