# Dockerfile cho Mekong Mobile Smart CRM - Kho dữ liệu bán hàng & Dashboard (Luồng L6 - Track DA)
# Sinh viên: Mai Tuấn Kiệt - MSSV: 2374802010259
FROM python:3.11-slim

WORKDIR /app

# Cài đặt các gói phụ thuộc hệ thống tối thiểu (curl phục vụ container healthcheck)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Cài đặt các thư viện Python từ tệp khóa phiên bản
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn dự án
COPY . .

# Chạy kiểm thử tự động và nạp dữ liệu ETL trước khi khởi động ứng dụng
RUN pytest -v && python run_pipeline.py

# Cổng Streamlit mặc định
EXPOSE 8501

# Healthcheck xác thực Streamlit và kho dữ liệu vận hành tốt
HEALTHCHECK --interval=20s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Lệnh khởi chạy Dashboard phân tích bán hàng
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
