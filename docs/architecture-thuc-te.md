# SƠ ĐỒ KIẾN TRÚC THỰC TẾ ĐÃ HIỆN THỰC (BÀI TẬP 2)
**Học phần:** Chuyên đề tốt nghiệp 1 – Học kỳ 1, Năm học 2026 – 2027  
**Phân hệ / Luồng nghiệp vụ:** Luồng L6 – Kho dữ liệu bán hàng & Báo cáo doanh thu đa chiều  
**Sinh viên thực hiện:** Mai Tuấn Kiệt | **MSSV:** 2374802010259 | **Track:** Data Analytics (DA)  

---

## 1. Sơ đồ Kiến trúc Phân tầng Thực tế (Architecture Layers)

```mermaid
flowchart TD
    subgraph SOURCELAYER ["1. TẦNG NGUỒN DỮ LIỆU (DATA SOURCES - CSV/SEEDS)"]
        S1["stores.csv (24 cửa hàng)"]
        S2["products.csv (Danh mục sản phẩm)"]
        S3["orders_2024_2026.csv (~2.058 đơn hàng)"]
        S4["order_items.csv (~3.146 dòng chi tiết)"]
    end

    subgraph EXTRACTLAYER ["2. TẦNG TRÍCH XUẤT (SRC/EXTRACT)"]
        E1["DataExtractor (extractor.py)\n- Quét thư mục data/raw/ và seeds/\n- Xử lý mất file an toàn (Graceful Fallback)\n- Đọc dữ liệu thô vào Pandas DataFrame"]
    end

    subgraph QUALITYLAYER ["3. TẦNG KIỂM SOÁT CHẤT LƯỢNG (SRC/QUALITY)"]
        Q1["check_date_validity() -> (count, rate)"]
        Q2["check_currency_amount() -> (count, rate)"]
        Q3["check_line_total_consistency() -> (count, rate)"]
        Q4["check_referential_integrity() -> (count, rate)"]
        Q5["check_uniqueness() -> (count, rate)"]
        Q6["check_phone_validity() -> (count, rate)"]
        QReport["Báo cáo chất lượng (Data Quality Report)"]
    end

    subgraph TRANSFORMLAYER ["4. TẦNG BIẾN ĐỔI & PHÂN LOẠI (SRC/TRANSFORM)"]
        T1["DataTransformer (transformer.py)"]
        T2["Chuẩn hóa ngày: %d/%m/%Y, %d-%m-%y, %Y.%m.%d -> ISO"]
        T3["Làm sạch chuỗi tiền: Bỏ 'đ', ép BIGINT"]
        T4["Bảo mật: Che 4 số cuối SĐT (090123****)"]
        T5["Tách luồng dữ liệu"]
    end

    subgraph DWHLAYER ["5. TẦNG KHO DỮ LIỆU DUCKDB (DATA WAREHOUSE & STAR SCHEMA)"]
        direction TB
        subgraph DIMENSIONS ["Các bảng chiều (Dimensions)"]
            D1["dim_date (731 dòng)"]
            D2["dim_store (24 dòng)"]
            D3["dim_product (25 dòng - kèm Unknown -1)"]
            D4["dim_customer (11 dòng - kèm Vãng lai 0)"]
        end
        subgraph FACT ["Bảng sự kiện (Fact Table)"]
            F1["fact_sales (3.144 dòng)\n- Grain: 1 sản phẩm / 1 đơn / 1 cửa hàng / 1 ngày\n- Idempotent: UNIQUE(store_id, order_id, line_item_id)"]
        end
        subgraph REJECT ["Bảng cách ly lỗi (Reject Tables)"]
            R1["reject_orders (5 đơn lỗi)\n- INVALID_DATE_FORMAT\n- CORRUPTED_CURRENCY_STRING\n- UNKNOWN_STORE_ID"]
            R2["reject_order_items (1 dòng lỗi)\n- INCONSISTENT_LINE_TOTAL"]
        end
        subgraph AUDIT ["Nhật ký kiểm toán"]
            A1["etl_audit_log (Lưu vết từng batch ETL)"]
        end
    end

    subgraph PRESENTATIONLAYER ["6. TẦNG TRÌNH DIỄN & DASHBOARD (APP.PY - STREAMLIT)"]
        UI1["Streamlit Revenue Dashboard"]
        UI2["CH1: Doanh thu theo tháng/ngày kèm Benchmark"]
        UI3["CH2: Cảnh báo cửa hàng giảm 3 tháng liên tiếp"]
        UI4["CH4: Cơ cấu danh mục sản phẩm theo quý"]
        UI_States["Xử lý 3 Trạng thái:\n1. Đang truy vấn (Loading)\n2. Bộ lọc rỗng (Empty Filter / Empty DB)\n3. Lỗi kết nối CSDL (Error State)"]
    end

    %% Luồng liên kết dữ liệu
    SOURCELAYER --> EXTRACTLAYER
    EXTRACTLAYER --> QUALITYLAYER
    QUALITYLAYER --> TRANSFORMLAYER
    TRANSFORMLAYER -->|Dữ liệu sạch| DIMENSIONS
    TRANSFORMLAYER -->|Dữ liệu sạch| FACT
    TRANSFORMLAYER -->|Dữ liệu vi phạm quy tắc| REJECT
    TRANSFORMLAYER -->|Thông số vận hành| AUDIT

    DIMENSIONS --> PRESENTATIONLAYER
    FACT --> PRESENTATIONLAYER
    DWHLAYER -.->|Truy vấn SQL DuckDB| PRESENTATIONLAYER
```

---

## 2. Vị trí các thành phần trong Thư mục Dự án

| Thành phần kiến trúc | Tệp mã nguồn thực tế | Trách nhiệm và Chức năng chính |
| :--- | :--- | :--- |
| **Pha Trích xuất (Extract)** | `src/extract/extractor.py` | Quét và đọc 4 file CSV dữ liệu từ `data/raw/` hoặc `seeds/`. |
| **Pha Kiểm soát chất lượng (Quality)** | `src/quality/checker.py` | 6 hàm kiểm tra chất lượng dữ liệu, mỗi hàm trả về số lượng dòng lỗi và tỷ lệ lỗi (CL1–CL5). |
| **Pha Biến đổi (Transform)** | `src/transform/transformer.py` | Chuẩn hóa ngày ISO, làm sạch tiền tệ, che 4 số cuối SĐT, phân tách bản ghi sạch và bản ghi reject. |
| **Pha Nạp dữ liệu (Load - Idempotent)** | `src/load/loader.py` | Nạp vào DuckDB Star Schema, thực thi chiến lược chống nhân đôi dữ liệu qua bộ ba khóa tự nhiên. |
| **Khởi chạy Pipeline** | `run_pipeline.py` | Điểm khởi chạy 1 lệnh duy nhất cho toàn bộ quá trình ETL và in báo cáo. |
| **Bộ kiểm thử tự động (Test Suite)** | `tests/test_pipeline.py` | 4 test cases (Luồng đúng, Giá trị biên, Dữ liệu sai, Tính Idempotent) chạy bằng `pytest`. |
| **Trình diễn kết quả (Dashboard)** | `app.py` | Dashboard Streamlit xử lý đủ 3 trạng thái (Loading, Empty, Error) và trả lời CH1, CH2, CH4. |
