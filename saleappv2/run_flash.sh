echo "---Cài thư viện---"
pip install -r requirements.txt

echo "---Tạo dữ liệu---"
python eapp/models.py

echo "---Chạy dữ liệu---"
python -m run flash eapp/index.py