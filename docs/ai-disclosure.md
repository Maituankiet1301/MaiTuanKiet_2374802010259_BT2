# PHỤ LỤC: BẢNG KHAI BÁO SỬ DỤNG CÔNG CỤ AI (BÀI TẬP 3 - GIAI ĐOẠN 3)
*(Bắt buộc đính kèm theo quy định học phần Chuyên đề tốt nghiệp 1 – Bài tập 3)*

**Học phần:** Chuyên đề tốt nghiệp 1 – Học kỳ 1, Năm học 2026 – 2027  
**Sinh viên thực hiện:** Mai Tuấn Kiệt  
**MSSV:** 2374802010259  
**Track:** Data Analytics (DA)  
**Luồng bài tập:** Luồng L6 – Kho dữ liệu bán hàng & Báo cáo doanh thu đa chiều  
**Case Study:** Mekong Mobile Smart CRM  
**Tag nộp bài:** `v1.0` | **Kho GitHub công khai:** [https://github.com/Maituankiet1301/MaiTuanKiet_2374802010259_BT2](https://github.com/Maituankiet1301/MaiTuanKiet_2374802010259_BT2)

---

### BẢNG KHAI BÁO CHI TIẾT SỬ DỤNG CÔNG CỤ AI CHO GIAI ĐOẠN 3 (BÀI TẬP 3)

| Công cụ AI | Dùng vào việc gì cụ thể | Áp dụng ở tệp / hàm nào | Em đã kiểm chứng thế nào? |
| :--- | :--- | :--- | :--- |
| **Claude / ChatGPT / Antigravity AI** | Hỗ trợ rà soát cấu trúc Dockerfile tối ưu kích thước image và cú pháp directive `HEALTHCHECK` kiểm tra trạng thái Streamlit. | `Dockerfile`, `docker-compose.yml` | Kiểm tra cú pháp theo chuẩn Docker Reference; tự xây dựng container và đối chiếu lệnh kiểm tra healthcheck `curl -f http://localhost:8501/_stcore/health` trả về mã 200 OK. |
| **Claude / ChatGPT / Antigravity AI** | Gợi ý cấu trúc dàn ý chuẩn tiếng Anh cho tài liệu kỹ thuật chuyên ngành Kỹ thuật dữ liệu (Pipeline Doc 6 mục, Data Dictionary, Deployment Guide 5 mục). | `docs/deployment-guide.md`, `docs/pipeline-doc.md`, `docs/data-dictionary.md` | Tự rà soát và đối chiếu từng bảng, từng cột với lược đồ thật trong CSDL DuckDB (`DESCRIBE table`); tính toán số dòng reject (5 orders, 1 item) khớp 100% với nhật ký chạy thực tế. |
| **Claude / ChatGPT / Antigravity AI** | Gợi ý bố cục CSS in ấn `@page` và cấu trúc Flexbox hiện đại để xuất file PDF báo cáo chuẩn A4 không bị vỡ bảng hay tràn trang. | `ho_so_bt3/build_bt3_pdf.ps1`, `ho_so_bt3/HO_SO_BT3_HOAN_CHINH.html` | Chạy lệnh xuất PDF bằng Google Chrome headless; mở kiểm tra từng trang trên trình đọc PDF để xác nhận căn lề, số trang, ngắt dòng và độ sắc nét của hình ảnh minh chứng. |
| **— Không dùng — (Tự làm hoàn toàn)** | Hiện thực hóa toàn bộ mã nguồn pipeline ETL (`src/extract`, `src/transform`, `src/load`, `src/quality`); thiết kế 12 test case chuyên sâu; phân tích 5 bug log thực tế; lập luận nghiệp vụ về tác động của các bản ghi reject. | Toàn bộ module `src/`, tệp `tests/test_pipeline.py`, `docs/bug-log.md`, `docs/test-plan.md`, `docs/test-report.md` | Tự chạy toàn bộ kiểm thử `pytest -v` đạt 12/12 PASS (100%); kiểm tra tính idempotent nạp lại lần 2 bằng chính xác 3.144 dòng; tự điều tra nguyên nhân gốc rễ và commit sửa từng bug. |

---

### LỜI CAM KẾT LIÊM CHÍNH HỌC THUẬT

> **"Tôi xác nhận đã đọc, hiểu và chịu trách nhiệm về toàn bộ nội dung nộp trong báo cáo và kho mã nguồn này."**

- **Họ và tên sinh viên:** Mai Tuấn Kiệt  
- **Mã số sinh viên (MSSV):** 2374802010259  
- **Ngày khai báo:** 17/11/2026  
