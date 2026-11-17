# CHECKLIST BẢO MẬT BẢY MỤC (SECURITY CHECKLIST - OWASP TOP 10:2025)
## Hệ thống Smart CRM Mekong Mobile – Luồng L6 (Kho Dữ Liệu Bán Hàng & Báo Cáo Doanh Thu)
**Sinh viên thực hiện:** Mai Tuấn Kiệt | **MSSV:** 2374802010259 | **Track:** Data Analytics (DA)  
**Học phần:** Chuyên đề tốt nghiệp 1 – Học kỳ 1, Năm học 2026 – 2027  
**Quy ước đánh giá:** ĐÃ LÀM / CHƯA LÀM / KHÔNG ÁP DỤNG. Mỗi mục có đúng 1 dòng minh chứng cụ thể kèm file/hàm kiểm chứng.

---

| STT | Hạng mục kiểm tra bảo mật (Theo OWASP Top 10:2025 & Yêu cầu BT3) | Trạng thái thực hiện | Dòng minh chứng cụ thể (File, Hàm, Dòng mã & Cơ chế kiểm chứng) |
|:---:|:---|:---:|:---|
| **1** | **A01:2025 – Broken Access Control (Kiểm soát truy cập phân quyền)** | **ĐÃ LÀM** | Phân quyền 3 vai trò (Admin, Store Manager, Data Engineer) trong `app.py`; Manager CH01 chỉ được truy cập dữ liệu cửa hàng CH01, bị chặn truy cập số liệu 23 chi nhánh khác. |
| **2** | **A02:2025 – Security Misconfiguration (Cấu hình bảo mật sai / Lộ vết lỗi)** | **ĐÃ LÀM** | Khi CSDL lỗi (Error state trong `app.py`), giao diện bắt ngoại lệ trả về cảnh báo thân thiện, che dấu 100% stack trace, tên bảng nội bộ và chuỗi kết nối (đạt chuẩn NFR3). |
| **3** | **A04:2025 – Cryptographic Failures (Thất bại mã hóa / Lộ mật khẩu)** | **ĐÃ LÀM** | Mật khẩu tài khoản quản trị được băm một chiều an toàn bằng thuật toán SHA-256 kết hợp Salt bí mật (`AUTH_SALT`) trong hàm `hash_password()` của `app.py`, không lưu plaintext. |
| **4** | **A05:2025 – Injection (Lỗ hổng tiêm mã độc SQL / Script Injection)** | **ĐÃ LÀM** | Module `src/load/loader.py` sử dụng Parameterized Queries và cơ chế Appender nội tại của DuckDB; ca kiểm thử `TC-10` chứng minh chuỗi `Robert'); DROP TABLE fact_sales; --` không thể phá hoại schema. |
| **5** | **A07:2025 – Identification and Authentication Failures (Lỗ hổng xác thực)** | **ĐÃ LÀM** | Ứng dụng Dashboard yêu cầu đăng nhập bắt buộc qua biểu mẫu xác thực, lưu phiên trong `st.session_state`; mật khẩu sai bị từ chối ngay lập tức, hỗ trợ nạp credentials qua biến môi trường. |
| **6** | **Sensitive Data Exposure & PII Masking (Bảo vệ thông tin định danh cá nhân - D4)** | **ĐÃ LÀM** | Toàn bộ số điện thoại khách hàng trên bảng `dim_customer` và giao diện Dashboard được tự động che 4 số cuối dạng `090123****` qua hàm `mask_phone()` trong `src/transform/transformer.py` (kiểm chứng tại `TC-08`). |
| **7** | **Secret Management (Quản lý bí mật & Kho mã nguồn công khai)** | **ĐÃ LÀM** | Lệnh `git log --all --oneline -- .env` trả về rỗng chứng minh tệp `.env` chưa từng bị commit vào lịch sử git; tệp `.env.example` cung cấp đầy đủ biến môi trường không chứa secret thật. |

---

### BẢNG ĐỐI CHIẾU TIÊU CHÍ KỸ THUẬT VÀ MINH CHỨNG CHI TIẾT
1. **Kiểm tra Secret trong Git History (Tiêu chí C7):**
   ```powershell
   git log --all --oneline -- .env
   # Kết quả: Rỗng (Không có bản ghi commit nào chứa .env)
   ```
2. **Kiểm tra cơ chế Che số điện thoại PII (Tiêu chí D4):**
   ```python
   # File src/transform/transformer.py - hàm mask_phone
   def mask_phone(phone_str: str) -> str:
       if not phone_str or len(phone_str) < 7:
           return phone_str
       return phone_str[:-4] + "****"
   ```
3. **Kiểm tra cơ chế Băm mật khẩu (BUG-04 & OWASP A04):**
   ```python
   # File app.py - hàm hash_password
   def hash_password(password: str, salt: str = AUTH_SALT) -> str:
       return hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
   ```
4. **Kiểm tra chống SQL Injection (Tiêu chí A05 & TC-10):**
   Chạy `pytest -v tests/test_pipeline.py::test_tc10_bao_mat_chong_sql_injection_ky_tu_dac_biet` $\rightarrow$ **PASSED**.
