# DEPLOYMENT GUIDE (ENGLISH)
## Smart CRM Mekong Mobile – Retail Sales Data Warehouse & Multi-Dimensional Analytics (Flow L6)
**Track:** Data Analytics (DA) | **Student:** Mai Tuan Kiet | **Student ID:** 2374802010259  
**Course:** Specialized Graduation Topic 1 (Chuyên đề tốt nghiệp 1) – Semester 1 (2026 – 2027)  
**Target Release:** Assignment 3 (Tag `v1.0`) | **Repository:** [https://github.com/Maituankiet1301/MaiTuanKiet_2374802010259_BT2](https://github.com/Maituankiet1301/MaiTuanKiet_2374802010259_BT2)

---

## 1. Requirements

Before running the prototype, ensure that your system meets the following software and hardware requirements:

### 1.1. Operating System
- **Supported OS:** Linux (Ubuntu 20.04+, Debian 11+), macOS (12.0+ Monterey or higher), Microsoft Windows 10/11 (64-bit).

### 1.2. Runtime & Software Dependencies
- **Option A (Containerized - Recommended):**
  - **Docker Engine:** Version `20.10.0` or later (`docker --version`).
  - **Docker Compose:** Version `2.0.0` or later (`docker compose version`).
- **Option B (Native Host Execution):**
  - **Python:** Python `3.11.x` runtime (`python --version >= 3.11`).
  - **Package Manager:** `pip` version `23.0+`.
  - **Virtual Environment:** `venv` or `conda`.
  - **Web Browser:** Google Chrome, Microsoft Edge, or Mozilla Firefox.

### 1.3. Hardware Requirements
- **CPU:** Minimum 2 physical cores (x86_64 or ARM64 / Apple Silicon).
- **RAM:** Minimum 2 GB free RAM (4 GB recommended).
- **Disk Space:** Minimum 500 MB free storage for Docker images and DuckDB analytical storage.
- **Network Ports:** Port `8501` available (default Streamlit HTTP port).

---

## 2. Setup Steps

The entire project is structured to be reproducible from a completely clean directory in **$\le 2$ single commands**.

### Option A: Deployment via Docker Compose (Recommended - $\le 2$ Commands)
From an empty directory or after cloning the repository:

```bash
# Step 1: Copy environment template to configure runtime variables
cp .env.example .env

# Step 2: Build image and start container in detached mode (1 single command)
docker compose up -d --build
```
*Note: The container will automatically execute the automated test suite (`pytest -v`), run the initial ETL pipeline (`python run_pipeline.py`), build the DuckDB database, and start the Streamlit service on port `8501`.*

To view container logs and operational status:
```bash
docker compose logs -f
```

To stop and remove containers and volumes:
```bash
docker compose down -v
```

---

### Option B: Native Host Environment Setup (Alternative)

If Docker is not installed on your testing machine, execute the following commands in order:

```bash
# Step 1: Clone the repository with tag v1.0
git clone --branch v1.0 https://github.com/Maituankiet1301/MaiTuanKiet_2374802010259_BT2.git
cd MaiTuanKiet_2374802010259_BT2

# Step 2: Create and activate a clean Python virtual environment
python -m venv .venv
# On Windows PowerShell:
.venv\Scripts\activate
# On Linux / macOS:
source .venv/bin/activate

# Step 3: Install all locked dependencies
pip install -r requirements.txt

# Step 4: Run the automated ETL pipeline (1 command)
python run_pipeline.py

# Step 5: Launch the interactive Streamlit Dashboard (1 command)
streamlit run app.py
```

---

## 3. Environment Variables

The application is completely configured through environment variables to ensure zero hardcoded secrets. The `.env.example` file provides the standard reference template:

| Variable Name | Default Value | Required | Description |
|:---|:---:|:---:|:---|
| `DB_TYPE` | `duckdb` | Yes | Storage engine type (`duckdb` for embedded OLAP or `postgres` for enterprise). |
| `DB_PATH` | `data/dwh_mekong.duckdb` | Yes | Relative or absolute path to the DuckDB analytical file. |
| `STREAMLIT_PORT` | `8501` | No | Listening port for Streamlit web server. |
| `APP_PORT` | `8501` | No | Application port mapping for container healthcheck. |
| `DATA_RAW_DIR` | `./data/raw` | Yes | Directory containing raw store CSV inputs (falls back to `./seeds`). |
| `AUTH_SALT` | `mekong_crm_salt_2026_demo` | Yes | Cryptographic salt used by SHA-256 password hashing. |
| `ADMIN_USER` | `admin` | No | Default administrative username for dashboard login. |
| `ADMIN_PASSWORD` | `admin123` | No | Initial administrator password. |

---

## 4. Sample Data

The prototype includes a complete synthetic dataset representing the operational reality of 24 Mekong Mobile retail stores in Southern Vietnam over a two-year period (2024–2025):

### 4.1. Data Sources (`seeds/` and `data/raw/`)
1. **`stores.csv` (24 records):**
   - Contains 24 retail stores across Ho Chi Minh City, Can Tho, Binh Duong, etc.
   - Fields: `ma_cua_hang`, `ten_cua_hang`, `tinh_thanh`, `khu_vuc`, `quan_ly`.
2. **`products.csv` (24 records):**
   - Catalog of mobile phones, tablets, smart wearables, and accessories.
   - Fields: `ma_san_pham`, `ten_san_pham`, `danh_muc`, `hang_san_xuat`, `gia_niem_yet`.
3. **`orders_sample.csv` (2,058 records):**
   - Multi-store transaction orders containing realistic edge-case errors (3 corrupted dates, 1 corrupted currency string, 1 invalid store ID `CH99`).
   - Fields: `ma_don`, `ma_cua_hang`, `ngay_raw`, `sdt_raw`, `khach_hang_raw`, `thanh_tien_raw`, `nhan_vien`.
4. **`order_items_sample.csv` (3,146 records):**
   - Detailed line-item breakdown including 2 records with arithmetic rounding/calculation discrepancies ($|thanh\_tien - so\_luong \times don\_gia| > 1$ VND).
   - Fields: `ma_don`, `ma_cua_hang`, `ma_san_pham`, `so_luong`, `don_gia`, `thanh_tien`.

### 4.2. Warehouse Output Summary
Upon pipeline execution, raw data is cleaned, validated, and loaded into DuckDB with the following table record counts:
- `dim_date`: 731 calendar days (2024-01-01 to 2025-12-31).
- `dim_store`: 24 physical stores.
- `dim_product`: 25 products (24 catalog products + 1 Unknown Product key `-1`).
- `dim_customer`: 11 unique customer records (all with 4-digit masked phone `090123****`).
- `fact_sales`: 3,144 valid sales records ($100\%$ consistent).
- `reject_orders`: 5 isolated invalid orders.
- `reject_order_items`: 1 isolated invalid item line.
- `etl_audit_log`: Audit trail tracking batch ID, processing duration, and error metrics.

---

## 5. Verify It Works

To verify that the deployment succeeded without errors, perform the following 5 verification checks:

### Check 1: Container Health Status
Run the following command to check that the service is running and marked as **healthy**:
```bash
docker compose ps
```
**Expected Output:**
```text
NAME                     IMAGE      COMMAND                  SERVICE   STATUS                    PORTS
mekong_mobile_l6_dwh     app        "streamlit run app..."   app       Up 15 seconds (healthy)   0.0.0.0:8501->8501/tcp
```

### Check 2: HTTP Healthcheck Endpoint
Query the Streamlit internal health status endpoint:
```bash
curl -I http://localhost:8501/_stcore/health
```
**Expected Output:** HTTP status code `200 OK`.

### Check 3: Automated Test Suite (100% PASS)
Run the full 12 test cases covering all 5 mandatory test categories:
```bash
# In native environment:
pytest -v
# Or inside the running Docker container:
docker compose exec app pytest -v
```
**Expected Output:** `12 passed in < 2.0s` (100% PASS rate).

### Check 4: Idempotency Verification (C8 Compliance)
Run the pipeline a second time and check that row counts remain strictly identical:
```bash
python run_pipeline.py
# Or via docker:
docker compose exec app python run_pipeline.py
```
**Expected Output:**
- `fact_sales` row count remains exactly **3,144 rows** (no duplicate records).
- All dimension tables remain identical.

### Check 5: Interactive Web Dashboard Access
Open your web browser and navigate to: `http://localhost:8501`.
- **Login screen:** Authenticate using one of the demo credentials:
  - Administrator: `admin` / `admin123` (Full visibility over all 24 stores).
  - Store Manager: `manager1` / `manager123` (Filtered to Store CH01).
  - Data Engineer: `dataeng` / `data123` (Full system and ETL audit view).
- **Verification of 3 UX States:**
  - *Loading State:* Spinner `⏳ Đang thực thi truy vấn...` appears when changing filters.
  - *Empty State:* Toggle sidebar checkbox `🟡 Giả lập Bộ lọc rỗng` $\rightarrow$ warning box with reset button.
  - *Error State:* Toggle sidebar checkbox `🔴 Giả lập Lỗi kết nối CSDL` $\rightarrow$ secure friendly error box without leaking stack traces or database paths (NFR3).

---

## 6. Optional Cloud Deployment (Bonus +1.0 Point)

The prototype is fully configured for zero-friction cloud deployment on **Streamlit Community Cloud** or **Render / Railway**:

### Deploying to Streamlit Community Cloud (Step-by-Step):
1. Fork or push the public repository `https://github.com/Maituankiet1301/MaiTuanKiet_2374802010259_BT2` to GitHub.
2. Sign in to [share.streamlit.io](https://share.streamlit.io/) with your GitHub account.
3. Click **"New app"** and specify:
   - **Repository:** `Maituankiet1301/MaiTuanKiet_2374802010259_BT2`
   - **Branch:** `main` (or Tag `v1.0`)
   - **Main file path:** `app.py`
4. Expand **"Advanced settings..."** and configure environment secrets:
   ```toml
   [env]
   DB_TYPE = "duckdb"
   DB_PATH = "data/dwh_mekong.duckdb"
   AUTH_SALT = "mekong_crm_salt_2026_demo"
   ADMIN_USER = "admin"
   ADMIN_PASSWORD = "admin123"
   ```
5. Click **"Deploy!"**. Within 2 minutes, the live dashboard will be accessible via a public URL:
   `https://maituankiet-bt2-mekong.streamlit.app` (or similar cloud domain).
