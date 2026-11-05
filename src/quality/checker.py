"""
Module kiem tra chat luong du lieu (Data Quality Layer)
Bao gom it nhat 5 ham kiem tra chat luong du lieu theo chuan CL1 - CL5 da dac ta o BT1.
Moi ham tra ve: (failed_count, error_rate, failed_df)
"""

import re
import pandas as pd
from datetime import datetime
from typing import Tuple, List, Optional


def parse_date_flexibly(date_val: str) -> Optional[datetime]:
    """
    Thu giai ma ngay thang theo 3 dinh dang da biet trong case study:
    1. %d/%m/%Y (15/03/2024)
    2. %d-%m-%y (5-8-24)
    3. %Y.%m.%d (2024.11.20)
    4. %Y-%m-%d (ISO chuan)
    """
    if pd.isna(date_val) or not str(date_val).strip():
        return None
    s = str(date_val).strip()
    formats = ["%d/%m/%Y", "%d-%m-%y", "%Y.%m.%d", "%Y-%m-%d"]
    for fmt in formats:
        try:
            dt = datetime.strptime(s, fmt)
            # Kiem tra gioi han nam hop ly (2020 den hien tai)
            if 2020 <= dt.year <= datetime.now().year + 1:
                return dt
        except (ValueError, TypeError):
            continue
    return None


def clean_currency_str(val: str) -> Optional[int]:
    """
    Chuan hoa chuoi tien te: loai bo 'đ', dau cham, dau phay, khoang trang.
    Tra ve so nguyen VNĐ hoac None neu hong.
    """
    if pd.isna(val):
        return None
    s = str(val).strip().lower()
    # Loai bo chu 'đ', 'vnd', dau cham ngan cach hang nghin
    s = s.replace("đ", "").replace("vnd", "").replace(".", "").replace(",", "").replace(" ", "")
    try:
        amount = int(s)
        if amount >= 0:
            return amount
    except ValueError:
        return None
    return None


def clean_phone_str(val: str) -> Tuple[Optional[str], bool]:
    """
    Chuan hoa so dien thoai ve 10 chu so Viet Nam (bat dau bang 0).
    Tra ve: (phone_clean, is_valid)
    """
    if pd.isna(val) or not str(val).strip():
        return ("", False)
    s = re.sub(r"[^\d]", "", str(val))
    if s.startswith("84") and len(s) == 11:
        s = "0" + s[2:]
    if len(s) == 10 and s.startswith("0"):
        return (s, True)
    return (s, False)


# =====================================================================
# 5 HÀM KIỂM TRA CHẤT LƯỢNG DỮ LIỆU CHÍNH THỨC (TRẢ VỀ COUNT VÀ RATE)
# =====================================================================

def check_date_validity(df: pd.DataFrame, date_col: str = "Ngay") -> Tuple[int, float, pd.DataFrame]:
    """
    [CL2 - Validity] Kiem tra tinh hop le cua cot ngay thang.
    Dieu kien: phai parse duoc thanh ngay hop le va trong khoang [2020..hien tai].
    """
    total = len(df)
    if total == 0:
        return (0, 0.0, pd.DataFrame())
    
    is_valid = df[date_col].apply(lambda x: parse_date_flexibly(x) is not None)
    failed_df = df[~is_valid].copy()
    failed_count = len(failed_df)
    error_rate = failed_count / total
    return (failed_count, error_rate, failed_df)


def check_currency_amount(df: pd.DataFrame, amount_col: str = "Thanh tien") -> Tuple[int, float, pd.DataFrame]:
    """
    [CL1 & QT-03 - Validity] Kiem tra chuoi so tien.
    Dieu kien: phai ep kieu duoc thanh so nguyen >= 0 (VNĐ), khong bi dinh chu ky tu hong.
    """
    total = len(df)
    if total == 0:
        return (0, 0.0, pd.DataFrame())
    
    is_valid = df[amount_col].apply(lambda x: clean_currency_str(x) is not None)
    failed_df = df[~is_valid].copy()
    failed_count = len(failed_df)
    error_rate = failed_count / total
    return (failed_count, error_rate, failed_df)


def check_line_total_consistency(
    items_df: pd.DataFrame,
    qty_col: str = "so_luong",
    price_col: str = "don_gia",
    total_col: str = "thanh_tien",
    threshold: int = 1
) -> Tuple[int, float, pd.DataFrame]:
    """
    [CL4 - Consistency] Kiem tra tinh nhat quan: |thanh_tien - (so_luong * don_gia)| <= threshold.
    Theo quy tac QT-03: cho phep sai so lam tron toi da 1 VND.
    """
    total = len(items_df)
    if total == 0:
        return (0, 0.0, pd.DataFrame())
    
    expected = items_df[qty_col] * items_df[price_col]
    diff = (items_df[total_col] - expected).abs()
    is_valid = diff <= threshold
    
    failed_df = items_df[~is_valid].copy()
    failed_df["calculated_total"] = expected[~is_valid]
    failed_df["diff_amount"] = diff[~is_valid]
    
    failed_count = len(failed_df)
    error_rate = failed_count / total
    return (failed_count, error_rate, failed_df)


def check_referential_integrity(
    df: pd.DataFrame,
    ref_df: pd.DataFrame,
    fk_col: str = "Ma cua hang",
    pk_col: str = "ma_cua_hang"
) -> Tuple[int, float, pd.DataFrame]:
    """
    [CL5 - Accuracy / Referential Integrity] Kiem tra toan ven tham chieu.
    Dieu kien: moi ma cua hang trong don hang phai ton tai trong danh muc stores.
    """
    total = len(df)
    if total == 0:
        return (0, 0.0, pd.DataFrame())
    
    valid_keys = set(ref_df[pk_col].astype(str).str.strip())
    is_valid = df[fk_col].astype(str).str.strip().isin(valid_keys)
    failed_df = df[~is_valid].copy()
    failed_count = len(failed_df)
    error_rate = failed_count / total
    return (failed_count, error_rate, failed_df)


def check_uniqueness(
    df: pd.DataFrame,
    key_cols: List[str] = ["Ma cua hang", "Ma don"]
) -> Tuple[int, float, pd.DataFrame]:
    """
    [CL3 - Uniqueness] Kiem tra tinh duy nhat cua khoa nghiep vu phuc hop (store_id + order_id).
    Dieu kien: cap (Ma cua hang, Ma don) khong duoc trung lap trong cung tap du lieu.
    """
    total = len(df)
    if total == 0:
        return (0, 0.0, pd.DataFrame())
    
    duplicates_mask = df.duplicated(subset=key_cols, keep="first")
    failed_df = df[duplicates_mask].copy()
    failed_count = len(failed_df)
    error_rate = failed_count / total
    return (failed_count, error_rate, failed_df)


def check_phone_validity(df: pd.DataFrame, phone_col: str = "SDT") -> Tuple[int, float, pd.DataFrame]:
    """
    [QT-04 - Validity] Kiem tra dinh dang so dien thoai (khong bat buoc, nhung phai dung chuan neu co).
    """
    total = len(df)
    if total == 0:
        return (0, 0.0, pd.DataFrame())
    
    # Giữ index đồng nhất bằng cách fillna chuỗi rỗng
    phone_series = df[phone_col].fillna("").astype(str).str.strip()
    has_phone = phone_series != ""
    phone_subset = df[has_phone].copy()
    if len(phone_subset) == 0:
        return (0, 0.0, pd.DataFrame())
        
    is_valid = phone_subset[phone_col].apply(lambda x: clean_phone_str(x)[1])
    failed_df = phone_subset[~is_valid].copy()
    failed_count = len(failed_df)
    error_rate = failed_count / len(phone_subset)
    return (failed_count, error_rate, failed_df)


# =====================================================================
# BỘ TỔNG HỢP BÁO CÁO CHẤT LƯỢNG (DATA QUALITY SUITE)
# =====================================================================

def run_data_quality_suite(
    orders_df: pd.DataFrame,
    items_df: pd.DataFrame,
    stores_df: pd.DataFrame
) -> dict:
    """
    Chay toan bo bo kiem tra chat luong va tong hop bao cao kem so luong loi va ti le loi.
    """
    c_date, r_date, f_date = check_date_validity(orders_df, "Ngay")
    c_curr, r_curr, f_curr = check_currency_amount(orders_df, "Thanh tien")
    c_store, r_store, f_store = check_referential_integrity(orders_df, stores_df, "Ma cua hang", "ma_cua_hang")
    c_uniq, r_uniq, f_uniq = check_uniqueness(orders_df, ["Ma cua hang", "Ma don"])
    c_line, r_line, f_line = check_line_total_consistency(items_df, "so_luong", "don_gia", "thanh_tien")
    c_phone, r_phone, f_phone = check_phone_validity(orders_df, "SDT")
    
    report = {
        "date_validity": {"failed_count": c_date, "error_rate": r_date, "failed_df": f_date},
        "currency_validity": {"failed_count": c_curr, "error_rate": r_curr, "failed_df": f_curr},
        "store_referential": {"failed_count": c_store, "error_rate": r_store, "failed_df": f_store},
        "composite_uniqueness": {"failed_count": c_uniq, "error_rate": r_uniq, "failed_df": f_uniq},
        "line_total_consistency": {"failed_count": c_line, "error_rate": r_line, "failed_df": f_line},
        "phone_validity": {"failed_count": c_phone, "error_rate": r_phone, "failed_df": f_phone},
    }
    return report
