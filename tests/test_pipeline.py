"""
Bộ kiểm thử tự động cho Luồng L6 - Mekong Mobile Smart CRM (Track DA)
Bao gồm đầy đủ 3 loại kiểm thử theo yêu cầu bắt buộc của Bài tập 2:
1. Luồng đúng (Normal flow)
2. Giá trị biên (Boundary value)
3. Dữ liệu sai (Invalid data graceful rejection)
Kèm kiểm thử Idempotent (chạy 2 lần không nhân đôi).
Chạy bằng một lệnh duy nhất: pytest
"""

import pytest
import pandas as pd
from datetime import date
from src.quality.checker import (
    check_date_validity,
    check_currency_amount,
    check_line_total_consistency,
    check_referential_integrity,
    clean_currency_str,
    parse_date_flexibly
)
from src.transform.transformer import DataTransformer
from src.load.loader import DWHLoader


@pytest.fixture
def sample_valid_data():
    """Tự sinh dữ liệu hợp lệ hoàn toàn trong bộ nhớ (không phụ thuộc file ngoài)"""
    stores = pd.DataFrame([
        {"ma_cua_hang": "CH01", "ten_cua_hang": "Mekong Cần Thơ", "tinh_thanh": "Cần Thơ", "khu_vuc": "Tây Nam Bộ", "quan_ly": "Nguyễn Văn Hùng"},
        {"ma_cua_hang": "CH02", "ten_cua_hang": "Mekong Mỹ Tho", "tinh_thanh": "Tiền Giang", "khu_vuc": "Đông Nam Bộ", "quan_ly": "Lê Hoàng Phúc"}
    ])
    products = pd.DataFrame([
        {"ma_san_pham": "SP001", "ten_san_pham": "iPhone 15 Pro", "danh_muc": "DIEN_THOAI_CAO_CAP", "hang_san_xuat": "Apple", "gia_niem_yet": 25000000},
        {"ma_san_pham": "SP013", "ten_san_pham": "Sạc nhanh 25W", "danh_muc": "PHU_KIEN_SAC_CAP", "hang_san_xuat": "Samsung", "gia_niem_yet": 350000}
    ])
    orders = pd.DataFrame([
        {"Ma don": "HD_TEST_01", "Ma cua hang": "CH01", "Ngay": "15/03/2024", "SDT": "0901234567", "Khach hang": "Khách Test 1", "Thanh tien": "25000000", "Nhan vien": "NV01"},
        {"Ma don": "HD_TEST_02", "Ma cua hang": "CH02", "Ngay": "2024-05-10", "SDT": "84912345678", "Khach hang": "Khách Test 2", "Thanh tien": "350000", "Nhan vien": "NV02"}
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
# LOẠI 1: LUỒNG ĐÚNG (NORMAL FLOW)
# ==============================================================================
def test_case_1_luong_dung_normal_flow(sample_valid_data):
    """
    Kiểm thử chức năng chạy đúng trong điều kiện bình thường:
    Tệp nguồn đúng định dạng thì nạp đủ số dòng, không có dòng nào bị reject,
    và các khóa chiều được ánh xạ chính xác.
    """
    transformer = DataTransformer(batch_id="TEST_NORMAL_BATCH")
    dim_tables, df_fact, df_rej_orders, df_rej_items = transformer.transform_all(sample_valid_data)

    # 1. Không có đơn nào bị từ chối
    assert len(df_rej_orders) == 0, f"Kỳ vọng 0 đơn lỗi, thực tế có {len(df_rej_orders)}"
    assert len(df_rej_items) == 0, f"Kỳ vọng 0 chi tiết lỗi, thực tế có {len(df_rej_items)}"

    # 2. Số dòng Fact nạp đúng bằng số dòng order_items hợp lệ (2 dòng)
    assert len(df_fact) == 2, f"Kỳ vọng 2 dòng Fact, thực tế có {len(df_fact)}"

    # 3. Kiểm tra tính toàn vẹn khóa ngoại
    assert (df_fact["store_key"] > 0).all(), "Store key phải là số nguyên dương hợp lệ"
    assert (df_fact["date_key"] >= 20200101).all(), "Date key phải thuộc khoảng ngày hợp lệ"
    assert df_fact["line_total"].sum() == 25350000, "Tổng doanh thu Fact phải khớp với dữ liệu nguồn"


# ==============================================================================
# LOẠI 2: GIÁ TRỊ BIÊN (BOUNDARY VALUE)
# ==============================================================================
def test_case_2_gia_tri_bien_line_total_tolerance():
    """
    Kiểm thử trường hợp ở đúng ranh giới của quy tắc QT-03 / CL4:
    Sai số thành tiền giữa thanh_tien và (so_luong * don_gia):
    - Chênh lệch = 0đ  -> HỢP LỆ (PASS)
    - Chênh lệch = +1đ -> ĐÚNG RANH GIỚI NGƯỠNG CHO PHÉP -> HỢP LỆ (PASS)
    - Chênh lệch = -1đ -> ĐÚNG RANH GIỚI NGƯỠNG CHO PHÉP -> HỢP LỆ (PASS)
    - Chênh lệch = +2đ -> VƯỢT NGƯỠNG CHO PHÉP -> TỪ CHỐI (REJECT)
    """
    items_boundary = pd.DataFrame([
        {"id": 1, "so_luong": 2, "don_gia": 100000, "thanh_tien": 200000},  # Lệch 0đ
        {"id": 2, "so_luong": 2, "don_gia": 100000, "thanh_tien": 200001},  # Lệch +1đ (Biên trên)
        {"id": 3, "so_luong": 2, "don_gia": 100000, "thanh_tien": 199999},  # Lệch -1đ (Biên dưới)
        {"id": 4, "so_luong": 2, "don_gia": 100000, "thanh_tien": 200002},  # Lệch +2đ (Vi phạm)
    ])

    failed_cnt, err_rate, failed_df = check_line_total_consistency(
        items_boundary, qty_col="so_luong", price_col="don_gia", total_col="thanh_tien", threshold=1
    )

    # Chỉ có duy nhất dòng ID = 4 bị tính là lỗi
    assert failed_cnt == 1, f"Kỳ vọng đúng 1 dòng lỗi vượt biên, thực tế phát hiện {failed_cnt}"
    assert failed_df.iloc[0]["id"] == 4, "Dòng bị bắt lỗi phải là dòng ID = 4 (lệch 2đ)"
    assert failed_df.iloc[0]["diff_amount"] == 2, "Độ lệch ghi nhận phải bằng 2"


# ==============================================================================
# LOẠI 3: DỮ LIỆU SAI (INVALID DATA REJECTION)
# ==============================================================================
def test_case_3_du_lieu_sai_graceful_rejection(sample_valid_data):
    """
    Kiểm thử hệ thống TỪ CHỐI đúng cách, không sập (Graceful Rejection):
    Khi gặp ngày sai (31/02/2025), chuỗi tiền hỏng, mã cửa hàng không tồn tại:
    - Pipeline không được quăng ngoại lệ làm crash chương trình.
    - Bản ghi lỗi phải được cách ly vào bảng reject_orders với mã lỗi rõ ràng.
    """
    # Tạo đơn hàng lỗi
    bad_orders = pd.DataFrame([
        {"Ma don": "BAD_01", "Ma cua hang": "CH01", "Ngay": "31/02/2025", "SDT": "0901234567", "Khach hang": "Sai ngày", "Thanh tien": "500000"},
        {"Ma don": "BAD_02", "Ma cua hang": "CH01", "Ngay": "15/03/2024", "SDT": "0901234567", "Khach hang": "Sai tiền", "Thanh tien": "LOI_TIEN_TE"},
        {"Ma don": "BAD_03", "Ma cua hang": "CH99_KHONG_CO", "Ngay": "15/03/2024", "SDT": "0901234567", "Khach hang": "Sai cửa hàng", "Thanh tien": "500000"},
    ])
    bad_items = pd.DataFrame([
        {"ma_don": "BAD_01", "ma_cua_hang": "CH01", "ma_san_pham": "SP001", "so_luong": 1, "don_gia": 500000, "thanh_tien": 500000}
    ])

    test_payload = {
        "stores": sample_valid_data["stores"],
        "products": sample_valid_data["products"],
        "orders": bad_orders,
        "order_items": bad_items
    }

    transformer = DataTransformer(batch_id="TEST_BAD_BATCH")
    dim_tables, df_fact, df_rej_orders, df_rej_items = transformer.transform_all(test_payload)

    # Kiểm tra cả 3 đơn hàng sai đều bị từ chối
    assert len(df_rej_orders) == 3, f"Kỳ vọng từ chối đủ 3 đơn lỗi, thực tế từ chối {len(df_rej_orders)}"
    error_codes = set(df_rej_orders["error_code"])
    assert "INVALID_DATE_FORMAT" in error_codes, "Phải ghi nhận lỗi INVALID_DATE_FORMAT"
    assert "CORRUPTED_CURRENCY_STRING" in error_codes, "Phải ghi nhận lỗi CORRUPTED_CURRENCY_STRING"
    assert "UNKNOWN_STORE_ID" in error_codes, "Phải ghi nhận lỗi UNKNOWN_STORE_ID"

    # Đơn hàng lỗi thì không có dòng nào lọt vào Fact
    assert len(df_fact) == 0, "Dữ liệu lỗi không được phép nạp vào bảng fact_sales"


# ==============================================================================
# KIỂM THỬ TÍNH IDEMPOTENT (CHẠY 2 LẦN KHÔNG NHÂN ĐÔI DỮ LIỆU)
# ==============================================================================
def test_case_4_idempotent_double_run(sample_valid_data, tmp_path):
    """
    Kiểm thử tiêu chí chấm điểm DA:
    Chạy pipeline nạp dữ liệu hai lần liên tiếp -> Bảng đích fact_sales KHÔNG bị nhân đôi số dòng.
    """
    test_db = str(tmp_path / "test_idempotent.duckdb")
    loader = DWHLoader(db_path=test_db)
    loader.init_schema()

    transformer = DataTransformer(batch_id="TEST_IDEMPOTENT_1")
    dim_tables, df_fact, df_rej_orders, df_rej_items = transformer.transform_all(sample_valid_data)

    # Nạp lần 1
    loader.load_dimensions(dim_tables)
    loader.load_fact_sales(df_fact)
    counts_run_1 = loader.get_table_counts()
    assert counts_run_1["fact_sales"] == 2, "Lần 1 phải có đúng 2 dòng Fact"

    # Nạp lần 2 (với cùng dữ liệu)
    loader.load_dimensions(dim_tables)
    loader.load_fact_sales(df_fact)
    counts_run_2 = loader.get_table_counts()

    # Xác nhận số dòng Fact lần 2 hoàn toàn bằng lần 1 (KHÔNG NHÂN ĐÔI)
    assert counts_run_2["fact_sales"] == 2, f"Lỗi nhân đôi: Kỳ vọng vẫn là 2 dòng, thực tế thành {counts_run_2['fact_sales']}"
    assert counts_run_2["dim_store"] == counts_run_1["dim_store"], "Số dòng dim_store không đổi"
