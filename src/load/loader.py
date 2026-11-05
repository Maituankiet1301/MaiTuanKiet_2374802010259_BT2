"""
Module nap du lieu vao Kho du lieu DuckDB (Load Layer)
Dam bao tinh chat IDEMPOTENT: Chay nhieu lan khong nhan doi du lieu.
"""

import os
import logging
import duckdb
import pandas as pd
from datetime import datetime
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class DWHLoader:
    def __init__(self, db_path: Optional[str] = None):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.db_path = db_path or os.path.join(base_dir, "data", "dwh_mekong.duckdb")
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.schema_file = os.path.join(base_dir, "sql", "schema.sql")

    def get_connection(self) -> duckdb.DuckDBPyConnection:
        return duckdb.connect(self.db_path)

    def init_schema(self):
        """Khoi tao cau truc cac bang Star Schema neu chua ton tai"""
        if not os.path.exists(self.schema_file):
            raise FileNotFoundError(f"Schema file not found at {self.schema_file}")

        with open(self.schema_file, "r", encoding="utf-8") as f:
            sql_script = f.read()

        con = self.get_connection()
        try:
            # Tach cac cau lenh theo dau cham phay
            statements = [s.strip() for s in sql_script.split(";") if s.strip()]
            for stmt in statements:
                con.execute(stmt)
            logger.info("Successfully initialized DWH Star Schema.")
        finally:
            con.close()

    def load_dimensions(self, dim_tables: Dict[str, pd.DataFrame]):
        """
        Nap cac bang chieu vao kho (Idempotent: Cap nhat hoac chen moi theo Natural Key)
        """
        con = self.get_connection()
        try:
            # 1. dim_store
            df_store = dim_tables.get("dim_store")
            if df_store is not None and not df_store.empty:
                cols_store = ["store_key", "store_id", "store_name", "city", "region", "manager_name"]
                df_store_reordered = df_store[cols_store]
                con.register("temp_store", df_store_reordered)
                con.execute("""
                    DELETE FROM dim_store WHERE store_id IN (SELECT store_id FROM temp_store);
                    INSERT INTO dim_store (store_key, store_id, store_name, city, region, manager_name)
                    SELECT store_key, store_id, store_name, city, region, manager_name FROM temp_store;
                """)
                con.unregister("temp_store")

            # 2. dim_product
            df_prod = dim_tables.get("dim_product")
            if df_prod is not None and not df_prod.empty:
                cols_prod = ["product_key", "product_code", "product_name", "category", "brand", "standard_price"]
                df_prod_reordered = df_prod[cols_prod]
                con.register("temp_prod", df_prod_reordered)
                con.execute("""
                    DELETE FROM dim_product WHERE product_code IN (SELECT product_code FROM temp_prod);
                    INSERT INTO dim_product (product_key, product_code, product_name, category, brand, standard_price)
                    SELECT product_key, product_code, product_name, category, brand, standard_price FROM temp_prod;
                """)
                con.unregister("temp_prod")

            # 3. dim_date
            df_date = dim_tables.get("dim_date")
            if df_date is not None and not df_date.empty:
                cols_date = ["date_key", "full_date", "day_of_month", "month", "quarter", "year", "day_name", "is_weekend"]
                df_date_reordered = df_date[cols_date]
                con.register("temp_date", df_date_reordered)
                con.execute("""
                    DELETE FROM dim_date WHERE date_key IN (SELECT date_key FROM temp_date);
                    INSERT INTO dim_date (date_key, full_date, day_of_month, month, quarter, year, day_name, is_weekend)
                    SELECT date_key, full_date, day_of_month, month, quarter, year, day_name, is_weekend FROM temp_date;
                """)
                con.unregister("temp_date")

            # 4. dim_customer
            df_cust = dim_tables.get("dim_customer")
            if df_cust is not None and not df_cust.empty:
                cols_cust = ["customer_key", "phone_number", "customer_name", "masked_phone", "is_valid_phone"]
                df_cust_reordered = df_cust[cols_cust]
                con.register("temp_cust", df_cust_reordered)
                con.execute("""
                    DELETE FROM dim_customer WHERE phone_number IN (SELECT phone_number FROM temp_cust);
                    INSERT INTO dim_customer (customer_key, phone_number, customer_name, masked_phone, is_valid_phone)
                    SELECT customer_key, phone_number, customer_name, masked_phone, is_valid_phone FROM temp_cust;
                """)
                con.unregister("temp_cust")

            logger.info("Successfully loaded all dimension tables.")
        finally:
            con.close()

    def load_fact_sales(self, df_fact: pd.DataFrame):
        """
        Nap bang fact_sales voi tinh chat IDEMPOTENT:
        Su dung khoa phuc hop (store_id, order_id, line_item_id) de khong nhan doi ban ghi
        khi chay lai pipeline nhieu lan.
        """
        if df_fact is None or df_fact.empty:
            logger.warning("Fact sales dataframe is empty. Nothing to load.")
            return

        con = self.get_connection()
        try:
            con.register("temp_fact", df_fact)
            # Xoa cac dong da ton tai voi cung (store_id, order_id, line_item_id) truoc khi nap
            con.execute("""
                DELETE FROM fact_sales 
                WHERE (store_id, order_id, line_item_id) IN (
                    SELECT store_id, order_id, line_item_id FROM temp_fact
                );
                
                INSERT INTO fact_sales (
                    sales_fact_key, order_id, store_id, line_item_id,
                    date_key, store_key, product_key, customer_key,
                    quantity, unit_price, line_total, discount_amount, created_at
                )
                SELECT 
                    sales_fact_key, order_id, store_id, line_item_id,
                    date_key, store_key, product_key, customer_key,
                    quantity, unit_price, line_total, discount_amount, CURRENT_TIMESTAMP
                FROM temp_fact;
            """)
            con.unregister("temp_fact")
            logger.info(f"Loaded {len(df_fact)} rows into fact_sales (Idempotency guaranteed).")
        finally:
            con.close()

    def load_rejects(self, df_reject_orders: pd.DataFrame, df_reject_items: pd.DataFrame):
        """
        Nap du lieu bi tu choi vao cac bang reject_orders va reject_order_items.
        """
        con = self.get_connection()
        try:
            if df_reject_orders is not None and not df_reject_orders.empty:
                con.register("temp_rej_orders", df_reject_orders)
                con.execute("""
                    DELETE FROM reject_orders 
                    WHERE (order_id, error_code) IN (
                        SELECT order_id, error_code FROM temp_rej_orders
                    );
                    INSERT INTO reject_orders (
                        reject_id, batch_id, order_id, store_id, raw_date,
                        raw_phone, raw_amount, error_code, rejection_reason, rejected_at
                    )
                    SELECT 
                        reject_id, batch_id, order_id, store_id, raw_date,
                        raw_phone, raw_amount, error_code, rejection_reason, CURRENT_TIMESTAMP
                    FROM temp_rej_orders;
                """)
                con.unregister("temp_rej_orders")

            if df_reject_items is not None and not df_reject_items.empty:
                con.register("temp_rej_items", df_reject_items)
                con.execute("""
                    DELETE FROM reject_order_items 
                    WHERE (order_id, store_id, product_code, error_code) IN (
                        SELECT order_id, store_id, product_code, error_code FROM temp_rej_items
                    );
                    INSERT INTO reject_order_items (
                        reject_id, batch_id, order_id, store_id, product_code,
                        quantity, unit_price, line_total, calculated_total, diff_amount,
                        error_code, rejection_reason, rejected_at
                    )
                    SELECT 
                        reject_id, batch_id, order_id, store_id, product_code,
                        quantity, unit_price, line_total, calculated_total, diff_amount,
                        error_code, rejection_reason, CURRENT_TIMESTAMP
                    FROM temp_rej_items;
                """)
                con.unregister("temp_rej_items")

            logger.info("Successfully loaded reject tables.")
        finally:
            con.close()

    def record_audit_log(
        self,
        batch_id: str,
        ext_orders: int,
        ext_items: int,
        clean_orders: int,
        clean_items: int,
        rej_orders: int,
        rej_items: int,
        fact_loaded: int,
        duration: float,
        status: str = "SUCCESS"
    ):
        con = self.get_connection()
        try:
            con.execute("""
                INSERT OR REPLACE INTO etl_audit_log (
                    batch_id, pipeline_run_at, extracted_orders_count, extracted_items_count,
                    clean_orders_count, clean_items_count, rejected_orders_count, rejected_items_count,
                    fact_sales_loaded, duration_seconds, status
                ) VALUES (?, CURRENT_TIMESTAMP, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, [batch_id, ext_orders, ext_items, clean_orders, clean_items, rej_orders, rej_items, fact_loaded, duration, status])
        finally:
            con.close()

    def get_table_counts(self) -> Dict[str, int]:
        """Dem so dong trong tat ca cac bang DWH de kiem chung khi cham diem"""
        con = self.get_connection()
        tables = [
            "dim_date", "dim_store", "dim_product", "dim_customer",
            "fact_sales", "reject_orders", "reject_order_items", "etl_audit_log"
        ]
        counts = {}
        try:
            for tbl in tables:
                res = con.execute(f"SELECT COUNT(*) FROM {tbl};").fetchone()
                counts[tbl] = res[0] if res else 0
        finally:
            con.close()
        return counts
