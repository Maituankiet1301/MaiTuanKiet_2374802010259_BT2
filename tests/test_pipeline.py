"""
BỘ KIỂM THỬ TỰ ĐỘNG TOÀN DIỆN CHO LUỒNG L6 - MEKONG MOBILE DWH (TRACK DA)
Sinh viên thực hiện: Mai Tuấn Kiệt (MSSV: 2374802010259)
Học phần: Chuyên đề tốt nghiệp 1 - Buổi 14: Workshop Kiểm thử hệ thống cá nhân
Giảng viên chấm: TS. Nguyễn Trí Hải / ThS. Nguyễn Minh Tân / ThS. Trần Công Thanh

Bao gồm đầy đủ 12 Test Cases thuộc 5 loại kiểm thử bắt buộc cho Track DA:
1. Luồng đúng (Normal flow): TC-01, TC-02
2. Giá trị biên (Boundary value): TC-03, TC-04 (kiểm thử cả 2 bên ranh giới)
3. Dữ liệu sai (Invalid data graceful rejection): TC-05, TC-06, TC-07
4. Bảo mật & Chất lượng dữ liệu (Security & Data Quality): TC-08, TC-09, TC-10
5. Tái lập & Ổn định hệ thống (Reproducibility & Robustness): TC-11, TC-12

Chạy toàn bộ bằng một lệnh duy nhất: pytest -v (hoặc pytest -q)
"""

import os
import tempfile
import pytest
import pandas as pd
from datetime import datetime, date

from src.quality.checker import (
    check_date_validity,
    check_currency_amount,
    check_line_total_consistency,
    check_referential_integrity,
    check_uniqueness,
    check_phone_validity,
    clean_currency_str,
    clean_phone_str,
    parse_date_flexibly,
    run_data_quality_suite
)
from src.transform.transformer import DataTransformer
from src.load.loader import DWHLoader
from src.extract.extractor import DataExtractor


@pytest.fixture
def sample_valid_data():
    """Tự sinh dữ liệu hợp lệ hoàn toàn trong bộ nhớ (Fixture in-memory độc lập)"""
    stores = pd.DataFrame([
        {"ma_cua_hang": "CH01", "ten_cua_hang": "Mekong Cần Thơ", "tinh_thanh": "Cần Thơ", "khu_vuc": "Tây Nam Bộ", "quan_ly": "Nguyễn Văn Hùng"},
        {"ma_cua_hang": "CH02", "ten_cua_hang": "Mekong Mỹ Tho", "tinh_thanh": "Tiền Giang", "khu_vuc": "Đông Nam Bộ", "quan_ly": "Lê Hoàng Phúc"}
    ])
    products = pd.DataFrame([
        {"ma_san_pham": "SP001", "ten_san_pham": "iPhone 15 Pro", "danh_muc": "DIEN_THOAI_CAO_CAP", "hang_san_xuat": "Apple", "gia_niem_yet": 25000000},
        {"ma_san_pham": "SP013", "ten_san_pham": "Sạc nhanh 25W", "danh_muc": "PHU_KIEN_SAC_CAP", "hang_san_xuat": "Samsung", "gia_niem_yet": 350000}
    ])
    orders = pd.DataFrame([
        {"Ma don": "HD_TEST_01", "Ma cua hang": "CH01", "Ngay": "15/03/2024", "SDT": "0901234567", "Khach hang": "Nguyễn Văn An", "Thanh tien": "25000000", "Nhan vien": "NV01"},
        {"Ma don": "HD_TEST_02", "Ma cua hang": "CH02", "Ngay": "2024-05-10", "SDT": "84912345678", "Khach hang": "Trần Thị Bình", "Thanh tien": "350000", "Nhan vien": "NV02"}
    ])
    order_items = pd.DataFrame([
        {"ma_don": "HD_TEST_01", "ma_cua_hang": "CH01", "ma_san_pham": "SP001", "so_luong": 1, "don_gia": 25000000, "thanh_tien": 25000000},
        {"ma_don": "HD_TEST_02", "ma_cua_hang": "CH02", "ma_san_pham": "SP013", "so_luong": 1, "don_gia": 350000, "thanh_tien": 350000}
    ])
    return {
        "stores": stores,
        "products": products,
        "orders": orders,
        "order_items": order_items
    }


# ==============================================================================
# NHÓM 1: KIỂM THỬ LUỒNG ĐÚNG (NORMAL FLOW)
# ==============================================================================

def test_tc01_luong_dung_nap_du_lieu_chuan(sample_valid_data):
    """
    [TC-01] Luồng đúng: Nạp dữ liệu chuẩn hợp lệ vào mô hình Star Schema.
    Mục tiêu: Đảm bảo khi dữ liệu chuẩn, Fact nạp đủ số dòng, 0 đơn vào reject.
    """
    transformer = DataTransformer(batch_id="BATCH_TC01_NORMAL")
    dim_tables, df_fact, df_rej_orders, df_rej_items = transformer.transform_all(sample_valid_data)

    # 1. Không có bản ghi nào bị reject
    assert len(df_rej_orders) == 0, f"Kỳ vọng 0 đơn lỗi, thực tế: {len(df_rej_orders)}"
    assert len(df_rej_items) == 0, f"Kỳ vọng 0 chi tiết lỗi, thực tế: {len(df_rej_items)}"

    # 2. Số dòng Fact nạp đúng bằng số dòng chi tiết hợp lệ (2 dòng)
    assert len(df_fact) == 2, f"Kỳ vọng 2 dòng Fact, thực tế: {len(df_fact)}"

    # 3. Tổng doanh thu Fact bảo toàn chính xác
    assert df_fact["line_total"].sum() == 25350000, "Tổng doanh thu Fact phải khớp với dữ liệu nguồn"
    assert (df_fact["store_key"] > 0).all(), "Store key phải là số nguyên dương hợp lệ"


def test_tc02_luong_dung_anh_xa_san_pham_chua_phan_loai(sample_valid_data):
    """
    [TC-02] Luồng đúng: Ánh xạ an toàn sản phẩm chưa có trong danh mục (QT-05).
    Mục tiêu: Sản phẩm lạ SP999 được gán product_key = -1, Fact vẫn nạp đủ không mất doanh số.
    """
    payload = {
        "stores": sample_valid_data["stores"],
        "products": sample_valid_data["products"],
        "orders": pd.DataFrame([{
            "Ma don": "HD_UNKNOWN_01", "Ma cua hang": "CH01", "Ngay": "20/04/2024",
            "SDT": "0901234567", "Khach hang": "Khách Mua Hàng Lạ", "Thanh tien": "1200000", "Nhan vien": "NV01"
        }]),
        "order_items": pd.DataFrame([{
            "ma_don": "HD_UNKNOWN_01", "ma_cua_hang": "CH01", "ma_san_pham": "SP999_CHUA_CO",
            "so_luong": 1, "don_gia": 1200000, "thanh_tien": 1200000
        }])
    }
    transformer = DataTransformer(batch_id="BATCH_TC02_UNKNOWN_PROD")
    dim_tables, df_fact, df_rej_orders, df_rej_items = transformer.transform_all(payload)

    assert len(df_fact) == 1, "Dòng hàng sản phẩm lạ vẫn phải được nạp vào Fact"
    assert df_fact.iloc[0]["product_key"] == -1, "Mã sản phẩm lạ phải được map về fallback product_key = -1"
    assert len(df_rej_orders) == 0, "Đơn hàng chứa sản phẩm lạ không được bị reject"


# ==============================================================================
# NHÓM 2: KIỂM THỬ GIÁ TRỊ BIÊN (BOUNDARY VALUE - 2 PHÍA RANH GIỚI)
# ==============================================================================

def test_tc03_gia_tri_bien_sai_so_trong_nguong_cho_phep():
    """
    [TC-03] Giá trị biên: Kiểm tra sai số thành tiền ở đúng ranh giới cho phép (QT-03).
    Ranh giới cho phép: |thanh_tien - so_luong * don_gia| <= 1 VNĐ.
    - Điểm 0đ: Khớp hoàn toàn -> PASS
    - Điểm +1đ (Biên trên): Hợp lệ -> PASS
    - Điểm -1đ (Biên dưới): Hợp lệ -> PASS
    """
    boundary_items = pd.DataFrame([
        {"id": 1, "so_luong": 2, "don_gia": 150000, "thanh_tien": 300000},  # Lệch 0đ
        {"id": 2, "so_luong": 2, "don_gia": 150000, "thanh_tien": 300001},  # Lệch +1đ (Biên trên)
        {"id": 3, "so_luong": 2, "don_gia": 150000, "thanh_tien": 299999},  # Lệch -1đ (Biên dưới)
    ])
    failed_cnt, err_rate, failed_df = check_line_total_consistency(
        boundary_items, qty_col="so_luong", price_col="don_gia", total_col="thanh_tien", threshold=1
    )
    assert failed_cnt == 0, f"Kỳ vọng 0 dòng lỗi trong ngưỡng 1đ, thực tế: {failed_cnt}"
    assert err_rate == 0.0, "Tỷ lệ lỗi phải là 0.0%"
    assert len(failed_df) == 0, "Không có dòng nào bị đánh dấu lỗi"


def test_tc04_gia_tri_bien_sai_so_vuot_nguong_cho_phep():
    """
    [TC-04] Giá trị biên: Kiểm tra sai số thành tiền vượt ngưỡng ranh giới (QT-03).
    - Điểm +2đ (Vượt biên trên): Vi phạm -> REJECT
    - Điểm -2đ (Vượt biên dưới): Vi phạm -> REJECT
    """
    exceed_items = pd.DataFrame([
        {"id": 101, "so_luong": 3, "don_gia": 100000, "thanh_tien": 300002},  # Lệch +2đ (Vi phạm trên)
        {"id": 102, "so_luong": 3, "don_gia": 100000, "thanh_tien": 299998},  # Lệch -2đ (Vi phạm dưới)
    ])
    failed_cnt, err_rate, failed_df = check_line_total_consistency(
        exceed_items, qty_col="so_luong", price_col="don_gia", total_col="thanh_tien", threshold=1
    )
    assert failed_cnt == 2, f"Kỳ vọng phát hiện đúng 2 dòng lỗi vượt biên, thực tế: {failed_cnt}"
    assert err_rate == 1.0, "Tỷ lệ lỗi là 100% đối với tập dữ liệu vi phạm"
    diff_values = set(failed_df["diff_amount"])
    assert 2 in diff_values, "Độ lệch 2đ phải được phát hiện và lưu vết"


# ==============================================================================
# NHÓM 3: KIỂM THỬ DỮ LIỆU SAI (INVALID DATA GRACEFUL REJECTION)
# ==============================================================================

def test_tc05_du_lieu_sai_dinh_dang_ngay_thang(sample_valid_data):
    """
    [TC-05] Dữ liệu sai: Từ chối an toàn ngày sai định dạng / ngày ngoài biên (CL2 & QT-02).
    Các trường hợp: Ngày ảo 31/02/2025, ngày trước 2020 (2018-01-01), chuỗi rác.
    """
    bad_date_orders = pd.DataFrame([
        {"Ma don": "BAD_D01", "Ma cua hang": "CH01", "Ngay": "31/02/2025", "SDT": "0901234567", "Khach hang": "Ngày 31/2 ảo", "Thanh tien": "500000", "Nhan vien": "NV01"},
        {"Ma don": "BAD_D02", "Ma cua hang": "CH01", "Ngay": "2018-05-15", "SDT": "0901234567", "Khach hang": "Ngày trước 2020", "Thanh tien": "500000", "Nhan vien": "NV01"},
        {"Ma don": "BAD_D03", "Ma cua hang": "CH01", "Ngay": "NGAY_KHONG_HOP_LE", "SDT": "0901234567", "Khach hang": "Chuỗi rác", "Thanh tien": "500000", "Nhan vien": "NV01"}
    ])
    payload = {
        "stores": sample_valid_data["stores"],
        "products": sample_valid_data["products"],
        "orders": bad_date_orders,
        "order_items": pd.DataFrame()
    }
    transformer = DataTransformer(batch_id="BATCH_TC05_BAD_DATE")
    dim_tables, df_fact, df_rej_orders, df_rej_items = transformer.transform_all(payload)

    assert len(df_rej_orders) == 3, f"Kỳ vọng từ chối 3 đơn sai ngày, thực tế: {len(df_rej_orders)}"
    assert (df_rej_orders["error_code"] == "INVALID_DATE_FORMAT").all(), "Mã lỗi phải là INVALID_DATE_FORMAT"
    assert len(df_fact) == 0, "Không có dòng Fact nào được nạp từ đơn hàng sai ngày"


def test_tc06_du_lieu_sai_chuoi_tien_te_hong(sample_valid_data):
    """
    [TC-06] Dữ liệu sai: Từ chối đơn hàng có giá trị tiền tệ dính chữ hoặc số âm (CL1 & QT-03).
    """
    bad_curr_orders = pd.DataFrame([
        {"Ma don": "BAD_C01", "Ma cua hang": "CH01", "Ngay": "15/03/2024", "SDT": "0901234567", "Khach hang": "Tiền dính chữ", "Thanh tien": "HAI_TRIEU_DONG", "Nhan vien": "NV01"},
        {"Ma don": "BAD_C02", "Ma cua hang": "CH01", "Ngay": "15/03/2024", "SDT": "0901234567", "Khach hang": "Tiền âm", "Thanh tien": "-250000", "Nhan vien": "NV01"}
    ])
    payload = {
        "stores": sample_valid_data["stores"],
        "products": sample_valid_data["products"],
        "orders": bad_curr_orders,
        "order_items": pd.DataFrame()
    }
    transformer = DataTransformer(batch_id="BATCH_TC06_BAD_CURRENCY")
    dim_tables, df_fact, df_rej_orders, df_rej_items = transformer.transform_all(payload)

    assert len(df_rej_orders) == 2, f"Kỳ vọng từ chối 2 đơn sai tiền, thực tế: {len(df_rej_orders)}"
    assert (df_rej_orders["error_code"] == "CORRUPTED_CURRENCY_STRING").all()


def test_tc07_du_lieu_sai_ma_cua_hang_khong_ton_tai(sample_valid_data):
    """
    [TC-07] Dữ liệu sai: Từ chối đơn hàng có mã cửa hàng không tồn tại trong danh mục 24 chi nhánh (CL5 & QT-05).
    """
    bad_store_orders = pd.DataFrame([
        {"Ma don": "BAD_S01", "Ma cua hang": "CH99_KHONG_CO", "Ngay": "15/03/2024", "SDT": "0901234567", "Khach hang": "Cửa hàng lạ", "Thanh tien": "1000000", "Nhan vien": "NV01"}
    ])
    payload = {
        "stores": sample_valid_data["stores"],
        "products": sample_valid_data["products"],
        "orders": bad_store_orders,
        "order_items": pd.DataFrame()
    }
    transformer = DataTransformer(batch_id="BATCH_TC07_BAD_STORE")
    dim_tables, df_fact, df_rej_orders, df_rej_items = transformer.transform_all(payload)

    assert len(df_rej_orders) == 1, "Phải từ chối đơn hàng có mã cửa hàng lạ"
    assert df_rej_orders.iloc[0]["error_code"] == "UNKNOWN_STORE_ID"


# ==============================================================================
# NHÓM 4: KIỂM THỬ BẢO MẬT & CHẤT LƯỢNG DỮ LIỆU (SECURITY & DATA QUALITY)
# ==============================================================================

def test_tc08_bao_mat_che_so_dien_thoai_khach_hang(sample_valid_data):
    """
    [TC-08] Bảo mật: Che 4 số cuối số điện thoại khách hàng theo tiêu chuẩn NFR3 (Data Masking).
    Ví dụ: '0901234567' -> '090123****'
    """
    transformer = DataTransformer(batch_id="BATCH_TC08_MASKING")
    dim_tables, df_fact, df_rej_orders, df_rej_items = transformer.transform_all(sample_valid_data)
    df_cust = dim_tables["dim_customer"]

    # Lọc khách hàng có SĐT hợp lệ
    valid_cust = df_cust[df_cust["is_valid_phone"]]
    assert len(valid_cust) >= 2, "Phải có ít nhất 2 khách hàng hợp lệ được ghi nhận"
    
    # Kiểm tra quy tắc che: đúng 10 ký tự, kết thúc bằng '****'
    for _, row in valid_cust.iterrows():
        masked = row["masked_phone"]
        assert len(masked) == 10, f"SĐT che phải đủ 10 ký tự: {masked}"
        assert masked.endswith("****"), f"SĐT che phải kết thúc bằng 4 dấu sao: {masked}"
        assert not masked.isdigit(), f"SĐT che không được để lộ toàn bộ số: {masked}"


def test_tc09_chat_luong_du_lieu_do_luong_va_canh_bao(sample_valid_data):
    """
    [TC-09] Chất lượng dữ liệu: Bộ kiểm tra run_data_quality_suite đo lường chính xác tỷ lệ lỗi.
    """
    orders_mixed = pd.DataFrame([
        {"Ma don": "ORD_01", "Ma cua hang": "CH01", "Ngay": "15/03/2024", "SDT": "0901234567", "Thanh tien": "500000"},
        {"Ma don": "ORD_02", "Ma cua hang": "CH01", "Ngay": "31/02/2024", "SDT": "0901234567", "Thanh tien": "500000"}, # Sai ngày
        {"Ma don": "ORD_03", "Ma cua hang": "CH01", "Ngay": "15/03/2024", "SDT": "0901234567", "Thanh tien": "HONG_TIEN"}, # Sai tiền
        {"Ma don": "ORD_04", "Ma cua hang": "CH99", "Ngay": "15/03/2024", "SDT": "0901234567", "Thanh tien": "500000"}, # Sai store
    ])
    items_mixed = pd.DataFrame([
        {"so_luong": 2, "don_gia": 100000, "thanh_tien": 200000},
        {"so_luong": 2, "don_gia": 100000, "thanh_tien": 250000}, # Sai lệch 50.000đ
    ])

    report = run_data_quality_suite(orders_mixed, items_mixed, sample_valid_data["stores"])

    # Xác nhận các chỉ số đo lường
    assert report["date_validity"]["failed_count"] == 1
    assert report["date_validity"]["error_rate"] == 0.25 # 1 / 4
    assert report["currency_validity"]["failed_count"] == 1
    assert report["store_referential"]["failed_count"] == 1
    assert report["line_total_consistency"]["failed_count"] == 1
    assert report["line_total_consistency"]["error_rate"] == 0.50 # 1 / 2


def test_tc10_bao_mat_chong_sql_injection_ky_tu_dac_biet(sample_valid_data, tmp_path):
    """
    [TC-10] Bảo mật: Dữ liệu chứa ký tự đặc biệt nguy hiểm (SQL Injection, XSS probe)
    được xử lý an toàn qua parameterized queries, không làm sập kho DuckDB.
    """
    test_db = str(tmp_path / "test_security.duckdb")
    loader = DWHLoader(db_path=test_db)
    loader.init_schema()

    malicious_orders = pd.DataFrame([
        {
            "Ma don": "ORD_SQLI_01",
            "Ma cua hang": "CH01",
            "Ngay": "15/03/2024",
            "SDT": "0901234567",
            "Khach hang": "Robert'); DROP TABLE fact_sales; --",
            "Thanh tien": "100000",
            "Nhan vien": "<script>alert('xss')</script>"
        }
    ])
    malicious_items = pd.DataFrame([
        {"ma_don": "ORD_SQLI_01", "ma_cua_hang": "CH01", "ma_san_pham": "SP001", "so_luong": 1, "don_gia": 100000, "thanh_tien": 100000}
    ])
    payload = {
        "stores": sample_valid_data["stores"],
        "products": sample_valid_data["products"],
        "orders": malicious_orders,
        "order_items": malicious_items
    }

    transformer = DataTransformer(batch_id="BATCH_TC10_SECURITY")
    dim_tables, df_fact, df_rej_o, df_rej_i = transformer.transform_all(payload)

    # Nạp vào DuckDB và kiểm tra bảng fact_sales vẫn toàn vẹn
    loader.load_dimensions(dim_tables)
    loader.load_fact_sales(df_fact)

    counts = loader.get_table_counts()
    assert counts["fact_sales"] == 1, "Fact sales phải nạp an toàn 1 dòng, không bị phá hủy"
    assert counts["dim_customer"] >= 1, "Bảng dimension customer không bị ảnh hưởng"


# ==============================================================================
# NHÓM 5: KIỂM THỬ TÁI LẬP & ỔN ĐỊNH HỆ THỐNG (REPRODUCIBILITY & ROBUSTNESS)
# ==============================================================================

def test_tc11_tai_lap_idempotent_chay_nhieu_lan_khong_nhan_doi(sample_valid_data, tmp_path):
    """
    [TC-11] Tính tái lập & Idempotent: Chạy pipeline nạp dữ liệu 2 lần liên tiếp trên cùng CSDL.
    Mục tiêu: Đảm bảo số dòng bảng Fact lần 2 hoàn toàn bằng lần 1 (không nhân đôi).
    """
    test_db = str(tmp_path / "test_idempotent_v14.duckdb")
    loader = DWHLoader(db_path=test_db)
    loader.init_schema()

    transformer = DataTransformer(batch_id="BATCH_TC11_RUN1")
    dim_tables, df_fact, df_rej_o, df_rej_i = transformer.transform_all(sample_valid_data)

    # Lần nạp 1
    loader.load_dimensions(dim_tables)
    loader.load_fact_sales(df_fact)
    counts_run_1 = loader.get_table_counts()
    assert counts_run_1["fact_sales"] == 2, "Lần 1 phải có đúng 2 dòng Fact"

    # Lần nạp 2 (chạy lại với cùng dữ liệu)
    loader.load_dimensions(dim_tables)
    loader.load_fact_sales(df_fact)
    counts_run_2 = loader.get_table_counts()

    # Xác nhận tính Idempotent: Tuyệt đối không bị nhân đôi
    assert counts_run_2["fact_sales"] == 2, f"Lỗi nhân đôi dữ liệu: {counts_run_2['fact_sales']} != 2"
    assert counts_run_2["dim_store"] == counts_run_1["dim_store"]
    assert counts_run_2["dim_product"] == counts_run_1["dim_product"]


def test_tc12_tai_lap_xu_ly_an_toan_tep_rong_zero_bytes():
    """
    [TC-12] Khả năng chịu lỗi & Tái lập: Xử lý tệp CSV rỗng (0 bytes hoặc chỉ dòng header).
    Mục tiêu: DataExtractor xử lý an toàn (BUG-03), không gây lỗi unhandled EmptyDataError.
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        # Tạo 4 tệp rỗng kích thước 0 bytes
        for fname in ["stores.csv", "products.csv", "orders_sample.csv", "order_items_sample.csv"]:
            open(os.path.join(tmp_dir, fname), "w").close()

        extractor = DataExtractor(raw_data_dir=tmp_dir, seeds_dir=tmp_dir)
        raw_data = extractor.extract_all()

        # Xác nhận trích xuất thành công và trả về DataFrame rỗng có cột chuẩn
        assert len(raw_data["stores"]) == 0
        assert "ma_cua_hang" in raw_data["stores"].columns
        assert len(raw_data["orders"]) == 0
        assert "Ma don" in raw_data["orders"].columns

        # Đưa vào Transformer: không gây crash
        transformer = DataTransformer(batch_id="BATCH_TC12_EMPTY")
        dim_tables, df_fact, df_rej_o, df_rej_i = transformer.transform_all(raw_data)
        assert len(df_fact) == 0, "Dữ liệu rỗng cho ra 0 dòng Fact mà không sập"
        assert len(df_rej_o) == 0
        assert len(df_rej_i) == 0
