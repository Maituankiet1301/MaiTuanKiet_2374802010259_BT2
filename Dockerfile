# Dockerfile cho Mekong Mobile Smart CRM - Kho dữ liệu bán hàng & Dashboard (Luồng L6)
FROM python:3.11-slim

WORKDIR /app

# Cài đặt các gói phụ thuộc hệ thống tối thiểu
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Sao chép và cài đặt thư viện Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn dự án
COPY . .

# Chạy kiểm thử tự động và nạp dữ liệu ETL trước khi khởi động ứng dụng
RUN pytest -v && python run_pipeline.py

# Cổng Streamlit mặc định
EXPOSE 8501

# Lệnh khởi chạy Dashboard
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
