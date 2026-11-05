# BÁO CÁO BÀI TẬP 2 (BT2) — HIỆN THỰC HÓA MODULE CỐT LÕI
**Học phần:** Chuyên đề tốt nghiệp 1 – Học kỳ 1, Năm học 2026 – 2027  
**Phân hệ / Luồng nghiệp vụ:** Luồng L6 – Kho dữ liệu bán hàng & Báo cáo doanh thu đa chiều  
**Case Study:** Mekong Mobile Smart CRM  
**Sinh viên thực hiện:** Mai Tuấn Kiệt | **MSSV:** 2374802010259 | **Track:** Data Analytics (DA)  
**Giảng viên chấm điểm:** TS. Nguyễn Trí Hải / ThS. Nguyễn Minh Tân / ThS. Trần Công Thanh  
**Đường dẫn GitHub Repo:** [https://github.com/Maituankiet1301/MaiTuanKiet_2374802010259_BT2](https://github.com/Maituankiet1301/MaiTuanKiet_2374802010259_BT2)  
**Git Tag chính thức:** `v0.2`  
**File PDF chính thức đã xuất:** [BT2_2374802010259_MaiTuanKiet.pdf](BT2_2374802010259_MaiTuanKiet.pdf)

---

## MỤC LỤC TỔNG HỢP
1. [Mục 1: Tóm tắt hệ thống đã hiện thực](#mục-1-tóm-tắt-hệ-thống-đã-hiện-thực)
2. [Mục 2: Kiến trúc hệ thống đã hiện thực](#mục-2-kiến-trúc-hệ-thống-đã-hiện-thực)
3. [Mục 3: Module cốt lõi (Core Pipeline & Business Rules)](#mục-3-module-cốt-lõi-core-pipeline--business-rules)
4. [Mục 4: Bộ kiểm thử tự động (Automated Test Suite)](#mục-4-bộ-kiểm-thử-tự-động-automated-test-suite)
5. [Mục 5: Module mở rộng & Trình bày kết quả (Dashboard)](#mục-5-module-mở-rộng--trình-bày-kết-quả-dashboard)
6. [Mục 6: Cách dựng lại hệ thống (Reproducibility Guide)](#mục-6-cách-dựng-lại-hệ-thống-reproducibility-guide)
7. [Mục 7: Thay đổi so với thiết kế Bài tập 1](#mục-7-thay-đổi-so-với-thiết-kế-bài-tập-1)
8. [Phụ lục: Bảng khai báo sử dụng công cụ AI](#phụ-lục-bảng-khai-báo-sử-dụng-công-cụ-ai)

---

## MỤC 1. TÓM TẮT HỆ THỐNG ĐÃ HIỆN THỰC

### 1.1. Những phần đã hoàn thành 100%
- **Pha Trích xuất (Extract):** Module `DataExtractor` (`src/extract/extractor.py`) quét và nạp dữ liệu từ 24 tệp CSV bán hàng của chuỗi Mekong Mobile, hỗ trợ cơ chế fallback an toàn.
- **Pha Kiểm soát chất lượng (Quality):** Bộ 6 hàm kiểm tra độc lập (`src/quality/checker.py`), mỗi hàm trả về số lượng dòng lỗi và tỷ lệ phần trăm lỗi.
- **Pha Biến đổi (Transform):** Module `DataTransformer` (`src/transform/transformer.py`) chuẩn hóa 3 định dạng ngày tháng về ISO-8601 (`YYYY-MM-DD`); làm sạch chuỗi tiền tệ dính ký tự lạ; chuẩn hóa số điện thoại 10 số; che 4 số cuối (`090123****` - NFR3); định tuyến dòng lỗi vào các bảng Reject.
- **Pha Nạp dữ liệu (Load - Idempotent):** Module `DWHLoader` (`src/load/loader.py`) nạp kho DuckDB theo mô hình hình sao (Star Schema). Đạt tuyệt đối tiêu chí **IDEMPOTENT**: chạy lại nhiều lần không bao giờ bị nhân đôi dữ liệu.
- **Bộ kiểm thử tự động (Test Suite):** Xây dựng 4 kịch bản kiểm thử độc lập thuộc 3 loại khác nhau (Luồng đúng, Giá trị biên, Dữ liệu sai, Tính Idempotent) đạt kết quả **100% PASS** bằng một lệnh duy nhất: `pytest`.
- **Module mở rộng / Dashboard (Streamlit):** Ứng dụng Dashboard (`app.py`) phân tích trả lời đầy đủ 3 câu hỏi nghiệp vụ (CH1, CH2, CH4), có so sánh ngữ cảnh Benchmark, và **xử lý triệt để cả 3 trạng thái**: Đang tải, Rỗng/Bộ lọc không ra dòng nào, và Lỗi kết nối CSDL (có nút Thử lại, ẩn chuỗi kết nối).
- **Xác thực đăng nhập cơ bản (Authentication):** Dashboard yêu cầu đăng nhập trước khi truy cập, hỗ trợ 3 vai trò: `admin` (Giám đốc – xem toàn bộ 24 chi nhánh), `manager1` (Quản lý cửa hàng – xem CH01), `dataeng` (Kỹ sư dữ liệu – quản trị ETL). Có nút Đăng xuất trên Sidebar.
- **Đóng gói và Tái lập được:** Khởi chạy bằng lệnh đơn hoặc qua `docker-compose up`.

### 1.2. Những phần chủ ý chưa làm (Theo đúng phạm vi MoSCoW)
- Chưa triển khai Cloud công khai (thuộc phạm vi Bài tập 3).
- Chưa tích hợp thuật toán phân tích hành vi phức tạp (Customer Churn ML - thuộc Chuyên đề 2).

---

## MỤC 2. KIẾN TRÚC HỆ THỐNG ĐÃ HIỆN THỰC

| Tầng kiến trúc | Thư mục mã nguồn | Trách nhiệm và Thành phần cụ thể |
| :--- | :--- | :--- |
| **1. Data Source** | `seeds/` & `data/raw/` | Chứa các tệp dữ liệu bảng tính nguồn: `stores.csv` (24 chi nhánh), `products.csv` (24 sản phẩm), `orders_2024_2026.csv` (2.058 đơn hàng), `order_items.csv` (3.146 dòng chi tiết). |
| **2. Extract Layer** | `src/extract/` (`extractor.py`) | Quét thư mục, đọc CSV, kiểm soát lỗi thiếu tệp và nạp thô vào Pandas DataFrame. |
| **3. Quality Layer** | `src/quality/` (`checker.py`) | 6 hàm kiểm tra độc lập (CL1–CL5), tính số dòng lỗi và tỷ lệ lỗi. |
| **4. Transform Layer** | `src/transform/` (`transformer.py`) | Chuẩn hóa ngày ISO, làm sạch tiền tệ, che 4 số cuối SĐT, phân tách bản ghi sạch và bản ghi Reject. |
| **5. Load Layer (DWH)** | `src/load/` (`loader.py`, `sql/`) | Quản lý DuckDB (`dwh_mekong.duckdb`), nạp Star Schema idempotent và ghi `etl_audit_log`. |
| **6. Presentation Layer** | `app.py` & `src/dashboard/` | Dashboard Streamlit: Trực quan hóa CH1, CH2, CH4, thẻ KPI so sánh ngữ cảnh, và quản lý 3 trạng thái giao diện. |

---

## MỤC 3. MODULE CỐT LÕI (CORE PIPELINE & BUSINESS RULES)

### 3.1. Các quy tắc nghiệp vụ đã hiện thực hóa
1. **QT-01 (Khóa nghiệp vụ phức hợp):** Khử trùng lặp mã đơn giữa các chi nhánh bằng việc ghép cặp `(ma_cua_hang, ma_don)` ở tầng Staging và duy trì khóa logic duy nhất `(store_id, order_id, line_item_id)` trên bảng Fact.
2. **QT-02 (Chuẩn hóa ngày giao dịch ISO-8601):** Tự động nhận diện và chuyển đổi 3 định dạng ngày (`dd/mm/yyyy`, `d-m-yy`, `yyyy.mm.dd`) sang chuẩn `YYYY-MM-DD`. Ngày lỗi vào `reject_orders`.
3. **QT-03 (Bảo toàn tính toán thành tiền & Ngưỡng sai số 1đ):** Đối soát `thanh_tien` so với `so_luong * don_gia`. Sai số $\le 1$ VNĐ được chấp nhận; sai số $> 1$ VNĐ bị cách ly vào bảng `reject_order_items`.
4. **QT-04 (Chuẩn hóa số điện thoại & Bảo mật NFR3):** Số điện thoại làm sạch về 10 chữ số chuẩn viễn thông Việt Nam; che (mask) 4 chữ số cuối (`090123****`).
5. **QT-05 (Toàn vẹn tham chiếu & Bản ghi dự phòng):** Cửa hàng lạ bị từ chối; sản phẩm lạ gán `product_key = -1` (Chưa phân loại) để không làm mất số liệu tổng doanh thu.

### 3.2. Báo cáo kiểm soát chất lượng dữ liệu
| Mục kiểm tra | Quy tắc | Số dòng lỗi | Tỉ lệ lỗi | Xử lý |
| :--- | :--- | :---: | :---: | :--- |
| `check_date_validity` | CL2 / QT-02 | **3 dòng** | 0.15 % | Cách ly vào `reject_orders` (INVALID_DATE_FORMAT) |
| `check_currency_amount` | CL1 / QT-03 | **1 dòng** | 0.05 % | Cách ly vào `reject_orders` (CORRUPTED_CURRENCY_STRING) |
| `check_referential_integrity` | CL5 / QT-05 | **1 dòng** | 0.05 % | Cách ly vào `reject_orders` (UNKNOWN_STORE_ID) |
| `check_uniqueness` | CL3 / QT-01 | **0 dòng** | 0.00 % | Khóa phức hợp triệt tiêu trùng lặp |
| `check_line_total_consistency` | CL4 / QT-03 | **2 dòng** | 0.06 % | Cách ly vào `reject_order_items` |
| `check_phone_validity` | QT-04 | **0 dòng** | 0.00 % | 100% SĐT có dữ liệu chuẩn hóa thành công |

### 3.3. Minh chứng tính Idempotent (Chống nhân đôi dữ liệu)
- **Lần chạy 1:** `fact_sales` nạp **3.144 dòng** (Thời gian: 1.38 giây).
- **Lần chạy 2:** `fact_sales` duy trì đúng **3.144 dòng** (Thời gian: 1.42 giây).
$\rightarrow$ **Kết luận:** Dữ liệu hoàn toàn không bị nhân đôi khi chạy lại pipeline.

---

## MỤC 4. BỘ KIỂM THỬ TỰ ĐỘNG (AUTOMATED TEST SUITE)

Chạy bằng một lệnh duy nhất: `pytest -v`

| Loại kiểm thử | Hàm kiểm thử | Kết quả |
| :--- | :--- | :---: |
| **1. Luồng đúng** | `test_case_1_luong_dung_normal_flow` | <span style="color:green; font-weight:bold;">PASSED</span> |
| **2. Giá trị biên** | `test_case_2_gia_tri_bien_line_total_tolerance` | <span style="color:green; font-weight:bold;">PASSED</span> |
| **3. Dữ liệu sai** | `test_case_3_du_lieu_sai_graceful_rejection` | <span style="color:green; font-weight:bold;">PASSED</span> |
| **4. Kiểm thử Idempotent** | `test_case_4_idempotent_double_run` | <span style="color:green; font-weight:bold;">PASSED</span> |

**Kết quả:** 4 passed in 1.35s (100% PASS).

---

## MỤC 5. MODULE MỞ RỘNG & TRÌNH BÀY KẾT QUẢ (DASHBOARD)

### 5.1. Trả lời các câu hỏi phân tích có ngữ cảnh so sánh
- **CH1:** Biểu đồ đường doanh thu theo tháng/ngày kèm đường chuẩn trung bình (Benchmark line) màu đỏ; thẻ KPI AOV so sánh với trung bình hệ thống (`+52.000 đ so với TB toàn chuỗi`).
- **CH2:** Bảng cảnh báo đỏ các chi nhánh sụt giảm 3 tháng liên tiếp tính bằng hàm cửa sổ `LAG()`, hiển thị mức % giảm.
- **CH4:** Biểu đồ Donut phân bổ doanh số theo nhóm danh mục thiết bị và phụ kiện theo từng quý.

### 5.2. Xác thực đăng nhập cơ bản (Authentication)
Dashboard yêu cầu xác thực trước khi truy cập, phân quyền theo vai trò:

| Tài khoản | Mật khẩu | Vai trò | Phạm vi dữ liệu |
|---|---|---|---|
| `admin` | `admin123` | Giám đốc kinh doanh | Toàn bộ 24 chi nhánh |
| `manager1` | `manager123` | Quản lý cửa hàng | Cửa hàng CH01 |
| `dataeng` | `data123` | Kỹ sư dữ liệu | Toàn bộ hệ thống + ETL |

### 5.3. Hiện thực hóa và minh chứng CẢ BA TRẠNG THÁI
1. **Trạng thái Đang tải (Loading State):** `st.spinner("⏳ Đang thực thi truy vấn...")`.
2. **Trạng thái Dữ liệu rỗng (Empty State):** Tích chọn toggle *"🟡 Giả lập Bộ lọc rỗng"* $\rightarrow$ Giao diện hiển thị cảnh báo bộ lọc không có dữ liệu phù hợp kèm nút Đặt lại bộ lọc.
3. **Trạng thái Lỗi kết nối CSDL (Error State):** Tích chọn toggle *"🔴 Giả lập Lỗi kết nối CSDL"* $\rightarrow$ Giao diện hiển thị cảnh báo đỏ thân thiện, ẩn hoàn toàn chuỗi kết nối và mật khẩu, cung cấp nút Thử lại.

---

## MỤC 6. CÁCH DỰNG LẠI HỆ THỐNG (REPRODUCIBILITY GUIDE)

```bash
# Bước 1: Clone repo
git clone https://github.com/Maituankiet1301/MaiTuanKiet_2374802010259_BT2.git
cd MaiTuanKiet_2374802010259_BT2

# Bước 2: Tạo và kích hoạt môi trường ảo
python -m venv .venv
.venv\Scripts\activate

# Bước 3: Cài đặt thư viện theo tệp khóa
pip install -r requirements.txt

# Bước 4: Chạy Pipeline nạp kho DuckDB (1 lệnh duy nhất)
python run_pipeline.py

# Bước 5: Chạy bộ kiểm thử tự động
pytest -v

# Bước 6: Khởi chạy Dashboard Streamlit
streamlit run app.py
# Đăng nhập bằng tài khoản: admin / admin123 (hoặc manager1 / manager123)
```

---

## MỤC 7. THAY ĐỔI SO VỚI THIẾT KẾ BÀI TẬP 1

- **Thay đổi 1 (Bổ sung `line_item_id` vào khóa logic Fact):**
  - *Thay đổi gì:* Thêm `line_item_id` vào bộ khóa `(store_id, order_id, line_item_id)`.
  - *Vì sao:* Đơn hàng có nhiều mặt hàng; tránh đè các sản phẩm khác khi chạy lại pipeline.
  - *Ảnh hưởng:* Bảng `fact_sales` và module `loader.py`.
- **Thay đổi 2 (Tách biệt bảng `reject_order_items`):**
  - *Thay đổi gì:* Tạo riêng bảng `reject_order_items` lưu các dòng lệch tiền > 1đ.
  - *Vì sao:* Lỗi thành tiền phát sinh ở cấp độ dòng chi tiết, không phải toàn đơn.
  - *Ảnh hưởng:* Bảng Reject trong DDL và hàm `check_line_total_consistency`.
- **Thay đổi 3 (Chuẩn hóa kho dữ liệu DuckDB nhúng):**
  - *Thay đổi gì:* Sử dụng DuckDB thay vì PostgreSQL daemon server.
  - *Vì sao:* Tối ưu OLAP dạng cột, không cần cài server, đảm bảo chạy được ngay trên máy người khác.
  - *Ảnh hưởng:* Module `loader.py`, `app.py` và `requirements.txt`.

---

## PHỤ LỤC. BẢNG KHAI BÁO SỬ DỤNG CÔNG CỤ AI

| Công cụ AI | Dùng vào việc gì cụ thể | Áp dụng ở tệp / hàm nào | Em đã kiểm chứng thế nào? |
| :--- | :--- | :--- | :--- |
| **Claude / ChatGPT / Antigravity** | Gợi ý cấu trúc giải thuật nạp Idempotent trong DuckDB theo bộ ba khóa tự nhiên. | `src/load/loader.py`, hàm `load_fact_sales` | Đọc tài liệu DuckDB về ACID; viết test case `test_case_4_idempotent_double_run`; chạy pipeline 2 lần kiểm tra `COUNT(*)`. |
| **Claude / ChatGPT / Antigravity** | Gợi ý Regex và thứ tự ưu tiên parse 3 định dạng ngày tháng. | `src/quality/checker.py`, hàm `parse_date_flexibly` | Viết unit test cho các định dạng ngày biên; chạy trên tập 2.058 đơn hàng để kiểm tra tính chính xác. |
| **Claude / ChatGPT / Antigravity** | Gợi ý mẫu layout 3 trạng thái (Loading, Empty, Error) cho Streamlit. | `app.py`, khối `st.spinner`, kiểm tra `empty` và `try...except` | Tự tạo 2 checkbox toggle trên Sidebar để kiểm tra trực quan giao diện ứng xử đúng theo rubric; đảm bảo chuỗi kết nối không bị lộ. |
| **— Không dùng — (Tự làm hoàn toàn)** | Thiết kế kiến trúc phân lớp; xây dựng 6 hàm đo chất lượng; thiết kế Star Schema; lập luận phân tích CH1, CH2, CH4. | Toàn bộ cấu trúc dự án `src/`, file `sql/schema.sql`, `seeds/generate_seeds.py` | Tự thiết kế và đối chiếu với Hồ sơ BT1; tự viết toàn bộ câu truy vấn phân tích SQL sụt giảm 3 tháng (`LAG`) và chạy pytest đạt 100% PASS. |

> **"Tôi xác nhận đã đọc, hiểu và chịu trách nhiệm về toàn bộ nội dung nộp trong báo cáo và kho mã nguồn này."**  
> **Sinh viên thực hiện:** Mai Tuấn Kiệt | **MSSV:** 2374802010259 | **Ngày:** 05/11/2026
