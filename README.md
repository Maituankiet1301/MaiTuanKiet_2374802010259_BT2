# Smart CRM Mekong Mobile – Luồng L6: Kho Dữ Liệu Bán Hàng & Báo Cáo Doanh Thu (Bài Tập 2)

**Học phần:** Chuyên đề tốt nghiệp 1 – Học kỳ 1, Năm học 2026 – 2027  
**Sinh viên thực hiện:** Mai Tuấn Kiệt  
**MSSV:** 2374802010259  
**Track:** Data Analytics (DA)  
**Luồng nghiệp vụ:** L6 – Kho dữ liệu bán hàng và báo cáo doanh thu  
**Giảng viên phụ trách:** TS. Nguyễn Trí Hải / ThS. Nguyễn Minh Tân / ThS. Trần Công Thanh  
**Git Tag nộp bài:** `v0.2`  
**GitHub Repository:** [https://github.com/Maituankiet1301/MaiTuanKiet_2374802010259_BT2](https://github.com/Maituankiet1301/MaiTuanKiet_2374802010259_BT2)

---

## 1. Mô tả hệ thống (3–5 câu)
Hệ thống hiện thực hóa trọn vẹn luồng phân tích dữ liệu bán hàng Luồng L6 cho chuỗi 24 chi nhánh Mekong Mobile theo mô hình kho dữ liệu hình sao (Star Schema). Pipeline ETL tự động trích xuất các tệp CSV thô, thực thi 6 hàm kiểm tra chất lượng dữ liệu trả về số lượng và tỷ lệ lỗi, đồng thời cách ly các bản ghi vi phạm vào bảng reject. Dữ liệu sạch được nạp vào kho DuckDB với cơ chế Idempotent chống nhân đôi dữ liệu khi nạp lại nhiều lần. Cuối cùng, giao diện Dashboard Streamlit trực quan hóa các chỉ số doanh thu (CH1), cảnh báo chi nhánh sụt giảm 3 tháng liên tiếp (CH2), phân tích cơ cấu danh mục sản phẩm (CH4) và xử lý đầy đủ cả 3 trạng thái: Đang tải, Rỗng và Lỗi kết nối.

---

## 2. Yêu cầu môi trường
- **Hệ điều hành:** Windows 10/11, macOS, hoặc Linux.
- **Python Runtime:** Phiên bản Python 3.11 trở lên (`python >= 3.11`).
- **Cơ sở dữ liệu:** DuckDB (engine nhúng không cần cài đặt daemon server).
- **Trình duyệt web:** Google Chrome, Microsoft Edge, hoặc Firefox để xem Dashboard.

---

## 3. Cài đặt và Khởi chạy (Mỗi bước một lệnh cụ thể)

### Bước 1: Clone repo và di chuyển vào thư mục dự án
```bash
git clone https://github.com/Maituankiet1301/MaiTuanKiet_2374802010259_BT2.git
cd MaiTuanKiet_2374802010259_BT2
```

### Bước 2: Tạo và kích hoạt môi trường ảo (Khuyến nghị)
- Trên Windows PowerShell:
  ```powershell
  python -m venv .venv
  .venv\Scripts\activate
  ```
- Trên Linux / macOS:
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### Bước 3: Cài đặt các thư viện theo tệp khóa phiên bản
```bash
pip install -r requirements.txt
```

### Bước 4: Chạy Pipeline ETL nạp kho dữ liệu DuckDB (1 lệnh duy nhất)
```bash
python run_pipeline.py
```
*(Hệ thống sẽ tự động quét dữ liệu mẫu tại `data/raw/` hoặc `seeds/`, thực thi kiểm tra chất lượng, nạp các bảng Dimension, Fact và Rejects vào `data/dwh_mekong.duckdb`)*

### Bước 5: Khởi chạy Dashboard Báo cáo Doanh thu Streamlit
```bash
streamlit run app.py
```
*(Mở trình duyệt tại địa chỉ: `http://localhost:8501` để xem giao diện)*

### Bước 6: Đăng nhập vào Dashboard
Hệ thống yêu cầu xác thực trước khi xem báo cáo. Sử dụng một trong các tài khoản demo sau:

| Tên đăng nhập | Mật khẩu | Vai trò | Phạm vi xem |
|---|---|---|---|
| `admin` | `admin123` | Giám đốc kinh doanh | Toàn bộ 24 chi nhánh |
| `manager1` | `manager123` | Quản lý cửa hàng | Cửa hàng CH01 |
| `dataeng` | `data123` | Kỹ sư dữ liệu | Toàn bộ hệ thống + ETL |

---

## 4. Lệnh chạy bộ kiểm thử tự động (Test Suite)
Chạy toàn bộ 4 trường hợp kiểm thử (Luồng đúng, Giá trị biên, Dữ liệu sai, và Tính Idempotent) bằng **MỘT LỆNH DUY NHẤT**:
```bash
pytest -v
```
**Kết quả kỳ vọng:** 100% test cases **PASSED** trong dưới 2 giây.

---

## 5. Cách kiểm tra hệ thống đã chạy đúng (Checklist chấm điểm của Giảng viên)

### A. Kiểm tra tính Idempotent (Chống nhân đôi dữ liệu khi nạp lại)
Chạy pipeline lần 1 và lần 2 liên tiếp:
```bash
python run_pipeline.py
python run_pipeline.py
```
**Kết quả xác nhận:** Số dòng trong bảng `fact_sales` ở cả 2 lần đều **bằng đúng 3.144 dòng** (không bị tăng lên gấp đôi).

### B. Kiểm tra Báo cáo Chất lượng & Bảng Reject
Sau khi chạy pipeline, mở terminal hoặc DuckDB CLI kiểm tra bảng reject:
- `reject_orders`: chứa 5 đơn hàng vi phạm (lỗi ngày tháng không hợp lệ `31/02/2025`, lỗi chuỗi tiền tệ hỏng, mã cửa hàng lạ `CH99`).
- `reject_order_items`: chứa 1 dòng mặt hàng có thành tiền sai lệch vượt quá ngưỡng cho phép 1 VNĐ.

### C. Kiểm tra 3 trạng thái trên giao diện Dashboard (Streamlit)
Mở ứng dụng `app.py`, trên thanh bên (Sidebar) có 2 công tắc phục vụ kiểm thử nhanh:
1. **Trạng thái Đang tải (Loading):** Mỗi khi bấm thay đổi bộ lọc, spinner *"⏳ Đang thực thi truy vấn..."* hiển thị rõ ràng.
2. **Trạng thái Dữ liệu rỗng (Empty State):**
   - Tích chọn checkbox: *"🟡 Giả lập Bộ lọc rỗng"* $\rightarrow$ Giao diện hiển thị hộp thông báo vàng: *"🔍 Không tìm thấy dữ liệu giao dịch phù hợp với bộ lọc"* kèm các thông tin chi tiết và nút Đặt lại bộ lọc.
3. **Trạng thái Lỗi kết nối CSDL (Error State):**
   - Tích chọn checkbox: *"🔴 Giả lập Lỗi kết nối CSDL"* $\rightarrow$ Giao diện hiển thị cảnh báo đỏ thân thiện: *"⚠️ Lỗi kết nối cơ sở dữ liệu kho phân tích"*, chuỗi kết nối và mật khẩu được ẩn hoàn toàn (NFR3), kèm nút *"🔄 Thử kết nối lại ngay"*.

---

## 6. Khởi chạy bằng Docker (Mức đánh giá cao)
Nếu máy đã cài Docker và Docker Compose, toàn bộ hệ thống có thể khởi chạy bằng **2 câu lệnh**:
```bash
docker-compose build
docker-compose up -d
```
Truy cập Dashboard tại `http://localhost:8501`.

---

## 7. Cấu trúc Thư mục Dự án
```text
.
├── app.py                         # Entrypoint Dashboard Streamlit (Xử lý 3 trạng thái + Login NFR3)
├── run_pipeline.py                # Entrypoint chạy Pipeline ETL 1 lệnh duy nhất
├── requirements.txt               # Danh mục thư viện có khóa phiên bản cố định (==)
├── Dockerfile                     # Đóng gói Docker container
├── docker-compose.yml             # Khởi chạy toàn bộ hệ thống bằng Docker Compose
├── .env.example                   # Biến môi trường mẫu
├── .gitignore                     # Loại trừ file tạm, cache, .env và file CSDL lớn
├── README.md                      # Tài liệu hướng dẫn cài đặt và kiểm thử
├── BT2_2374802010259_MaiTuanKiet.pdf # File PDF báo cáo chính thức nộp bài BT2
├── ho_so_bt1/                     # Toàn bộ hồ sơ tài liệu và báo cáo Bài tập 1 (BT1)
│   ├── BT1_DA_L6_2374802010259_MaiTuanKiet.pdf
│   ├── HO_SO_BT1_HOAN_CHINH.md
│   ├── HO_SO_BT1_HOAN_CHINH.html
│   ├── build_bt1_pdf.ps1
│   ├── BAO_CAO_BUOI_4.md
│   └── BAO_CAO_BUOI_5.md
├── ho_so_bt2/                     # Toàn bộ hồ sơ tài liệu và báo cáo Bài tập 2 (BT2)
│   ├── BT2_2374802010259_MaiTuanKiet.pdf
│   ├── HO_SO_BT2_HOAN_CHINH.md
│   ├── HO_SO_BT2_HOAN_CHINH.html
│   └── build_bt2_pdf.ps1
├── data/
│   ├── raw/                       # Dữ liệu CSV thô nguồn của 24 cửa hàng
│   └── dwh_mekong.duckdb          # Kho dữ liệu DuckDB Star Schema
├── seeds/                         # Dữ liệu hạt giống khởi tạo (stores, products, orders, items)
│   └── generate_seeds.py          # Script sinh dữ liệu mẫu giả lập
├── sql/
│   └── schema.sql                 # Script DDL tạo các bảng Dimension, Fact, Reject, Audit
├── src/                           # Mã nguồn tách lớp chuẩn theo Track DA
│   ├── extract/                   # Pha 1: Trích xuất dữ liệu từ các file CSV
│   │   └── extractor.py
│   ├── quality/                   # Pha kiểm soát chất lượng dữ liệu (6 hàm đo lường)
│   │   └── checker.py
│   ├── transform/                 # Pha 2: Làm sạch, chuẩn hóa ngày ISO, che SĐT, gắn mã Dim/Fact
│   │   └── transformer.py
│   ├── load/                      # Pha 3: Nạp dữ liệu vào DuckDB với cơ chế Idempotent
│   │   └── loader.py
│   ├── pipeline.py                # Bộ điều phối Pipeline (Orchestrator)
│   └── dashboard/
│       └── app.py
├── tests/                         # Bộ kiểm thử tự động pytest
│   └── test_pipeline.py           # 4 test cases: Luồng đúng, Biên, Dữ liệu sai, Idempotent
└── docs/                          # Hồ sơ đặc tả và sơ đồ thiết kế
    ├── srs.md                     # Đặc tả yêu cầu phần mềm từ BT1
    ├── data-requirements.md       # Đặc tả dữ liệu chuyên ngành DA
    ├── thay-doi-thiet-ke.md       # Bản ghi nhận 3 thay đổi thiết kế so với BT1
    ├── ai-disclosure.md           # Bảng khai báo công cụ AI và cam kết học thuật (BT2)
    ├── architecture-thuc-te.md     # Sơ đồ kiến trúc đã hiện thực thực tế
    ├── architecture-thuc-te.drawio # File thiết kế Draw.io gốc
    ├── usecase-specification.md   # Đặc tả chi tiết 6 use case và ranh giới hệ thống
    ├── usecase.drawio             # Sơ đồ Use Case chuẩn UML
    ├── erd.drawio                 # Sơ đồ ERD Star Schema
    └── wireframe.drawio           # Sơ đồ Wireframe Dashboard
```
