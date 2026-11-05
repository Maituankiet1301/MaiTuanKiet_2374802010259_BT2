# PHỤ LỤC: BẢNG KHAI BÁO SỬ DỤNG CÔNG CỤ AI (BÀI TẬP 2)
*(Bắt buộc đính kèm theo quy định học phần Chuyên đề tốt nghiệp 1 – Bài tập 2)*

**Học phần:** Chuyên đề tốt nghiệp 1 – Học kỳ 1, Năm học 2026 – 2027  
**Sinh viên thực hiện:** Mai Tuấn Kiệt  
**MSSV:** 2374802010259  
**Track:** Data Analytics (DA)  
**Luồng bài tập:** Luồng L6 – Kho dữ liệu bán hàng & Báo cáo doanh thu đa chiều  
**Case Study:** Mekong Mobile Smart CRM  

---

### BẢNG KHAI BÁO CHI TIẾT SỬ DỤNG CÔNG CỤ AI CHO BÀI TẬP 2

| Công cụ AI | Dùng vào việc gì cụ thể | Áp dụng ở tệp / hàm nào | Em đã kiểm chứng thế nào? |
| :--- | :--- | :--- | :--- |
| **Claude / ChatGPT / Antigravity AI** | Gợi ý cấu trúc giải thuật nạp idempotent trong DuckDB bằng chiến lược Delete/Insert theo bộ ba khóa tự nhiên. | `src/load/loader.py`, hàm `load_fact_sales` và `load_dimensions` | Đọc tài liệu chính thức của DuckDB về giao dịch ACID; viết kịch bản kiểm thử `test_case_4_idempotent_double_run` trong `tests/test_pipeline.py`; chạy pipeline 2 lần liên tiếp và truy vấn `COUNT(*)` để xác minh số dòng không bị nhân đôi. |
| **Claude / ChatGPT / Antigravity AI** | Gợi ý biểu thức chính quy (Regex) và thứ tự ưu tiên parse 3 định dạng ngày tháng thực tế (`%d/%m/%Y`, `%d-%m-%y`, `%Y.%m.%d`). | `src/quality/checker.py`, hàm `parse_date_flexibly` và `clean_phone_str` | Viết unit test cho các định dạng ngày biên (ngày đầu năm 2020, ngày nhuận 29/02/2024, ngày sai 31/02/2025); chạy trên tập 2.058 đơn hàng thực tế để kiểm tra tỷ lệ thành công. |
| **Claude / ChatGPT / Antigravity AI** | Gợi ý mẫu layout 3 trạng thái (Loading, Empty, Error) và cấu hình theme Plotly cho Streamlit. | `app.py`, các khối `st.spinner`, kiểm tra `df_filtered.empty` và khối `try...except` kết nối CSDL | Tự tạo 2 checkbox toggle trên Sidebar: *"🔴 Giả lập Lỗi kết nối CSDL"* và *"🟡 Giả lập Bộ lọc rỗng"* để kích hoạt và kiểm tra trực quan giao diện ứng xử đúng theo rubric chấm điểm; đảm bảo chuỗi kết nối tuyệt đối không bị lộ. |
| **— Không dùng — (Tự làm hoàn toàn)** | Thiết kế kiến trúc phân lớp `extract / transform / quality / load`; xây dựng 6 hàm đo lường chất lượng dữ liệu; thiết kế lược đồ Star Schema chuẩn Kimball; lập luận nghiệp vụ phân tích câu hỏi CH1, CH2, CH4. | Toàn bộ cấu trúc dự án `src/`, file `sql/schema.sql`, kịch bản sinh dữ liệu mẫu `seeds/generate_seeds.py` | Tự thiết kế và đối chiếu trực tiếp với Hồ sơ Bài tập 1 đã nộp; tự viết toàn bộ câu truy vấn phân tích SQL sụt giảm 3 tháng liên tiếp (`LAG window function`) và chạy kiểm thử pytest đạt 100% PASS. |

---

### LỜI CAM KẾT LIÊM CHÍNH HỌC THUẬT

> **"Tôi xác nhận đã đọc, hiểu và chịu trách nhiệm về toàn bộ nội dung nộp trong báo cáo và kho mã nguồn này."**

- **Họ và tên sinh viên:** Mai Tuấn Kiệt  
- **Mã số sinh viên (MSSV):** 2374802010259  
- **Ngày khai báo:** 05/11/2026  
