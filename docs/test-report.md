# BÁO CÁO KẾT QUẢ KIỂM THỬ THỰC TẾ (TEST REPORT - LUỒNG L6)
**Hệ thống:** Mekong Mobile Smart CRM – Kho dữ liệu bán hàng & Báo cáo doanh thu đa chiều  
**Sinh viên thực hiện:** Mai Tuấn Kiệt | **MSSV:** 2374802010259 | **Track:** Data Analytics (DA)  
**Thời điểm chạy kiểm thử:** Ngày 07 tháng 11 năm 2026 | **Lệnh thực thi:** `pytest -v`  
**Kết quả tổng quan:** **12/12 Test Cases PASSED 100% (Thời gian chạy: 1.62s)**  
**Minh chứng ảnh chụp:** Đầy đủ 12 ảnh chụp terminal tương ứng tại `docs/screenshots/TC-01.png` → `TC-12.png`  

---

## 1. BẢNG TỔNG HỢP CHI TIẾT 12 CA KIỂM THỬ ĐÃ CHẠY THẬT (ĐỦ 8 CỘT CHUẨN)

| Mã Test | Tên & Mô tả ca kiểm thử (Loại test) | Ưu tiên | Tiền điều kiện (Pre-conditions) | Các bước thực hiện (Test Steps) | Kết quả mong đợi (Expected Result) | Kết quả thực tế (Actual Result) | Đánh giá & Minh chứng |
|:---:|:---|:---:|:---|:---|:---|:---|:---:|
| **TC-01** | **Nạp dữ liệu chuẩn hợp lệ vào Star Schema**<br>*(Loại 1: Luồng đúng - Normal flow)* | **Cao** | Fixture dữ liệu sạch trong bộ nhớ gồm 2 cửa hàng, 2 sản phẩm, 2 đơn hàng, 2 dòng chi tiết. | 1. Khởi tạo `DataTransformer(batch_id)`.<br>2. Gọi `transform_all(sample_valid_data)`.<br>3. Kiểm tra số dòng Fact, Reject và tổng tiền. | - `len(df_fact) == 2`<br>- `len(df_rej_orders) == 0`<br>- `len(df_rej_items) == 0`<br>- Tổng doanh thu: 25.350.000 đ. | Fact nạp đúng 2 dòng; 0 đơn reject; 0 item reject; tổng doanh thu Fact = 25.350.000 đ; store_key > 0. | **PASS**<br>[TC-01.png](screenshots/TC-01.png) |
| **TC-02** | **Ánh xạ an toàn sản phẩm chưa phân loại**<br>*(Loại 1: Luồng đúng - Normal flow)* | **Cao** | Đơn hàng hợp lệ chứa mã sản phẩm lạ `SP999_CHUA_CO` không nằm trong danh mục 24 sản phẩm. | 1. Tạo payload chứa đơn hàng mua `SP999_CHUA_CO`.<br>2. Gọi `transformer.transform_all(payload)`.<br>3. Kiểm tra `product_key` trên bảng `fact_sales`. | - `len(df_fact) == 1`<br>- `product_key == -1` (Unknown)<br>- Đơn hàng KHÔNG bị đưa vào reject. | Fact nạp đủ 1 dòng; `product_key = -1`; `df_rej_orders` có 0 dòng; doanh thu 1.200.000 đ được bảo toàn. | **PASS**<br>[TC-02.png](screenshots/TC-02.png) |
| **TC-03** | **Sai số thành tiền trong ngưỡng cho phép (0đ, ±1đ)**<br>*(Loại 2: Giá trị biên - Boundary value)* | **Cao** | Tập 3 dòng mặt hàng có độ lệch thành tiền đúng biên quy tắc QT-03: 0đ, +1đ (biên trên), -1đ (biên dưới). | 1. Tạo DataFrame 3 dòng chi tiết với thành tiền lệch 0đ, +1đ, -1đ.<br>2. Gọi `check_line_total_consistency(threshold=1)`. | - `failed_cnt == 0`<br>- `error_rate == 0.0%`<br>- 100% dòng được chấp nhận hợp lệ. | `failed_cnt = 0`; `error_rate = 0.0%`; `len(failed_df) = 0`; cả 3 trường hợp biên đều hợp lệ. | **PASS**<br>[TC-03.png](screenshots/TC-03.png) |
| **TC-04** | **Sai số thành tiền vượt ngưỡng (±2đ) bị từ chối**<br>*(Loại 2: Giá trị biên - Boundary value)* | **Cao** | Tập 2 dòng mặt hàng có độ lệch thành tiền vượt biên quy tắc QT-03: +2đ (vượt trên) và -2đ (vượt dưới). | 1. Tạo DataFrame 2 dòng có thành tiền lệch +2đ và -2đ.<br>2. Gọi `check_line_total_consistency(threshold=1)`.<br>3. Kiểm tra số lượng lỗi và `diff_amount`. | - `failed_cnt == 2`<br>- `error_rate == 1.0 (100%)`<br>- Bắt đúng dòng vi phạm và độ lệch 2đ. | `failed_cnt = 2`; `error_rate = 1.0`; `diff_values` ghi nhận đúng {2}; cả 2 dòng bị cách ly an toàn. | **PASS**<br>[TC-04.png](screenshots/TC-04.png) |
| **TC-05** | **Từ chối đơn hàng sai định dạng ngày tháng**<br>*(Loại 3: Dữ liệu sai - Invalid data)* | **Cao** | 3 đơn hàng cố tình sai ngày: ngày ảo `31/02/2025`, ngày trước 2020 (`2018-05-15`), chuỗi rác `NGAY_KHONG_HOP_LE`. | 1. Nạp payload chứa 3 đơn hàng sai ngày.<br>2. Chạy `transformer.transform_all(payload)`.<br>3. Kiểm tra bảng `reject_orders` và `fact_sales`. | - `len(df_rej_orders) == 3`<br>- `error_code == 'INVALID_DATE_FORMAT'`<br>- `len(df_fact) == 0`. | Pipeline không crash; từ chối đúng 3 đơn; 100% gán mã lỗi `INVALID_DATE_FORMAT`; Fact có 0 dòng. | **PASS**<br>[TC-05.png](screenshots/TC-05.png) |
| **TC-06** | **Từ chối chuỗi tiền tệ hỏng hoặc số tiền âm**<br>*(Loại 3: Dữ liệu sai - Invalid data)* | **Cao** | 2 đơn hàng có tiền tệ hỏng: chuỗi chữ `HAI_TRIEU_DONG` và giá trị âm `-250000`. | 1. Nạp payload chứa 2 đơn hàng sai tiền.<br>2. Chạy `transformer.transform_all(payload)`.<br>3. Kiểm tra bảng `reject_orders` và mã lỗi. | - `len(df_rej_orders) == 2`<br>- `error_code == 'CORRUPTED_CURRENCY_STRING'`<br>- Fact không thêm bản ghi hỏng. | Từ chối đủ 2 đơn; ghi mã lỗi `CORRUPTED_CURRENCY_STRING`; Fact: 0 bản ghi; không xảy ra lỗi ép kiểu. | **PASS**<br>[TC-06.png](screenshots/TC-06.png) |
| **TC-07** | **Vi phạm toàn vẹn tham chiếu mã cửa hàng**<br>*(Loại 3: Dữ liệu sai - Invalid data)* | **Cao** | Đơn hàng có mã cửa hàng `CH99_KHONG_CO` không tồn tại trong danh mục 24 chi nhánh. | 1. Nạp đơn hàng có mã `CH99_KHONG_CO`.<br>2. Chạy `transformer.transform_all(payload)`.<br>3. Kiểm tra định tuyến lỗi vào `reject_orders`. | - `len(df_rej_orders) == 1`<br>- `error_code == 'UNKNOWN_STORE_ID'`<br>- `len(df_fact) == 0`. | Cách ly thành công 1 đơn vào `reject_orders`; ghi nhận mã `UNKNOWN_STORE_ID`; Fact có 0 dòng. | **PASS**<br>[TC-07.png](screenshots/TC-07.png) |
| **TC-08** | **Che 4 số cuối điện thoại khách hàng (Masking)**<br>*(Loại 4: Bảo mật - Security NFR3)* | **Cao** | Dữ liệu khách hàng có SĐT 10 số dạng `0901234567` và `84912345678`. | 1. Chạy `transformer.transform_all(sample_valid_data)`.<br>2. Truy vấn bảng `dim_customer`.<br>3. Kiểm tra cột `masked_phone`. | - Đúng 10 ký tự.<br>- Kết thúc bằng `****`.<br>- Không để lộ toàn bộ số nguyên gốc. | `dim_customer` che thành `090123****` và `091234****`; độ dài = 10; kết thúc bằng 4 dấu sao; đạt NFR3. | **PASS**<br>[TC-08.png](screenshots/TC-08.png) |
| **TC-09** | **Bộ kiểm tra chất lượng tự động cảnh báo**<br>*(Loại 4: Chất lượng dữ liệu - Data Quality)* | **Trung bình** | Tập dữ liệu hỗn hợp: 1 đơn sai ngày (tỷ lệ 25%), 1 đơn sai tiền (25%), 1 đơn sai cửa hàng (25%), 1 dòng lệch tiền (50%). | 1. Gọi `run_data_quality_suite(orders_mixed, items_mixed, stores)`.<br>2. Kiểm tra `failed_count` và `error_rate` trả về. | - `date_validity`: failed=1, rate=0.25<br>- `line_total`: failed=1, rate=0.50<br>- Đo lường chính xác không sót lỗi. | Kết quả đo lường: `date_err = 0.25 (1/4)`; `line_total_err = 0.50 (1/2)`; cảnh báo chính xác vượt ngưỡng. | **PASS**<br>[TC-09.png](screenshots/TC-09.png) |
| **TC-10** | **Chống SQL Injection và ký tự đặc biệt nguy hiểm**<br>*(Loại 4: Bảo mật CSDL - Security)* | **Cao** | Đơn hàng chứa chuỗi độc hại: `Robert'); DROP TABLE fact_sales; --` và `<script>alert('xss')</script>`. | 1. Khởi tạo kho DuckDB tạm thời.<br>2. Chạy transform và gọi `loader.load_fact_sales`.<br>3. Đếm số dòng bảng `fact_sales` sau khi nạp. | - DuckDB không báo lỗi cú pháp SQL.<br>- Bảng `fact_sales` không bị DROP.<br>- Fact nạp an toàn 1 dòng. | Parameterized queries xử lý an toàn chuỗi; `counts['fact_sales'] = 1`; CSDL và schema toàn vẹn 100%. | **PASS**<br>[TC-10.png](screenshots/TC-10.png) |
| **TC-11** | **Tính Idempotent: Chạy 2 lần không nhân đôi**<br>*(Loại 5: Tái lập - Reproducibility & Idempotent)* | **Cao** | CSDL DuckDB tạm thời; bộ dữ liệu mẫu 2 đơn hàng hợp lệ. | 1. Nạp lần 1: đếm số dòng `fact_sales`.<br>2. Nạp lần 2 với cùng dữ liệu.<br>3. So sánh số dòng lần 2 với lần 1. | - Số dòng `fact_sales` lần 1 = 2.<br>- Số dòng `fact_sales` lần 2 = 2.<br>- `count_run_2 == count_run_1`. | Lần 1: 2 dòng Fact; Lần 2: 2 dòng Fact (2 -> 2 dòng, độ lệch = 0); các bảng dim không đổi số dòng. | **PASS**<br>[TC-11.png](screenshots/TC-11.png) |
| **TC-12** | **Xử lý an toàn tệp dữ liệu rỗng 0 bytes**<br>*(Loại 5: Tính ổn định - Robustness)* | **Cao** | 4 tệp CSV nguồn rỗng kích thước 0 bytes (`stores.csv`, `products.csv`, `orders.csv`, `order_items.csv`). | 1. Gọi `DataExtractor.extract_all()`.<br>2. Chạy `DataTransformer.transform_all()`.<br>3. Kiểm tra ngoại lệ và số dòng trả về. | - Bắt ngoại lệ `EmptyDataError`.<br>- Ghi log cảnh báo rõ ràng.<br>- Fact trả về 0 dòng, 0 crash. | `_read_csv_safe` bắt `EmptyDataError`, trả DataFrame rỗng có schema chuẩn; pipeline hoàn tất với 0 dòng Fact, 0 crash. | **PASS**<br>[TC-12.png](screenshots/TC-12.png) |

---

## 2. MINH CHỨNG KẾT QUẢ CHẠY THẬT (TERMINAL EVIDENCE)

Toàn bộ 12 ca kiểm thử đã được chạy thực tế trên máy tính và chụp ảnh terminal trực tiếp vào thư mục `docs/screenshots/`:
- **Ảnh chụp tổng hợp toàn bộ 12 ca test PASSED 100%:** `docs/screenshots/full-pytest-pass.png`
- **Ảnh chụp chi tiết từng test case:**
  + [TC-01: Luồng đúng nạp dữ liệu chuẩn](screenshots/TC-01.png)
  + [TC-02: Ánh xạ an toàn sản phẩm lạ](screenshots/TC-02.png)
  + [TC-03: Biên sai số thành tiền trong ngưỡng cho phép](screenshots/TC-03.png)
  + [TC-04: Biên sai số thành tiền vượt ngưỡng cho phép](screenshots/TC-04.png)
  + [TC-05: Từ chối đơn hàng sai ngày](screenshots/TC-05.png)
  + [TC-06: Từ chối chuỗi tiền tệ hỏng](screenshots/TC-06.png)
  + [TC-07: Từ chối mã cửa hàng không tồn tại](screenshots/TC-07.png)
  + [TC-08: Bảo mật che số điện thoại NFR3](screenshots/TC-08.png)
  + [TC-09: Bộ kiểm tra chất lượng cảnh báo](screenshots/TC-09.png)
  + [TC-10: Bảo mật chống SQL Injection](screenshots/TC-10.png)
  + [TC-11: Tính Idempotent nạp lại 2 lần](screenshots/TC-11.png)
  + [TC-12: Xử lý an toàn tệp CSV rỗng 0 bytes](screenshots/TC-12.png)

---

## 3. KẾT LUẬN & ĐÁNH GIÁ CHẤT LƯỢNG
- **Tỷ lệ thành công:** Đạt **100% (12/12 test case PASSED)**.
- **Tiêu chuẩn kiểm thử:** Phủ trọn vẹn 5 loại kiểm thử chuyên ngành Data Analytics (Luồng đúng, Biên 2 phía, Dữ liệu sai cách ly an toàn, Bảo mật & Chất lượng dữ liệu, Tính tái lập Idempotent).
- **Tính sẵn sàng cho phản biện:** Bất kỳ test case nào giảng viên chọn ngẫu nhiên đều có thể chạy lại ngay tại chỗ bằng lệnh:
  ```powershell
  pytest -v tests/test_pipeline.py::<tên_hàm_test>
  ```
