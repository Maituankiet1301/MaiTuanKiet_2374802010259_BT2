# NHẬT KÝ THEO DÕI VÀ SỬA LỖI (BUG LOG - LUỒNG L6)
**Học phần:** Chuyên đề tốt nghiệp 1 – Học kỳ 1, Năm học 2026 – 2027  
**Phân hệ / Luồng nghiệp vụ:** Luồng L6 – Kho dữ liệu bán hàng & Báo cáo doanh thu đa chiều (Smart CRM - Mekong Mobile)  
**Sinh viên thực hiện:** Mai Tuấn Kiệt | **MSSV:** 2374802010259 | **Track:** Data Analytics (DA)  
**Kho mã nguồn chính thức (PUBLIC):** `https://github.com/Maituankiet1301/MaiTuanKiet_2374802010259_BT2`  
**Quy ước ghi:** Mỗi bug ghi đúng 7 dòng chuẩn theo hướng dẫn Buổi 13 & Buổi 14, link commit mở được trực tiếp trên GitHub.

---

### BUG-01 (Mức độ: Major — Người khác clone repo về không dựng và chạy được bộ kiểm thử tự động)
- **1. Mã và Mức độ:** BUG-01 · Mức độ: **Major** *(Tiêu chí: Người dùng/giảng viên clone repo về không thể chạy bộ kiểm thử tự động `pytest` theo README, làm tắc nghẽn hoàn toàn quy trình nghiệm thu chất lượng mã nguồn).*
- **2. Phát hiện bởi:** Giảng viên khi chạy thử repo ở buổi 12 / Kiểm thử clone môi trường sạch.
- **3. Triệu chứng:** Chạy lệnh `pytest` hoặc `pytest -q` từ thư mục gốc bị dừng thu thập với thông báo: `ModuleNotFoundError: No module named 'src'` (0 items collected / 1 error).
- **4. Cách tái lập:** Clone repo sang thư mục mới, tạo môi trường ảo Python 3.11, cài `pip install -r requirements.txt`, sau đó gõ lệnh `pytest` trong terminal.
- **5. Nguyên nhân gốc rễ:** Repo thiếu tệp cấu hình `pytest.ini` chỉ định `pythonpath = .`, khiến pytest khi thực thi file nhị phân không tự động đưa thư mục gốc dự án vào đường dẫn tìm kiếm `sys.path` của Python.
- **6. Cách sửa:** Tạo tệp `pytest.ini` tại thư mục gốc với nội dung `pythonpath = .` và `testpaths = tests`, cập nhật `README.md` chỉ dẫn lệnh chạy kiểm thử chuẩn `pytest -v` hoặc `pytest -q`.
- **7. Commit và xác nhận:** Commit `2a1d0b28af804c1395cbdf8ec3407b46dfc0da85` · Link: [2a1d0b2](https://github.com/Maituankiet1301/MaiTuanKiet_2374802010259_BT2/commit/2a1d0b28af804c1395cbdf8ec3407b46dfc0da85) · Xác nhận: Chạy `pytest -v` từ thư mục gốc thành công 100%, thu thập đầy đủ các ca kiểm thử.

---

### BUG-02 (Mức độ: Critical — Xung đột khóa chính làm sập pipeline nạp dữ liệu ở các mẻ nạp gia tăng)
- **1. Mã và Mức độ:** BUG-02 · Mức độ: **Critical** *(Tiêu chí: Hệ thống bị đình trệ hoàn toàn khi nạp mẻ dữ liệu gia tăng, vi phạm tính toàn vẹn CSDL và làm hỏng khả năng vận hành liên tục của kho dữ liệu).*
- **2. Phát hiện bởi:** Sinh viên khi kiểm thử nạp nhiều batch liên tiếp trên kho dữ liệu thực tế (TC-11).
- **3. Triệu chứng:** Khi nạp batch thứ 2 có dữ liệu mới hoặc đơn hàng lỗi mới, DuckDB quăng ngoại lệ: `Constraint Error: Duplicate key "sales_fact_key: 100001" violates primary key constraint` (hoặc `Duplicate key "reject_id: 1001"`), làm sập toàn bộ pipeline.
- **4. Cách tái lập:** Nạp batch 1 có bản ghi Fact và Reject. Tạo batch 2 với đơn hàng mới khác biệt và gọi `loader.load_fact_sales()` hoặc `loader.load_rejects()`.
- **5. Nguyên nhân gốc rễ:** Trong `src/transform/transformer.py`, các biến đếm surrogate key (`fact_key_counter = 100000`, `reject_order_counter = 1000`, `reject_item_counter = 5000`) được khởi tạo tĩnh cố định trong bộ nhớ tại mỗi phiên khởi tạo class, không truy vấn giá trị ID lớn nhất hiện hữu trong CSDL (`COALESCE(MAX(...), base)`), dẫn đến việc batch sau gán trùng ID đã cấp ở batch trước.
- **6. Cách sửa:** Bổ sung phương thức `get_max_keys()` trong `DWHLoader` để truyền ID lớn nhất hiện hữu cho `DataTransformer`; đồng thời nâng cấp câu lệnh SQL `INSERT` sử dụng biểu thức `CASE WHEN key IN (SELECT key ...) THEN MAX(...) + ROW_NUMBER() OVER () ELSE key END` để bảo vệ 2 lớp chống đè khóa.
- **7. Commit và xác nhận:** Commit `5f12f88c588cd949b8abead92d4def63ba7b4b65` · Link: [5f12f88](https://github.com/Maituankiet1301/MaiTuanKiet_2374802010259_BT2/commit/5f12f88c588cd949b8abead92d4def63ba7b4b65) · Xác nhận: Chạy kiểm thử multi-batch 2 mẻ độc lập thành công 100%, số dòng cộng dồn chuẩn xác không bị lỗi duplicate key.

---

### BUG-03 (Mức độ: Major — Tệp CSV rỗng 0 bytes làm sập toàn bộ pipeline trích xuất dữ liệu)
- **1. Mã và Mức độ:** BUG-03 · Mức độ: **Major** *(Tiêu chí: Khi một chi nhánh truyền tệp rỗng do lỗi mạng, toàn bộ chuỗi xử lý ETL của 23 chi nhánh còn lại bị sập, hệ thống thiếu cơ chế tự phục hồi và khả năng chịu lỗi).*
- **2. Phát hiện bởi:** Sinh viên khi chạy ca kiểm thử độ ổn định (TC-12: Xử lý an toàn tệp rỗng).
- **3. Triệu chứng:** Khi gặp tệp CSV rỗng kích thước 0 bytes trong thư mục dữ liệu nguồn, `pd.read_csv()` quăng ngoại lệ `pandas.errors.EmptyDataError: No columns to parse from file`, làm sập chương trình.
- **4. Cách tái lập:** Tạo một tệp CSV rỗng kích thước 0 bytes trong thư mục `data/raw/` (hoặc fixture), sau đó khởi chạy `extractor.extract_all()`.
- **5. Nguyên nhân gốc rễ:** `DataExtractor` không kiểm tra kích thước tệp trước khi đọc và không bắt ngoại lệ `pd.errors.EmptyDataError`, thiếu cơ chế tạo DataFrame rỗng dự phòng có đầy đủ các cột lược đồ chuẩn.
- **6. Cách sửa:** Xây dựng hàm `_read_csv_safe` trong `DataExtractor` bọc quanh `pd.read_csv` với kiểm tra kích thước file (`os.path.getsize == 0`) và bắt ngoại lệ `EmptyDataError`, ghi log cảnh báo và trả về DataFrame rỗng có cấu trúc cột chuẩn tương ứng với từng loại bảng.
- **7. Commit và xác nhận:** Commit `1541cdf03112e5659eeee5f63a687bd585aca683` · Link: [1541cdf](https://github.com/Maituankiet1301/MaiTuanKiet_2374802010259_BT2/commit/1541cdf03112e5659eeee5f63a687bd585aca683) · Xác nhận: Chạy TC-12 với 4 tệp rỗng 0 bytes hoàn tất an toàn, trả về 0 dòng Fact mà không gây crash pipeline.

---

### BUG-04 (Mức độ: Major — Lộ mật khẩu dạng Plaintext trong mã nguồn ứng dụng Dashboard)
- **1. Mã và Mức độ:** BUG-04 · Mức độ: **Major** *(Tiêu chí: Lỗ hổng an toàn thông tin OWASP A07 - Identification and Authentication Failures, vi phạm tiêu chuẩn bảo mật NFR3 khi public repo trên GitHub).*
- **2. Phát hiện bởi:** Rà soát mã nguồn theo checklist bảo mật buổi 14 & yêu cầu công khai repo BT3.
- **3. Triệu chứng:** Mở tệp `app.py`, từ điển `USERS` lưu trực tiếp mật khẩu ở dạng văn bản thô: `"password": "admin123"`, `"password": "manager123"`, `"password": "data123"`.
- **4. Cách tái lập:** Mở tệp `app.py` từ dòng 36 đến dòng 40, nhìn thấy trực tiếp mật khẩu của cả 3 vai trò quản trị.
- **5. Nguyên nhân gốc rễ:** Triển khai cơ chế xác thực demo ban đầu mà chưa áp dụng cơ chế băm mật khẩu một chiều (cryptographic hashing) và chưa hỗ trợ đọc cấu hình từ biến môi trường.
- **6. Cách sửa:** Sử dụng thư viện `hashlib` để băm mật khẩu bằng thuật toán SHA-256 kết hợp chuỗi Salt bí mật (`AUTH_SALT`), so khớp chuỗi băm thay vì so khớp plaintext; đồng thời hỗ trợ nạp cấu hình tài khoản quản trị từ biến môi trường qua `os.getenv`.
- **7. Commit và xác nhận:** Commit `076b49f0017263d871e4b8be930c5ef8aed05596` · Link: [076b49f](https://github.com/Maituankiet1301/MaiTuanKiet_2374802010259_BT2/commit/076b49f0017263d871e4b8be930c5ef8aed05596) · Xác nhận: Đăng nhập Dashboard với mật khẩu chính xác thành công, nhập sai bị từ chối; mã nguồn không còn chứa bất kỳ plaintext secret nào.

---

### BUG-05 (Mức độ: Major — Lỗi `KeyError: 'ma_cua_hang'` khi dữ liệu chi tiết rỗng và thiếu định dạng ngày d-m-Y)
- **1. Mã và Mức độ:** BUG-05 · Mức độ: **Major** *(Tiêu chí: Pipeline bị crash khi tiếp nhận lô đơn hàng không có chi tiết dòng hàng hợp lệ; đồng thời từ chối nhầm các ngày hợp lệ viết theo chuẩn Việt Nam dd-mm-yyyy).*
- **2. Phát hiện bởi:** Chạy ca kiểm thử dữ liệu sai TC-05, TC-06, TC-07 khi truyền `order_items` rỗng.
- **3. Triệu chứng:** Hàm `transform_all` quăng lỗi `KeyError: 'ma_cua_hang'` tại dòng `df_items_raw.groupby(["ma_cua_hang", "ma_don"])`; các ngày dạng `15-03-2024` bị từ chối oan thành `INVALID_DATE_FORMAT`.
- **4. Cách tái lập:** Chạy `transformer.transform_all` với DataFrame `order_items` rỗng hoặc không có cột `ma_cua_hang`.
- **5. Nguyên nhân gốc rễ:** Không kiểm tra `df_items_raw.empty` trước khi gọi `groupby`; danh sách format trong `parse_date_flexibly` chỉ có `%d-%m-%y` (2 số năm) mà thiếu `%d-%m-%Y` (4 số năm có gạch ngang).
- **6. Cách sửa:** Bổ sung điều kiện kiểm tra nếu `df_items_raw.empty` hoặc thiếu cột khóa thì gán `grouped_items = []`; bổ sung chuỗi định dạng `"%d-%m-%Y"` vào `parse_date_flexibly`.
- **7. Commit và xác nhận:** Commit `83766a061cef252ec5cf537a8f163fead6b18129` · Link: [83766a0](https://github.com/Maituankiet1301/MaiTuanKiet_2374802010259_BT2/commit/83766a061cef252ec5cf537a8f163fead6b18129) · Xác nhận: Cả 3 test case TC-05, TC-06, TC-07 đều chạy PASSED mượt mà.
