# KẾ HOẠCH KIỂM THỬ RÚT GỌN (TEST PLAN - LUỒNG L6)
**Hệ thống:** Mekong Mobile Smart CRM – Phân hệ Kho dữ liệu bán hàng & Báo cáo doanh thu đa chiều  
**Sinh viên thực hiện:** Mai Tuấn Kiệt | **MSSV:** 2374802010259 | **Track:** Data Analytics (DA)  
**Học phần:** Chuyên đề tốt nghiệp 1 – Học kỳ 1 (2026 – 2027) | **Buổi 14:** Workshop Kiểm thử hệ thống cá nhân  
**Giảng viên chấm:** TS. Nguyễn Trí Hải / ThS. Nguyễn Minh Tân / ThS. Trần Công Thanh  

---

## MỤC 1. PHẠM VI VÀ PHẦN CHỦ Ý KHÔNG KIỂM THỬ (SCOPE & OUT-OF-SCOPE)

### 1.1. Phạm vi kiểm thử (In-Scope)
- **Tầng Trích xuất (Extract Layer):** Đọc an toàn các tệp CSV nguồn từ 24 chi nhánh; cơ chế tìm kiếm fallback; kiểm soát ngoại lệ tệp rỗng (0 bytes) hoặc không có dữ liệu.
- **Tầng Kiểm soát chất lượng (Quality Layer):** Bộ 6 hàm kiểm tra độc lập (CL1–CL5, QT-01–QT-05) gồm: tính hợp lệ ngày giao dịch (CL2), tính hợp lệ tiền tệ (CL1), tính nhất quán sai số thành tiền $\le 1$ đ (CL4), tính toàn vẹn tham chiếu cửa hàng (CL5), tính duy nhất khóa phức hợp (CL3), và chuẩn hóa số điện thoại (QT-04).
- **Tầng Biến đổi (Transform Layer):** Chuẩn hóa ngày ISO-8601; che số điện thoại bảo mật 4 số cuối `090123****` (NFR3); phân tách dữ liệu sạch nạp Fact và dữ liệu lỗi vào các bảng Reject (`reject_orders`, `reject_order_items`); ánh xạ mã sản phẩm lạ vào `product_key = -1` (Unknown Dimension).
- **Tầng Nạp kho (Load Layer & DWH):** Nạp Star Schema vào DuckDB; bảo toàn tuyệt đối tính **Idempotent** (chạy lại nhiều lần không nhân đôi dòng); không phát sinh xung đột khóa chính khi nạp nhiều batch liên tiếp; ghi nhật ký kiểm toán ETL (`etl_audit_log`).
- **Giao diện & Bảo mật (Dashboard & Security):** Kiểm tra cơ chế băm mật khẩu SHA-256 kèm Salt; xử lý an toàn chuỗi ký tự đặc biệt / SQL Injection probe.

### 1.2. Phần chủ ý KHÔNG kiểm thử (Deliberate Out-of-Scope theo MoSCoW)
- **Chủ ý không kiểm thử tải đồng thời phân tán (High Concurrency Load Testing):** Do hệ thống sử dụng DuckDB dạng file nhúng phục vụ phân tích OLAP nội bộ, không kiểm thử tình huống hàng nghìn kết nối ghi đồng thời cùng lúc (thuộc phạm vi hệ quản trị OLTP phân tán).
- **Chủ ý không kiểm thử hạ tầng Cloud đa vùng:** Theo phân loại MoSCoW, phạm vi BT2/BT3 tập trung vào đóng gói Docker cục bộ tái lập được 100% trên máy tính cá nhân; không kiểm thử triển khai Cloud công khai (AWS/GCP đa vùng).
- **Chủ ý không kiểm thử thuật toán Machine Learning phức tạp:** Các mô hình dự đoán rời mạng khách hàng (Customer Churn Prediction) thuộc phạm vi học phần Chuyên đề tốt nghiệp 2.

---

## MỤC 2. LOẠI TEST VÀ SỐ LƯỢNG MỖI TẦNG (TEST LEVELS & SUITE COMPOSITION)

Bộ kiểm thử gồm **12 Test Cases độc lập**, phân bổ toàn diện qua **5 loại kiểm thử bắt buộc** của Track Data Analytics (DA):

| STT Loại kiểm thử | Mục đích kiểm thử | Mã Test Case | Số lượng | Tầng kiến trúc kiểm thử |
|:---|:---|:---:|:---:|:---|
| **1. Luồng đúng (Normal Flow)** | Kiểm thử hệ thống xử lý hoàn hảo dữ liệu sạch, nạp đủ số dòng, bảo toàn doanh thu và ánh xạ khóa chiều chính xác. | TC-01, TC-02 | 2 ca | Extract, Transform, Load, Dimension Mapping |
| **2. Giá trị biên (Boundary Value)** | Kiểm thử ở 2 bên ranh giới quy tắc nghiệp vụ QT-03: sai số cho phép $\le 1$đ (biên 0đ, +1đ, -1đ) và vượt ngưỡng biên (+2đ, -2đ). | TC-03, TC-04 | 2 ca | Quality Layer, Transform Layer, Reject Routing |
| **3. Dữ liệu sai (Invalid Data)** | Kiểm thử tính năng từ chối an toàn (Graceful Rejection): ngày ảo/ngoài biên, chuỗi tiền hỏng/số âm, mã chi nhánh không tồn tại; không làm sập pipeline. | TC-05, TC-06, TC-07 | 3 ca | Quality Layer, Transform Layer, Error Isolation |
| **4. Bảo mật & Chất lượng (Security & DQ)** | Kiểm tra che dữ liệu SĐT NFR3 (`090123****`), bộ kiểm tra chất lượng tự động cảnh báo, và xử lý an toàn injection ký tự đặc biệt. | TC-08, TC-09, TC-10 | 3 ca | Security, Presentation, Quality Suite, DWH Layer |
| **5. Tái lập & Ổn định (Reproducibility)** | Kiểm thử tính Idempotent khi chạy nạp 2 lần liên tiếp không nhân đôi dòng, và khả năng chịu lỗi khi gặp tệp CSV rỗng 0 bytes. | TC-11, TC-12 | 2 ca | Load Layer (DuckDB), Extract Layer, Pipeline Robustness |
| **TỔNG CỘNG** | **Bao phủ trọn vẹn 5 loại kiểm thử chuyên sâu cho Track DA** | **TC-01 → TC-12** | **12 ca** | **Toàn bộ 6 tầng Pipeline ETL & DWH** |

---

## MỤC 3. TIÊU CHÍ THÀNH CÔNG ĐO ĐƯỢC (MEASURABLE SUCCESS CRITERIA)

Mọi ca kiểm thử phải đạt kết quả định lượng cụ thể, kiểm chứng được bằng số đo:
1. **Tỷ lệ vượt qua kiểm thử (Pass Rate):** Đạt **100% (12/12 Test Cases PASSED)** bằng một câu lệnh duy nhất: `pytest -v` (hoặc `pytest -q`).
2. **Tính Idempotent tuyệt đối:** Khi chạy liên tiếp pipeline 2 lần trên cùng tập dữ liệu, số dòng bảng `fact_sales` lần 2 bằng chính xác số dòng lần 1: **3.144 dòng $\rightarrow$ 3.144 dòng (Độ lệch = 0 dòng)**.
3. **Hiệu năng thực thi (NFR1):** Thời gian thực thi toàn bộ pipeline $\le$ 45 giây (kết quả đo lường thực tế đạt **~1.41 giây**, vượt 96% yêu cầu chuẩn). Thời gian chạy trọn bộ 12 test cases $\le$ 5 giây (thực tế **~1.62 giây**).
4. **Bảo mật dữ liệu cá nhân (NFR3):** **100%** số điện thoại khách hàng hợp lệ trên bảng `dim_customer` và giao diện Dashboard phải được che 4 số cuối dạng `090123****`. Mật khẩu người dùng được băm an toàn SHA-256.
5. **Khả năng chịu lỗi & Không crash:** **0% unhandled exception** khi tiếp nhận tệp dữ liệu rỗng (0 bytes) hoặc dữ liệu sai lệch; 100% bản ghi vi phạm được cách ly vào các bảng `reject_orders` và `reject_order_items`.

---

## MỤC 4. MÔI TRƯỜNG VÀ DỮ LIỆU THỬ (ENVIRONMENT & TEST DATA)

### 4.1. Môi trường kiểm thử
- **Hệ điều hành:** Windows 11 (Tương thích 100% Linux Ubuntu 22.04 qua CI GitHub Actions).
- **Ngôn ngữ & Phiên bản:** Python 3.11.9.
- **Hệ quản trị CSDL:** DuckDB 2.0.0 (File nhúng `data/dwh_mekong.duckdb` & In-memory DuckDB cho fixtures).
- **Thư viện kiểm thử:** `pytest==9.2.0`, `pluggy==1.7.0`, `pandas==3.1.1`.
- **Cấu hình môi trường:** Tệp `pytest.ini` chỉ định `pythonpath = .` và `testpaths = tests`, đảm bảo tính tái lập 100% từ môi trường sạch.

### 4.2. Dữ liệu thử & Kỹ thuật chọn dữ liệu
- **Dữ liệu Fixture tự sinh trong bộ nhớ (In-memory Mock Fixtures):** Bộ kiểm thử sử dụng `sample_valid_data` và `tmp_path` tự động cấp phát và giải phóng sau mỗi ca test, hoàn toàn độc lập và không phụ thuộc vào dữ liệu có sẵn trên máy của giảng viên.
- **Kỹ thuật Phân vùng tương đương (Equivalence Partitioning):**
  + *Ngày giao dịch:* Phân vùng hợp lệ (2020..2027 với các định dạng dd/mm/yyyy, d-m-y, d-m-Y, yyyy.mm.dd, ISO); Phân vùng không hợp lệ (ngày ảo 31/02, năm trước 2020, chuỗi chữ).
  + *Tiền tệ:* Phân vùng hợp lệ (chuỗi số nguyên dương kèm đ/vnd/chấm/phẩy/khoảng trắng); Phân vùng không hợp lệ (chuỗi chữ cái, số âm).
  + *Mã cửa hàng:* Phân vùng hợp lệ (`CH01`..`CH24`); Phân vùng không hợp lệ (`CH99_UNKNOWN`).
- **Kỹ thuật Phân tích giá trị biên (Boundary Value Analysis):**
  + *Quy tắc QT-03 (Sai số thành tiền $\le 1$đ):* Kiểm tra tại 5 điểm: 
    * $-2$ đ: Vượt biên dưới $\rightarrow$ REJECT.
    * $-1$ đ: Ranh giới biên dưới cho phép $\rightarrow$ PASS.
    * $0$ đ: Khớp hoàn hảo $\rightarrow$ PASS.
    * $+1$ đ: Ranh giới biên trên cho phép $\rightarrow$ PASS.
    * $+2$ đ: Vượt biên trên $\rightarrow$ REJECT.
  + *Kích thước tệp nguồn:* 0 bytes (tệp rỗng) vs $> 0$ bytes (tệp có dữ liệu).
