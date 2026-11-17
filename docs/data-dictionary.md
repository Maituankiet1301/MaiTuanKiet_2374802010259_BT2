# TECHNICAL DATA DICTIONARY (FLOW L6)
## Mekong Mobile Smart CRM – Dimensional Warehouse Schema Specification
**Track:** Data Analytics (DA) | **Student:** Mai Tuan Kiet | **Student ID:** 2374802010259  
**Course:** Specialized Graduation Topic 1 (Chuyên đề tốt nghiệp 1) – Semester 1 (2026 – 2027)  
**Standard Compliance:** Criteria D2, D3, D4 (Assignment 3 Technical Specification)

---

## 1. Dimensional Architecture Overview

The analytical schema follows the Kimball Dimensional Modeling methodology (Star Schema) hosted inside an embedded DuckDB analytical database (`data/dwh_mekong.duckdb`). It consists of **4 Dimension Tables**, **1 Central Fact Table**, **2 Quarantine Reject Tables**, and **1 Operational Audit Table**.

All column specifications below are directly reconciled against the live DuckDB schema (`DESCRIBE <table_name>`) and verified by automated unit and integration tests.

---

## 2. Dimension Tables (Các bảng Chiều)

### 2.1. `dim_date` (Calendar Date Dimension)
- **Table Type:** Conformed Dimension
- **Primary Key:** `date_key`
- **Total Rows in Production Warehouse:** 731 records (2 full calendar years: 2024-01-01 to 2025-12-31)

| Column Name | Data Type | Constraint | Nullable | Business Description & Sample Values |
|:---|:---|:---:|:---:|:---|
| `date_key` | `INTEGER` | **PK** | No | Surrogate integer key in `YYYYMMDD` format (e.g., `20240315`). |
| `full_date` | `DATE` | **UNIQUE** | No | Standard ISO-8601 calendar date (`YYYY-MM-DD`, e.g., `2024-03-15`). |
| `day_of_month` | `INTEGER` | None | No | Day of month (1 to 31). |
| `month` | `INTEGER` | None | No | Month number (1 to 12). |
| `quarter` | `INTEGER` | None | No | Financial quarter (1 to 4). |
| `year` | `INTEGER` | None | No | Calendar year (e.g., `2024`, `2025`). |
| `day_name` | `VARCHAR` | None | No | English day of week name (e.g., `'Monday'`, `'Friday'`). |
| `is_weekend` | `BOOLEAN` | None | No | Boolean flag: `TRUE` for Saturday/Sunday, `FALSE` otherwise. |

---

### 2.2. `dim_store` (Physical Retail Store Dimension)
- **Table Type:** Conformed Dimension
- **Primary Key:** `store_key`
- **Total Rows in Production Warehouse:** 24 records (`CH01` through `CH24`)

| Column Name | Data Type | Constraint | Nullable | Business Description & Sample Values |
|:---|:---|:---:|:---:|:---|
| `store_key` | `INTEGER` | **PK** | No | Surrogate auto-increment integer key (1, 2, ...). |
| `store_id` | `VARCHAR` | **UNIQUE** | No | Natural business store code (e.g., `'CH01'`, `'CH24'`). |
| `store_name` | `VARCHAR` | None | No | Commercial store name (e.g., `'Mekong Mobile Quận 1'`). |
| `city` | `VARCHAR` | None | No | Administrative province/city (e.g., `'TP. Hồ Chí Minh'`, `'Cần Thơ'`). |
| `region` | `VARCHAR` | None | No | Geographic sales territory (`'Đông Nam Bộ'`, `'Tây Nam Bộ'`). |
| `manager_name` | `VARCHAR` | None | Yes | Full name of the designated branch general manager. |

---

### 2.3. `dim_product` (Product Catalog Dimension)
- **Table Type:** Conformed Dimension
- **Primary Key:** `product_key`
- **Total Rows in Production Warehouse:** 25 records (24 catalog items + 1 Unknown Product record)

| Column Name | Data Type | Constraint | Nullable | Business Description & Sample Values |
|:---|:---|:---:|:---:|:---|
| `product_key` | `INTEGER` | **PK** | No | Surrogate integer key. **Key `-1` is reserved for Unknown/Unclassified Products**. |
| `product_code` | `VARCHAR` | **UNIQUE** | No | Natural SKU identifier (e.g., `'SP001'`, `'SP024'`, or `'UNKNOWN'`). |
| `product_name` | `VARCHAR` | None | No | Product display name (e.g., `'iPhone 15 Pro Max 256GB'`). |
| `category` | `VARCHAR` | None | No | Product hierarchy category (`'Điện thoại'`, `'Phụ kiện'`, `'Máy tính bảng'`). |
| `brand` | `VARCHAR` | None | Yes | Manufacturer brand (`'Apple'`, `'Samsung'`, `'Xiaomi'`). |
| `standard_price`| `BIGINT` | None | Yes | Manufacturer suggested retail price (MSRP) in VND (e.g., `34990000`). |

---

### 2.4. `dim_customer` (Customer Contact Dimension & PII Anonymization)
- **Table Type:** Conformed Dimension (Compliant with Criterion D4 & Decree 13/2023/ND-CP)
- **Primary Key:** `customer_key`
- **Total Rows in Production Warehouse:** 11 records (10 recognized customers + 1 Anonymous record)

| Column Name | Data Type | Constraint | Nullable | Business Description & Sample Values |
|:---|:---|:---:|:---:|:---|
| `customer_key` | `INTEGER` | **PK** | No | Surrogate integer key. **Key `0` is reserved for Anonymous Walk-in Customers**. |
| `phone_number` | `VARCHAR` | **UNIQUE** | No | Standardized 10-digit mobile number used as business identity key. |
| `customer_name` | `VARCHAR` | None | Yes | Customer name if captured at POS checkout. |
| `masked_phone` | `VARCHAR` | None | No | **Pseudonymized phone number with the last 4 digits masked as `****`** (e.g., `'090123****'`). Used for all analytical dashboards. |
| `is_valid_phone`| `BOOLEAN` | None | No | Verification flag: `TRUE` if phone successfully validated to 10 digits. |

---

## 3. Fact Table (Bảng Sự kiện)

### `fact_sales` (Retail Sales Transactions Fact)
- **Table Type:** Transactional Fact Table
- **Grain:** One row per individual product item purchased within an order at a specific store on a specific date.
- **Primary Key:** `sales_fact_key` (Surrogate Key)
- **Business Composite Key:** `(store_id, order_id, line_item_id)` with `UNIQUE` constraint for **Idempotency (C8)**.
- **Total Rows in Production Warehouse:** **3,144 records**

| Column Name | Data Type | Constraint | Nullable | Business Description & Sample Values |
|:---|:---|:---:|:---:|:---|
| `sales_fact_key` | `BIGINT` | **PK** | No | Unique surrogate primary key starting from `100001`. |
| `order_id` | `VARCHAR` | None | No | Natural order receipt identifier (e.g., `'DH_00001'`). |
| `store_id` | `VARCHAR` | None | No | Natural store code identifier (e.g., `'CH01'`). |
| `line_item_id` | `INTEGER` | None | No | Sequential position of line item within the order (1, 2, 3...). |
| `date_key` | `INTEGER` | **FK** | No | Foreign Key referencing `dim_date.date_key`. |
| `store_key` | `INTEGER` | **FK** | No | Foreign Key referencing `dim_store.store_key`. |
| `product_key` | `INTEGER` | **FK** | No | Foreign Key referencing `dim_product.product_key`. |
| `customer_key` | `INTEGER` | **FK** | No | Foreign Key referencing `dim_customer.customer_key`. |
| `quantity` | `INTEGER` | Measure | No | Number of product units sold ($\ge 1$). |
| `unit_price` | `BIGINT` | Measure | No | Actual unit selling price in VND after trade promotions. |
| `line_total` | `BIGINT` | Measure | No | Extended revenue amount in VND ($line\_total = quantity \times unit\_price$). |
| `discount_amount`| `BIGINT` | Measure | No | Trade discount applied to this line item (default 0). |
| `created_at` | `TIMESTAMP` | None | No | Timestamp when the ETL record was loaded into the warehouse. |

---

## 4. Reject Tables (Các bảng Cách ly lỗi)

### 4.1. `reject_orders` (Quarantined Header Records)
- **Table Type:** Operational Error Isolation Table
- **Primary Key:** `reject_id`
- **Total Rows in Production Warehouse:** **5 records** (Matching latest ETL audit report)

| Column Name | Data Type | Constraint | Nullable | Business Description & Sample Values |
|:---|:---|:---:|:---:|:---|
| `reject_id` | `BIGINT` | **PK** | No | Surrogate primary key for quarantine entry. |
| `batch_id` | `VARCHAR` | None | No | ETL execution batch identifier (e.g., `'BATCH_20261117_115459'`). |
| `order_id` | `VARCHAR` | None | Yes | Original raw order ID from POS file. |
| `store_id` | `VARCHAR` | None | Yes | Original raw store ID. |
| `raw_date` | `VARCHAR` | None | Yes | Raw date string causing format rejection (e.g., `'31/02/2025'`). |
| `raw_phone` | `VARCHAR` | None | Yes | Raw phone number string from POS file. |
| `raw_amount` | `VARCHAR` | None | Yes | Raw revenue string causing parsing rejection (e.g., `'HAI_TRIEU'`). |
| `error_code` | `VARCHAR` | None | No | Standard machine-readable error code: `INVALID_DATE_FORMAT`, `CORRUPTED_CURRENCY_STRING`, `UNKNOWN_STORE_ID`. |
| `rejection_reason`| `VARCHAR` | None | No | Detailed human-readable explanation of why the record was rejected. |
| `rejected_at` | `TIMESTAMP` | None | No | System timestamp when quarantine was logged. |

---

### 4.2. `reject_order_items` (Quarantined Detail Line Items)
- **Table Type:** Operational Error Isolation Table
- **Primary Key:** `reject_id`
- **Total Rows in Production Warehouse:** **1 record** (Order `DH_00332` with arithmetic error)

| Column Name | Data Type | Constraint | Nullable | Business Description & Sample Values |
|:---|:---|:---:|:---:|:---|
| `reject_id` | `BIGINT` | **PK** | No | Surrogate primary key for quarantine entry. |
| `batch_id` | `VARCHAR` | None | No | ETL execution batch identifier. |
| `order_id` | `VARCHAR` | None | Yes | Parent order ID. |
| `store_id` | `VARCHAR` | None | Yes | Originating store ID. |
| `product_code` | `VARCHAR` | None | Yes | SKU code of rejected item. |
| `quantity` | `INTEGER` | None | Yes | Unit quantity from POS file. |
| `unit_price` | `BIGINT` | None | Yes | Unit price from POS file. |
| `line_total` | `BIGINT` | None | Yes | Stated line total from POS file. |
| `calculated_total`| `BIGINT`| None | Yes | Recomputed total ($quantity \times unit\_price$). |
| `diff_amount` | `BIGINT` | None | Yes | Mathematical discrepancy ($|line\_total - calculated\_total|$). |
| `error_code` | `VARCHAR` | None | No | `INCONSISTENT_LINE_TOTAL` (when discrepancy $> 1$ VND). |
| `rejection_reason`| `VARCHAR` | None | No | Human-readable explanation of arithmetic violation. |
| `rejected_at` | `TIMESTAMP` | None | No | System timestamp when quarantine was logged. |

---

## 5. Audit Logging Table (Bảng Kiểm toán Vận hành)

### `etl_audit_log` (Pipeline Execution History)
- **Table Type:** Operational Metadata & Governance Table
- **Primary Key:** `batch_id`

| Column Name | Data Type | Constraint | Nullable | Business Description & Sample Values |
|:---|:---|:---:|:---:|:---|
| `batch_id` | `VARCHAR` | **PK** | No | Unique timestamped batch execution token. |
| `pipeline_run_at` | `TIMESTAMP` | None | No | Exact start time of the ETL run. |
| `extracted_orders_count` | `INTEGER` | Metric | No | Total raw orders read from source files (2,058). |
| `extracted_items_count` | `INTEGER` | Metric | No | Total raw order items read from source files (3,146). |
| `clean_orders_count` | `INTEGER` | Metric | No | Number of orders successfully validated (2,053). |
| `clean_items_count` | `INTEGER` | Metric | No | Number of items successfully validated (3,144). |
| `rejected_orders_count` | `INTEGER` | Metric | No | Total orders routed to `reject_orders` (5). |
| `rejected_items_count` | `INTEGER` | Metric | No | Total items routed to `reject_order_items` (1). |
| `fact_sales_loaded` | `INTEGER` | Metric | No | Final rows committed into `fact_sales` (**3,144**). |
| `duration_seconds` | `DOUBLE` | Metric | No | Total wall-clock execution time (typically **~1.38s to 1.42s**). |
| `status` | `VARCHAR` | None | No | Execution completion flag: `'SUCCESS'` or `'FAILED'`. |
