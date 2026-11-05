-- ==============================================================================
-- SCHEMA DEFINITION: MEKONG MOBILE DWH (LUỒNG L6) - STAR SCHEMA IN DUCKDB
-- Tác giả: Mai Tuấn Kiệt (MSSV: 2374802010259) - Track DA
-- ==============================================================================

-- 1. TẦNG STAGING (VÙNG ĐỆM TRÍCH XUẤT DỮ LIỆU THÔ)
CREATE TABLE IF NOT EXISTS stg_stores (
    ma_cua_hang VARCHAR,
    ten_cua_hang VARCHAR,
    tinh_thanh VARCHAR,
    khu_vuc VARCHAR,
    quan_ly VARCHAR,
    extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS stg_products (
    ma_san_pham VARCHAR,
    ten_san_pham VARCHAR,
    danh_muc VARCHAR,
    hang_san_xuat VARCHAR,
    gia_niem_yet BIGINT,
    extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS stg_orders (
    ma_don VARCHAR,
    ma_cua_hang VARCHAR,
    ngay_raw VARCHAR,
    sdt_raw VARCHAR,
    khach_hang_raw VARCHAR,
    thanh_tien_raw VARCHAR,
    nhan_vien VARCHAR,
    extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS stg_order_items (
    ma_don VARCHAR,
    ma_cua_hang VARCHAR,
    ma_san_pham VARCHAR,
    so_luong INT,
    don_gia BIGINT,
    thanh_tien BIGINT,
    extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. TẦNG DIMENSION (CÁC BẢNG CHIỀU THEO KIMBALL)

-- Chiều thời gian (dim_date)
CREATE TABLE IF NOT EXISTS dim_date (
    date_key INT PRIMARY KEY,              -- Định dạng YYYYMMDD (VD: 20240315)
    full_date DATE NOT NULL UNIQUE,        -- Định dạng chuẩn ISO-8601 (YYYY-MM-DD)
    day_of_month INT NOT NULL,
    month INT NOT NULL,
    quarter INT NOT NULL,
    year INT NOT NULL,
    day_name VARCHAR NOT NULL,
    is_weekend BOOLEAN NOT NULL
);

-- Chiều cửa hàng (dim_store)
CREATE TABLE IF NOT EXISTS dim_store (
    store_key INT PRIMARY KEY,             -- Surrogate Key tự sinh
    store_id VARCHAR NOT NULL UNIQUE,      -- Natural Key: CH01..CH24
    store_name VARCHAR NOT NULL,
    city VARCHAR NOT NULL,
    region VARCHAR NOT NULL,
    manager_name VARCHAR
);

-- Chiều sản phẩm (dim_product)
CREATE TABLE IF NOT EXISTS dim_product (
    product_key INT PRIMARY KEY,           -- Surrogate Key (-1: Chưa phân loại)
    product_code VARCHAR NOT NULL UNIQUE,  -- Natural Key: SP001..
    product_name VARCHAR NOT NULL,
    category VARCHAR NOT NULL,
    brand VARCHAR,
    standard_price BIGINT
);

-- Chiều khách hàng (dim_customer)
CREATE TABLE IF NOT EXISTS dim_customer (
    customer_key INT PRIMARY KEY,          -- Surrogate Key (0: Khách vãng lai)
    phone_number VARCHAR NOT NULL UNIQUE,  -- Số điện thoại 10 số đã chuẩn hóa
    customer_name VARCHAR,
    masked_phone VARCHAR,                  -- Che 4 số cuối: 090123**** (NFR3)
    is_valid_phone BOOLEAN NOT NULL
);

-- 3. TẦNG FACT (BẢNG SỰ KIỆN DOANH SỐ)
-- Grain: Một dòng đại diện cho một sản phẩm trong một đơn hàng tại một cửa hàng vào một ngày
CREATE TABLE IF NOT EXISTS fact_sales (
    sales_fact_key BIGINT PRIMARY KEY,     -- Surrogate Primary Key
    order_id VARCHAR NOT NULL,             -- Mã đơn hàng
    store_id VARCHAR NOT NULL,             -- Mã cửa hàng
    line_item_id INT NOT NULL,             -- Thứ tự mặt hàng trong đơn
    date_key INT NOT NULL,                 -- FK -> dim_date
    store_key INT NOT NULL,                -- FK -> dim_store
    product_key INT NOT NULL,              -- FK -> dim_product
    customer_key INT NOT NULL,             -- FK -> dim_customer
    quantity INT NOT NULL,                 -- Measure: Số lượng
    unit_price BIGINT NOT NULL,            -- Measure: Đơn giá thực tế
    line_total BIGINT NOT NULL,            -- Measure: Thành tiền dòng hàng
    discount_amount BIGINT DEFAULT 0,      -- Measure: Giảm giá
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- Khóa logic duy nhất để chống nhân đôi dữ liệu (Idempotency)
    UNIQUE(store_id, order_id, line_item_id)
);

-- 4. TẦNG CÁCH LY LỖI (REJECT TABLES)

-- Bảng lưu trữ đơn hàng bị từ chối
CREATE TABLE IF NOT EXISTS reject_orders (
    reject_id BIGINT PRIMARY KEY,
    batch_id VARCHAR NOT NULL,
    order_id VARCHAR,
    store_id VARCHAR,
    raw_date VARCHAR,
    raw_phone VARCHAR,
    raw_amount VARCHAR,
    error_code VARCHAR NOT NULL,           -- INVALID_DATE_FORMAT, CORRUPTED_CURRENCY, UNKNOWN_STORE_ID...
    rejection_reason VARCHAR NOT NULL,
    rejected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bảng lưu trữ chi tiết dòng hàng bị từ chối
CREATE TABLE IF NOT EXISTS reject_order_items (
    reject_id BIGINT PRIMARY KEY,
    batch_id VARCHAR NOT NULL,
    order_id VARCHAR,
    store_id VARCHAR,
    product_code VARCHAR,
    quantity INT,
    unit_price BIGINT,
    line_total BIGINT,
    calculated_total BIGINT,
    diff_amount BIGINT,
    error_code VARCHAR NOT NULL,           -- INCONSISTENT_LINE_TOTAL, UNKNOWN_PRODUCT_CODE...
    rejection_reason VARCHAR NOT NULL,
    rejected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. BẢNG KIỂM TOÁN ETL (ETL AUDIT LOG)
CREATE TABLE IF NOT EXISTS etl_audit_log (
    batch_id VARCHAR PRIMARY KEY,
    pipeline_run_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    extracted_orders_count INT,
    extracted_items_count INT,
    clean_orders_count INT,
    clean_items_count INT,
    rejected_orders_count INT,
    rejected_items_count INT,
    fact_sales_loaded INT,
    duration_seconds DOUBLE,
    status VARCHAR                         -- SUCCESS, PARTIAL_SUCCESS, FAILED
);
