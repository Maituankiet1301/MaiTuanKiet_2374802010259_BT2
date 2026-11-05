# BẢN GHI NHẬN THAY ĐỔI THIẾT KẾ (BT1 → BT2)
**Học phần:** Chuyên đề tốt nghiệp 1 – Học kỳ 1, Năm học 2026 – 2027  
**Phân hệ / Luồng nghiệp vụ:** Luồng L6 – Kho dữ liệu bán hàng & Báo cáo doanh thu đa chiều  
**Sinh viên thực hiện:** Mai Tuấn Kiệt | **MSSV:** 2374802010259 | **Track:** Data Analytics (DA)  
**Quy tắc:** Mỗi thay đổi ghi đúng 3 dòng: *Thay đổi gì · Vì sao · Ảnh hưởng tới thành phần nào*.

---

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
