# BẢN GHI NHẬN THAY ĐỔI THIẾT KẾ (BT1 → BT2 → BUỔI 14)
**Học phần:** Chuyên đề tốt nghiệp 1 – Học kỳ 1, Năm học 2026 – 2027  
**Phân hệ / Luồng nghiệp vụ:** Luồng L6 – Kho dữ liệu bán hàng & Báo cáo doanh thu đa chiều (Smart CRM - Mekong Mobile)  
**Sinh viên thực hiện:** Mai Tuấn Kiệt | **MSSV:** 2374802010259 | **Track:** Data Analytics (DA)  
**Giảng viên chính:** TS. Nguyễn Trí Hải / ThS. Nguyễn Minh Tân / ThS. Trần Công Thanh  
**Quy tắc:** Mỗi thay đổi ghi đúng 3 dòng: *Thay đổi gì · Vì sao · Ảnh hưởng tới thành phần nào*.

---

## PHẦN A. CÁC THAY ĐỔI KỸ THUẬT TỪ BÀI TẬP 1 SANG BÀI TẬP 2

### THAY ĐỔI 1: Bổ sung cột thứ tự mặt hàng `line_item_id` vào Khóa logic của bảng Fact
- **Thay đổi gì:** Bổ sung trường `line_item_id` để kết hợp thành bộ ba khóa logic tự nhiên `(store_id, order_id, line_item_id)` kèm Unique Constraint trên bảng `fact_sales`.
- **Vì sao:** Trong một đơn hàng của Mekong Mobile, khách hàng có thể mua nhiều sản phẩm khác nhau. Nếu chỉ dùng `(store_id, order_id)` làm khóa kiểm tra thì các mặt hàng thứ 2, thứ 3 trong cùng đơn sẽ bị ghi đè khi thực thi chiến lược nạp idempotent.
- **Ảnh hưởng tới thành phần nào:** Lược đồ bảng `fact_sales` trong `sql/schema.sql`, logic xử lý `src/transform/transformer.py` và câu lệnh DELETE/INSERT trong `src/load/loader.py`.

---

### THAY ĐỔI 2: Tách biệt bảng cách ly lỗi dòng hàng `reject_order_items` bên cạnh `reject_orders`
- **Thay đổi gì:** Xây dựng thêm bảng `reject_order_items` chuyên biệt để lưu trữ các dòng chi tiết vi phạm quy tắc tính tiền $|thanh\_tien - so\_luong \times don\_gia| > 1$ VNĐ (theo QT-03).
- **Vì sao:** Ban đầu ở BT1 dự kiến dồn chung vào một bảng `reject_orders`. Tuy nhiên, lỗi thành tiền phát sinh ở cấp độ từng dòng mặt hàng (`order_items.csv`), việc tách bảng giúp lưu vết chi tiết số lượng, đơn giá, số tiền chênh lệch mà không làm sai lệch cấu trúc dữ liệu đơn hàng tổng quát.
- **Ảnh hưởng tới thành phần nào:** Script DDL `sql/schema.sql`, hàm `check_line_total_consistency` trong `src/quality/checker.py`, và bảng báo cáo kiểm toán ETL.

---

### THAY ĐỔI 3: Chuẩn hóa engine kho dữ liệu phân tích nhúng DuckDB phục vụ triển khai cục bộ
- **Thay đổi gì:** Hiện thực hóa kho dữ liệu phân tích trực tiếp trên DuckDB (tệp `data/dwh_mekong.duckdb`) thay vì cấu hình máy chủ PostgreSQL phụ thuộc dịch vụ ngoài.
- **Vì sao:** DuckDB là hệ quản trị CSDL phân tích dạng cột (columnar OLAP) tối ưu vượt trội cho các truy vấn tổng hợp đa chiều theo chuẩn Kimball, không cần cài đặt daemon server, cho phép giảng viên hoặc sinh viên khác clone repo về là chạy được ngay trong 1 lệnh duy nhất (đáp ứng trọn vẹn tiêu chí Tái lập được và NFR4).
- **Ảnh hưởng tới thành phần nào:** Module `src/load/loader.py`, script `run_pipeline.py`, ứng dụng Dashboard `app.py` và tệp cấu hình `.env.example`.

---

## PHẦN B. TIẾP NHẬN PHẢN HỒI BT2 & QUYẾT ĐỊNH XỬ LÝ (WORKSHOP BUỔI 14)

### Bảng 1: Tổng hợp phản hồi của Giảng viên khi chạy thử repo ở buổi 12 và quyết định xử lý

| STT | Phản hồi từ Giảng viên khi chạy thử repo BT2 | Phân loại & Mức độ | Quyết định xử lý của sinh viên | Nơi ghi nhận minh chứng |
|:---:|:---|:---:|:---|:---|
| 1 | Clone theo README chạy lệnh `pytest` báo lỗi `ModuleNotFoundError: No module named 'src'`, người khác không chạy được test suite. | Bug Major (Môi trường) | Tạo tệp `pytest.ini` với `pythonpath = .` và `testpaths = tests`, cập nhật README.md hướng dẫn lệnh kiểm thử đơn giản `pytest -v` hoặc `pytest -q`. | Ghi vào `Bug Log (BUG-01)` và Thay đổi 4 |
| 2 | Nạp gia tăng nhiều batch liên tiếp bị lỗi `Constraint Error: Duplicate key violates primary key constraint` trên bảng `fact_sales` và `reject_orders`. | Bug Critical (Toàn vẹn DWH) | Đồng bộ max surrogate key từ CSDL qua `loader.get_max_keys()` và bổ sung cơ chế fallback sinh khóa động theo `ROW_NUMBER() OVER () + MAX(...)` chống đè khóa. | Ghi vào `Bug Log (BUG-02)` và Thay đổi 5 |
| 3 | Tệp CSV nguồn rỗng (0 bytes) làm sập hệ thống với ngoại lệ `pandas.errors.EmptyDataError`, thiếu khả năng chịu lỗi. | Bug Major (Xử lý ngoại lệ) | Viết hàm `_read_csv_safe` trong `DataExtractor` bắt ngoại lệ `EmptyDataError`, ghi log cảnh báo và trả về DataFrame rỗng có schema chuẩn. | Ghi vào `Bug Log (BUG-03)` và Thay đổi 6 |
| 4 | Mật khẩu tài khoản phân quyền Dashboard đang lưu plaintext trong `app.py`, vi phạm tiêu chuẩn bảo mật NFR3 khi public repo. | Bug Major (Bảo mật NFR3) | Áp dụng thuật toán băm mật khẩu một chiều SHA-256 kèm salt bảo mật, hỗ trợ nạp credentials từ biến môi trường `.env`. | Ghi vào `Bug Log (BUG-04)` và Thay đổi 7 |
| 5 | Bộ kiểm thử tự động quá ít (chỉ 4 test case), thiếu kiểm thử biên 2 phía, bảo mật, chất lượng dữ liệu và tính chịu lỗi. | Yêu cầu chất lượng BT3 | Thiết kế và hoàn thiện Test Plan 4 mục; mở rộng bộ kiểm thử lên 12 test cases phủ đủ 5 loại kiểm thử bắt buộc cho Track DA; chạy thật và chụp ảnh terminal 100%. | Ghi vào `Test Plan`, `Test Report` (TC-01..TC-12) |
| 6 | Khi tập dữ liệu chi tiết đơn hàng rỗng hoặc thiếu cột `ma_cua_hang`, `DataTransformer` bị lỗi `KeyError: 'ma_cua_hang'`. | Bug Major (Xử lý biên) | Bổ sung kiểm tra cấu trúc `df_items_raw` trước khi thực hiện `groupby(["ma_cua_hang", "ma_don"])`; bổ sung format ngày `%d-%m-%Y`. | Ghi vào `Bug Log (BUG-05)` và Thay đổi 8 |

---

### THAY ĐỔI 4: Bổ sung tệp cấu hình `pytest.ini` giải quyết triệt để lỗi đường dẫn module `src`
- **Thay đổi gì:** Bổ sung tệp `pytest.ini` tại thư mục gốc với cấu hình `pythonpath = .` và `testpaths = tests`.
- **Vì sao:** Khi người chấm hoặc sinh viên khác clone repo về máy trắng và chạy lệnh `pytest -v` (hoặc `pytest -q`), Python không tự động đưa thư mục làm việc hiện tại vào `sys.path`, gây ra lỗi collection failure `ModuleNotFoundError: No module named 'src'`.
- **Ảnh hưởng tới thành phần nào:** Tệp `pytest.ini`, tài liệu `README.md`, và toàn bộ quy trình chạy test tự động.

---

### THAY ĐỔI 5: Đồng bộ Max Surrogate Key và Fallback chống trùng khóa chính khi nạp nhiều Batch
- **Thay đổi gì:** Bổ sung phương thức `get_max_keys()` trong `DWHLoader` để truyền ID lớn nhất hiện hữu cho `DataTransformer`; đồng thời nâng cấp câu lệnh SQL `INSERT INTO fact_sales` và `INSERT INTO reject_orders` sử dụng biểu thức `CASE WHEN key IN (SELECT key ...) THEN MAX(...) + ROW_NUMBER() OVER () ELSE key END`.
- **Vì sao:** Trước đó, biến đếm surrogate key được đặt cố định trong bộ nhớ (100000, 1000, 5000), khiến mẻ nạp thứ 2 phát sinh trùng lặp khóa chính với mẻ nạp thứ 1, vi phạm ràng buộc PRIMARY KEY của DuckDB.
- **Ảnh hưởng tới thành phần nào:** Module `src/load/loader.py`, `src/transform/transformer.py`.

---

### THAY ĐỔI 6: Xử lý an toàn ngoại lệ `EmptyDataError` khi tệp CSV rỗng 0 bytes
- **Thay đổi gì:** Xây dựng hàm `_read_csv_safe` trong `DataExtractor` bọc quanh `pd.read_csv` với kiểm tra kích thước file (`os.path.getsize == 0`) và bắt ngoại lệ `pd.errors.EmptyDataError`.
- **Vì sao:** Trong điều kiện vận hành thực tế của chuỗi 24 chi nhánh, sự cố truyền tải mạng có thể khiến file CSV bị rỗng 0 bytes. Nếu không bắt ngoại lệ, pipeline sẽ sập hoàn toàn (crash) thay vì cách ly và cảnh báo an toàn.
- **Ảnh hưởng tới thành phần nào:** Module `src/extract/extractor.py`.

---

### THAY ĐỔI 7: Băm mật khẩu SHA-256 kèm Salt cho cơ chế xác thực Dashboard
- **Thay đổi gì:** Thay thế cơ chế so khớp mật khẩu plaintext bằng hàm băm mật khẩu `hash_password(password, salt)` sử dụng thuật toán SHA-256 kèm chuỗi Salt bí mật trong `app.py`; cho phép ghi đè qua biến môi trường.
- **Vì sao:** Đáp ứng tiêu chuẩn bảo mật NFR3 và yêu cầu của Bài tập 3 (repo bắt buộc PUBLIC). Việc để lộ mật khẩu plaintext trên GitHub vi phạm nghiêm trọng chuẩn mực an toàn thông tin và checklist bảo mật.
- **Ảnh hưởng tới thành phần nào:** Tệp `app.py`, cấu hình `.env.example`.

---

### THAY ĐỔI 8: Tăng cường tính bền vững cho bộ lọc Transformer và bộ phân giải ngày tháng
- **Thay đổi gì:** Bổ sung kiểm tra cấu trúc cột và dữ liệu rỗng cho `df_items_raw` trước khi thực hiện `groupby(["ma_cua_hang", "ma_don"])`; bổ sung định dạng ngày `%d-%m-%Y` vào hàm `parse_date_flexibly`.
- **Vì sao:** Tránh lỗi `KeyError: 'ma_cua_hang'` khi nạp đơn hàng không có chi tiết; đồng thời hỗ trợ đầy đủ các định dạng ngày thực tế tại Việt Nam không bị từ chối oan.
- **Ảnh hưởng tới thành phần nào:** Module `src/transform/transformer.py` và `src/quality/checker.py`.
