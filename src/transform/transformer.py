"""
Module bien doi va mo hinh hoa du lieu (Transform Layer)
Thuc hien lam sach, chuan hoa va tao cac bang Dimension, Fact, Reject theo Star Schema.
"""

import uuid
import logging
import pandas as pd
from datetime import datetime
from typing import Dict, Tuple

from ..quality.checker import (
    parse_date_flexibly,
    clean_currency_str,
    clean_phone_str
)

logger = logging.getLogger(__name__)


class DataTransformer:
    def __init__(self, batch_id: str = None):
        self.batch_id = batch_id or f"BATCH_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    def transform_all(
        self,
        raw_data: Dict[str, pd.DataFrame]
    ) -> Tuple[Dict[str, pd.DataFrame], pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Bien doi du lieu tho thanh:
        1. dim_tables: dim_date, dim_store, dim_product, dim_customer
        2. fact_sales: bang su kien da chuan hoa
        3. reject_orders: tap don hang bi tu choi kem ly do
        4. reject_order_items: tap chi tiet bi tu choi kem ly do
        """
        df_stores_raw = raw_data["stores"].copy()
        df_products_raw = raw_data["products"].copy()
        df_orders_raw = raw_data["orders"].copy()
        df_items_raw = raw_data["order_items"].copy()

        # =============================================================
        # 1. BIẾN ĐỔI BẢNG CHIỀU: dim_store
        # =============================================================
        df_store_dim = df_stores_raw.copy()
        df_store_dim["store_key"] = range(1, len(df_store_dim) + 1)
        df_store_dim = df_store_dim.rename(columns={
            "ma_cua_hang": "store_id",
            "ten_cua_hang": "store_name",
            "tinh_thanh": "city",
            "khu_vuc": "region",
            "quan_ly": "manager_name"
        })
        store_id_to_key = dict(zip(df_store_dim["store_id"], df_store_dim["store_key"]))
        valid_store_ids = set(df_store_dim["store_id"])

        # =============================================================
        # 2. BIẾN ĐỔI BẢNG CHIỀU: dim_product
        # =============================================================
        df_prod_dim = df_products_raw.copy()
        df_prod_dim["product_key"] = range(1, len(df_prod_dim) + 1)
        df_prod_dim = df_prod_dim.rename(columns={
            "ma_san_pham": "product_code",
            "ten_san_pham": "product_name",
            "danh_muc": "category",
            "hang_san_xuat": "brand",
            "gia_niem_yet": "standard_price"
        })
        # Them dong du phong Unknown (product_key = -1) theo dac ta BT1
        unknown_prod = pd.DataFrame([{
            "product_key": -1,
            "product_code": "SP_UNKNOWN",
            "product_name": "Sản phẩm chưa phân loại",
            "category": "CHUA_RO",
            "brand": "Unknown",
            "standard_price": 0
        }])
        df_prod_dim = pd.concat([unknown_prod, df_prod_dim], ignore_index=True)
        prod_code_to_key = dict(zip(df_prod_dim["product_code"], df_prod_dim["product_key"]))

        # =============================================================
        # 3. LÀM SẠCH VÀ PHÂN LOẠI ĐƠN HÀNG (ORDERS & REJECT_ORDERS)
        # =============================================================
        clean_orders = []
        rejected_orders = []
        reject_order_counter = 1000

        for idx, row in df_orders_raw.iterrows():
            ma_don = str(row.get("Ma don", "")).strip()
            store_id = str(row.get("Ma cua hang", "")).strip()
            raw_date = str(row.get("Ngay", "")).strip()
            raw_phone = str(row.get("SDT", "")) if pd.notna(row.get("SDT")) else ""
            raw_cust = str(row.get("Khach hang", "")) if pd.notna(row.get("Khach hang")) else ""
            raw_amt = str(row.get("Thanh tien", "")).strip()

            # Kiem tra 1: Cua hang hop le (CL5)
            if store_id not in valid_store_ids:
                reject_order_counter += 1
                rejected_orders.append({
                    "reject_id": reject_order_counter,
                    "batch_id": self.batch_id,
                    "order_id": ma_don,
                    "store_id": store_id,
                    "raw_date": raw_date,
                    "raw_phone": raw_phone,
                    "raw_amount": raw_amt,
                    "error_code": "UNKNOWN_STORE_ID",
                    "rejection_reason": f"Mã cửa hàng '{store_id}' không tồn tại trong danh mục 24 chi nhánh."
                })
                continue

            # Kiem tra 2: Ngay thang hop le (CL2 & QT-02)
            parsed_dt = parse_date_flexibly(raw_date)
            if not parsed_dt:
                reject_order_counter += 1
                rejected_orders.append({
                    "reject_id": reject_order_counter,
                    "batch_id": self.batch_id,
                    "order_id": ma_don,
                    "store_id": store_id,
                    "raw_date": raw_date,
                    "raw_phone": raw_phone,
                    "raw_amount": raw_amt,
                    "error_code": "INVALID_DATE_FORMAT",
                    "rejection_reason": f"Không thể giải mã ngày '{raw_date}' sang định dạng chuẩn hoặc ngày vi phạm quy tắc [2020..hiện tại]."
                })
                continue

            # Kiem tra 3: Tien te hop le (CL1 & QT-03)
            parsed_amt = clean_currency_str(raw_amt)
            if parsed_amt is None:
                reject_order_counter += 1
                rejected_orders.append({
                    "reject_id": reject_order_counter,
                    "batch_id": self.batch_id,
                    "order_id": ma_don,
                    "store_id": store_id,
                    "raw_date": raw_date,
                    "raw_phone": raw_phone,
                    "raw_amount": raw_amt,
                    "error_code": "CORRUPTED_CURRENCY_STRING",
                    "rejection_reason": f"Giá trị tiền '{raw_amt}' chứa chuỗi hỏng không thể ép sang số nguyên VNĐ."
                })
                continue

            # Chuan hoa so dien thoai (QT-04)
            clean_phone, is_valid_phone = clean_phone_str(raw_phone)
            # Che 4 so cuoi cho bao mat (NFR3)
            if is_valid_phone:
                masked_phone = clean_phone[:6] + "****"
            else:
                masked_phone = "KHONG_XAC_DINH"

            clean_orders.append({
                "order_id": ma_don,
                "store_id": store_id,
                "full_date": parsed_dt.date(),
                "date_key": int(parsed_dt.strftime("%Y%m%d")),
                "phone_number": clean_phone if is_valid_phone else "",
                "customer_name": raw_cust or "Khách hàng",
                "masked_phone": masked_phone,
                "is_valid_phone": is_valid_phone,
                "total_amount": parsed_amt,
                "nhan_vien": str(row.get("Nhan vien", ""))
            })

        df_clean_orders = pd.DataFrame(clean_orders)
        df_reject_orders = pd.DataFrame(rejected_orders)
        if df_reject_orders.empty:
            df_reject_orders = pd.DataFrame(columns=[
                "reject_id", "batch_id", "order_id", "store_id", "raw_date", "raw_phone",
                "raw_amount", "error_code", "rejection_reason"
            ])

        # =============================================================
        # 4. BIẾN ĐỔI BẢNG CHIỀU: dim_date
        # =============================================================
        if not df_clean_orders.empty:
            unique_dates = df_clean_orders["full_date"].unique()
            date_records = []
            for d in unique_dates:
                dt = datetime.combine(d, datetime.min.time())
                date_records.append({
                    "date_key": int(dt.strftime("%Y%m%d")),
                    "full_date": d,
                    "day_of_month": dt.day,
                    "month": dt.month,
                    "quarter": (dt.month - 1) // 3 + 1,
                    "year": dt.year,
                    "day_name": dt.strftime("%A"),
                    "is_weekend": dt.weekday() >= 5
                })
            df_date_dim = pd.DataFrame(date_records).drop_duplicates(subset=["date_key"])
        else:
            df_date_dim = pd.DataFrame(columns=[
                "date_key", "full_date", "day_of_month", "month", "quarter", "year", "day_name", "is_weekend"
            ])

        # =============================================================
        # 5. BIẾN ĐỔI BẢNG CHIỀU: dim_customer
        # =============================================================
        # Bat dau voi dong fallback Khach vang lai (customer_key = 0)
        cust_records = [{
            "customer_key": 0,
            "phone_number": "NONE",
            "customer_name": "Khách vãng lai",
            "masked_phone": "KHONG_XAC_DINH",
            "is_valid_phone": False
        }]
        if not df_clean_orders.empty:
            valid_phones_df = df_clean_orders[df_clean_orders["is_valid_phone"]].drop_duplicates(subset=["phone_number"])
            c_key = 1
            for _, r in valid_phones_df.iterrows():
                cust_records.append({
                    "customer_key": c_key,
                    "phone_number": r["phone_number"],
                    "customer_name": r["customer_name"],
                    "masked_phone": r["masked_phone"],
                    "is_valid_phone": True
                })
                c_key += 1
        df_cust_dim = pd.DataFrame(cust_records).drop_duplicates(subset=["phone_number"])
        phone_to_cust_key = dict(zip(df_cust_dim["phone_number"], df_cust_dim["customer_key"]))

        # =============================================================
        # 6. LÀM SẠCH VÀ TẠO BẢNG SỰ KIỆN: fact_sales & reject_order_items
        # =============================================================
        clean_order_lookup = {}
        if not df_clean_orders.empty:
            for _, r in df_clean_orders.iterrows():
                clean_order_lookup[(r["store_id"], r["order_id"])] = r

        fact_rows = []
        rejected_items = []
        reject_item_counter = 5000
        fact_key_counter = 100000

        # Nhom cac item theo (store_id, order_id) de tao line_item_id
        grouped_items = df_items_raw.groupby(["ma_cua_hang", "ma_don"])

        for (st_id, ord_id), items_group in grouped_items:
            # Kiem tra don hang nay co nam trong clean_orders khong
            order_info = clean_order_lookup.get((st_id, ord_id))
            if order_info is None:
                # Don hang nay da bi loai o cap order, khong nap item vao fact
                continue

            line_no = 0
            for _, item_row in items_group.iterrows():
                p_code = str(item_row.get("ma_san_pham", "")).strip()
                qty = int(item_row.get("so_luong", 1))
                price = int(item_row.get("don_gia", 0))
                line_tot = int(item_row.get("thanh_tien", 0))
                calc_tot = qty * price
                diff_amt = abs(line_tot - calc_tot)

                # Kiem tra quy tac CL4 / QT-03: Sai so khong qua 1 VND
                if diff_amt > 1:
                    reject_item_counter += 1
                    rejected_items.append({
                        "reject_id": reject_item_counter,
                        "batch_id": self.batch_id,
                        "order_id": ord_id,
                        "store_id": st_id,
                        "product_code": p_code,
                        "quantity": qty,
                        "unit_price": price,
                        "line_total": line_tot,
                        "calculated_total": calc_tot,
                        "diff_amount": diff_amt,
                        "error_code": "INCONSISTENT_LINE_TOTAL",
                        "rejection_reason": f"Thành tiền ({line_tot:,} đ) lệch quá 1đ so với Số lượng x Đơn giá ({calc_tot:,} đ). Chênh lệch: {diff_amt:,} đ."
                    })
                    continue

                # Tra cuu khoa chieu
                p_key = prod_code_to_key.get(p_code, -1)  # Fallback to -1 if unknown
                s_key = store_id_to_key.get(st_id, 0)
                d_key = order_info["date_key"]
                c_key = phone_to_cust_key.get(order_info["phone_number"], 0)

                line_no += 1
                fact_key_counter += 1
                fact_rows.append({
                    "sales_fact_key": fact_key_counter,
                    "order_id": ord_id,
                    "store_id": st_id,
                    "line_item_id": line_no,
                    "date_key": d_key,
                    "store_key": s_key,
                    "product_key": p_key,
                    "customer_key": c_key,
                    "quantity": qty,
                    "unit_price": price,
                    "line_total": line_tot,
                    "discount_amount": max(0, calc_tot - line_tot)
                })

        df_fact_sales = pd.DataFrame(fact_rows)
        if df_fact_sales.empty:
            df_fact_sales = pd.DataFrame(columns=[
                "sales_fact_key", "order_id", "store_id", "line_item_id", "date_key",
                "store_key", "product_key", "customer_key", "quantity", "unit_price",
                "line_total", "discount_amount"
            ])

        df_reject_items = pd.DataFrame(rejected_items)
        if df_reject_items.empty:
            df_reject_items = pd.DataFrame(columns=[
                "reject_id", "batch_id", "order_id", "store_id", "product_code", "quantity",
                "unit_price", "line_total", "calculated_total", "diff_amount", "error_code", "rejection_reason"
            ])

        dim_tables = {
            "dim_date": df_date_dim,
            "dim_store": df_store_dim,
            "dim_product": df_prod_dim,
            "dim_customer": df_cust_dim
        }

        logger.info(f"Transform complete: {len(df_fact_sales)} fact rows, {len(df_reject_orders)} rejected orders, {len(df_reject_items)} rejected items")
        return dim_tables, df_fact_sales, df_reject_orders, df_reject_items
