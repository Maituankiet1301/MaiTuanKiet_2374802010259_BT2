# Smart CRM Mekong Mobile – Luồng L6: Kho Dữ Liệu Bán Hàng & Báo Cáo Doanh Thu (Bài Tập 3)

**Học phần:** Chuyên đề tốt nghiệp 1 – Học kỳ 1, Năm học 2026 – 2027  
**Sinh viên thực hiện:** Mai Tuấn Kiệt  
**MSSV:** 2374802010259  
**Track:** Data Analytics (DA)  
**Luồng nghiệp vụ:** L6 – Kho dữ liệu bán hàng và báo cáo doanh thu  
**Giảng viên phụ trách:** TS. Nguyễn Trí Hải / ThS. Nguyễn Minh Tân / ThS. Trần Công Thanh  
**Git Tag chính thức:** `v1.0`  
**GitHub Repository (PUBLIC):** [https://github.com/Maituankiet1301/MaiTuanKiet_2374802010259_BT2](https://github.com/Maituankiet1301/MaiTuanKiet_2374802010259_BT2)  
**Tệp báo cáo PDF duy nhất:** `BT3_2374802010259_MaiTuanKiet.pdf`

---

## ⚡ KHỞI CHẠY HỆ THỐNG BẰNG 2 LỆNH DUY NHẤT (TIÊU CHÍ C1 CỐT LÕI)

Từ thư mục dự án (hoặc sau khi clone tag `v1.0`), khởi chạy toàn bộ hệ thống bằng **đúng 2 câu lệnh**:

```bash
cp .env.example .env
docker compose up -d --build
```

*(Sau khi chạy 2 lệnh trên: Docker container tự động chạy kiểm thử `pytest -v`, nạp kho dữ liệu DuckDB `python run_pipeline.py`, khởi động Dashboard tại `http://localhost:8501` và tự động đạt trạng thái `healthy`).*

> **Phương án khởi chạy Native Python (Nếu máy chưa cài Docker):**
> ```bash
> python run_pipeline.py
> streamlit run app.py
> ```

---

## 1. Mô tả hệ thống (3–5 câu)
Hệ thống hiện thực hóa trọn vẹn luồng phân tích dữ liệu bán hàng Luồng L6 cho chuỗi 24 chi nhánh Mekong Mobile theo mô hình kho dữ liệu hình sao (Star Schema). Pipeline ETL tự động trích xuất các tệp CSV thô, thực thi 6 hàm kiểm tra chất lượng dữ liệu trả về số lượng và tỷ lệ lỗi, đồng thời cách ly các bản ghi vi phạm vào bảng reject (`reject_orders`, `reject_order_items`). Dữ liệu sạch được nạp vào kho DuckDB với cơ chế Idempotent chống nhân đôi dữ liệu khi nạp lại nhiều lần (3.144 dòng). Cuối cùng, giao diện Dashboard Streamlit trực quan hóa các chỉ số doanh thu (CH1), cảnh báo chi nhánh sụt giảm 3 tháng liên tiếp (CH2), phân tích cơ cấu danh mục sản phẩm (CH4) và xử lý đầy đủ cả 3 trạng thái: Đang tải, Rỗng và Lỗi kết nối.

---

## 2. Sáu thành phần bắt buộc của Bài tập 3 (Tag `v1.0`)

| Thành phần | Tên tài liệu / Mã nguồn | Mô tả chi tiết & Vị trí |
|:---|:---|:---|
| **TP1 – Test Plan rút gọn** | [`docs/test-plan.md`](docs/test-plan.md) | Kế hoạch kiểm thử rút gọn 4 mục: Phạm vi & ngoài phạm vi, Tầng kiểm thử & kỹ thuật chọn dữ liệu (biên, phân vùng), Tiêu chí thành công đo được, Môi trường & dữ liệu thử. |
| **TP2 – Test Report** | [`docs/test-report.md`](docs/test-report.md) | Báo cáo 12 test cases đủ 8 cột chuẩn, bao phủ trọn vẹn 5 loại kiểm thử Track DA, **100% chạy thật** và có ảnh chụp terminal tại [`docs/screenshots/`](docs/screenshots/). |
| **TP3 – Bug Log** | [`docs/bug-log.md`](docs/bug-log.md) | Nhật ký theo dõi 5 bug thực tế (1 Critical, 4 Major), mỗi bug đủ 7 dòng chuẩn, có link commit mở được trực tiếp trên GitHub. |
| **TP4 – Gói đóng gói** | [`Dockerfile`](Dockerfile) & [`docker-compose.yml`](docker-compose.yml) | Đóng gói tái lập được bằng $\le 2$ lệnh từ thư mục trống, tích hợp sẵn Healthcheck tự động và dữ liệu mẫu đầy đủ. |
| **TP5 – Deployment Guide & Checklist bảo mật** | [`docs/deployment-guide.md`](docs/deployment-guide.md) & [`docs/checklist-bao-mat.md`](docs/checklist-bao-mat.md) | Deployment Guide tiếng Anh 5 mục chuẩn (Requirements, Setup, Env, Data, Verify) + Hướng dẫn Cloud; Checklist bảo mật 7 mục theo OWASP Top 10:2025. |
| **TP6 – Tài liệu kỹ thuật tiếng Anh (Track DA)** | [`docs/pipeline-doc.md`](docs/pipeline-doc.md) & [`docs/data-dictionary.md`](docs/data-dictionary.md) | Tài liệu kỹ thuật Pipeline 6 mục (có mục hạn chế nêu ảnh hưởng nghiệp vụ) và Từ điển dữ liệu Data Dictionary mô tả 100% cột của toàn bộ 8 bảng DuckDB. |

---

## 3. Lệnh chạy bộ kiểm thử tự động (Test Suite - 12 Test Cases)

Bộ kiểm thử tự động được cấu hình qua `pytest.ini` (`pythonpath = .`), bao phủ trọn vẹn **12 Test Cases thuộc đủ 5 loại kiểm thử bắt buộc cho Track DA**:
- **Loại 1:** Luồng đúng (TC-01, TC-02)
- **Loại 2:** Giá trị biên 2 phía (TC-03, TC-04)
- **Loại 3:** Dữ liệu sai cách ly an toàn (TC-05, TC-06, TC-07)
- **Loại 4:** Bảo mật & Chất lượng dữ liệu (TC-08 che PII NFR3, TC-09 đo 3 chiều, TC-10 chống SQL injection)
- **Loại 5:** Tính tái lập Idempotent & Chịu lỗi (TC-11 nạp 2 lần không nhân đôi, TC-12 tệp rỗng 0 bytes)

Chạy toàn bộ 12 ca kiểm thử bằng **MỘT LỆNH DUY NHẤT**:
```bash
pytest -v
```
Hoặc chạy gọn:
```bash
pytest -q
```
**Kết quả thực tế:** **100% test cases PASSED (12/12 passed trong ~1.6 giây)**.

---

## 4. Cách kiểm tra hệ thống đã chạy đúng (Dành cho Giảng viên nghiệm thu)

### A. Kiểm tra tính Idempotent (Tiêu chí C8 - Chống nhân đôi dữ liệu khi nạp lại)
Chạy pipeline lần 1 và lần 2 liên tiếp:
```bash
python run_pipeline.py
python run_pipeline.py
```
**Kết quả xác nhận:** Số dòng trong bảng `fact_sales` ở cả 2 lần đều **bằng đúng 3.144 dòng** (độ lệch = 0 dòng).

### B. Kiểm tra Báo cáo Chất lượng & Bảng Reject
Sau khi chạy pipeline, kiểm tra các bảng cách ly lỗi trong DuckDB:
- `reject_orders`: chứa đúng 5 đơn hàng vi phạm (3 đơn sai ngày `INVALID_DATE_FORMAT`, 1 đơn chuỗi tiền hỏng `CORRUPTED_CURRENCY_STRING`, 1 đơn mã cửa hàng lạ `UNKNOWN_STORE_ID`).
- `reject_order_items`: chứa đúng 1 dòng mặt hàng có sai lệch thành tiền vượt quá 1 VNĐ (`INCONSISTENT_LINE_TOTAL`).

### C. Đăng nhập Dashboard & Kiểm tra 3 trạng thái UX (Streamlit)
Mở trình duyệt tại `http://localhost:8501`. Đăng nhập bằng các tài khoản demo:
- `admin` / `admin123` (Giám đốc kinh doanh - xem 24 chi nhánh)
- `manager1` / `manager123` (Quản lý chi nhánh - chỉ xem CH01)
- `dataeng` / `data123` (Kỹ sư dữ liệu - xem báo cáo kiểm toán ETL)

Kiểm tra 3 trạng thái UX trên giao diện:
1. **Trạng thái Đang tải (Loading):** Spinner hiển thị khi thay đổi bộ lọc.
2. **Trạng thái Dữ liệu rỗng (Empty State):** Tích chọn `🟡 Giả lập Bộ lọc rỗng` trên Sidebar $\rightarrow$ hộp thông báo cảnh báo vàng kèm nút Đặt lại bộ lọc.
3. **Trạng thái Lỗi kết nối CSDL (Error State):** Tích chọn `🔴 Giả lập Lỗi kết nối CSDL` $\rightarrow$ cảnh báo đỏ thân thiện, ẩn hoàn toàn chuỗi kết nối và traceback (đạt NFR3).

---

## 5. Cấu trúc Thư mục Dự án

```text
.
├── Dockerfile                     # Đóng gói Dockerfile kèm Healthcheck và curl
├── docker-compose.yml             # Khởi chạy toàn bộ hệ thống bằng 1 lệnh duy nhất
├── app.py                         # Entrypoint Dashboard Streamlit (3 trạng thái + Login + RBAC)
├── run_pipeline.py                # Entrypoint chạy Pipeline ETL 1 lệnh duy nhất
├── requirements.txt               # Thư viện có khóa phiên bản cố định (==)
├── pytest.ini                     # Cấu hình pythonpath = . cho pytest chạy máy trắng
├── .env.example                   # Biến môi trường mẫu không chứa secret thật
├── .gitignore                     # Loại trừ tệp tạm, cache, .env và file CSDL lớn
├── README.md                      # Tài liệu hướng dẫn cài đặt và kiểm thử BT3
├── BT3_2374802010259_MaiTuanKiet.pdf # File PDF báo cáo chính thức duy nhất nộp bài BT3
├── ho_so_bt3/                     # Thư mục hồ sơ báo cáo hoàn chỉnh BT3
│   ├── build_bt3_pdf.ps1          # Script tự động xuất PDF bằng Google Chrome headless
│   └── HO_SO_BT3_HOAN_CHINH.html  # Mã nguồn HTML hoàn chỉnh của báo cáo BT3
├── ho_so_bt2/                     # Hồ sơ Bài tập 2 (BT2)
├── ho_so_bt1/                     # Hồ sơ Bài tập 1 (BT1)
├── data/
│   ├── raw/                       # Dữ liệu CSV thô nguồn của 24 cửa hàng
│   └── dwh_mekong.duckdb          # Kho dữ liệu DuckDB Star Schema
├── seeds/                         # Dữ liệu hạt giống khởi tạo
├── sql/
│   └── schema.sql                 # Lược đồ DDL Star Schema (Dim, Fact, Reject, Audit)
├── src/                           # Mã nguồn kiến trúc phân lớp chuẩn Track DA
│   ├── extract/extractor.py       # Pha 1: Trích xuất an toàn (bắt EmptyDataError)
│   ├── quality/checker.py         # Pha kiểm soát chất lượng (6 hàm kiểm tra 3 chiều)
│   ├── transform/transformer.py   # Pha 2: Biến đổi, che SĐT NFR3, ánh xạ dimension
│   ├── load/loader.py             # Pha 3: Nạp kho DuckDB Idempotent Delete/Insert
│   ├── pipeline.py                # Điều phối toàn bộ quy trình ETL
│   └── dashboard/app.py           # Dashboard phân tích doanh thu
├── tests/
│   └── test_pipeline.py           # 12 test cases phủ đủ 5 loại kiểm thử cho Track DA
└── docs/                          # Hồ sơ đặc tả và tài liệu kỹ thuật
    ├── test-plan.md               # TP1: Kế hoạch kiểm thử rút gọn 4 mục
    ├── test-report.md             # TP2: Báo cáo kết quả kiểm thử 12 ca đủ 8 cột
    ├── bug-log.md                 # TP3: Nhật ký sửa lỗi 5 bug đủ 7 dòng chuẩn
    ├── deployment-guide.md        # TP5: Hướng dẫn triển khai tiếng Anh 5 mục chuẩn
    ├── checklist-bao-mat.md       # TP5: Checklist bảo mật 7 mục OWASP Top 10:2025
    ├── pipeline-doc.md            # TP6: Tài liệu kỹ thuật Pipeline tiếng Anh 6 mục
    ├── data-dictionary.md         # TP6: Từ điển dữ liệu Data Dictionary tiếng Anh
    ├── thay-doi-thiet-ke.md       # Ghi nhận các thay đổi thiết kế BT1 -> BT2 -> BT3
    ├── ai-disclosure.md           # Bảng khai báo sử dụng công cụ AI cho giai đoạn 3
    └── screenshots/               # Ảnh chụp minh chứng terminal kết quả chạy thật
```
