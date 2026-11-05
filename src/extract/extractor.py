"""
Module trich xuat du lieu (Extract Layer)
Chiu trach nhiem doc cac tep CSV nguon tu data/raw/ hoac seeds/
"""

import os
import glob
import logging
import pandas as pd
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class DataExtractor:
    def __init__(self, raw_data_dir: Optional[str] = None, seeds_dir: Optional[str] = None):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.raw_data_dir = raw_data_dir or os.path.join(base_dir, "data", "raw")
        self.seeds_dir = seeds_dir or os.path.join(base_dir, "seeds")

    def _find_file(self, filename_patterns: list, preferred_dir: str, fallback_dir: str) -> Optional[str]:
        for pattern in filename_patterns:
            matches = glob.glob(os.path.join(preferred_dir, pattern))
            if matches:
                return matches[0]
        for pattern in filename_patterns:
            matches = glob.glob(os.path.join(fallback_dir, pattern))
            if matches:
                return matches[0]
        return None

    def extract_all(self) -> Dict[str, pd.DataFrame]:
        """
        Doc tat ca 4 bo du lieu cot loi:
        1. stores (24 cua hang)
        2. products (danh muc san pham)
        3. orders (don hang)
        4. order_items (chi tiet don hang)
        """
        logger.info(f"Extracting raw data from: {self.raw_data_dir} (fallback: {self.seeds_dir})")

        # 1. Stores
        stores_file = self._find_file(["stores.csv", "*store*.csv"], self.raw_data_dir, self.seeds_dir)
        if not stores_file or not os.path.exists(stores_file):
            raise FileNotFoundError(f"Cannot find stores.csv in {self.raw_data_dir} or {self.seeds_dir}")
        df_stores = pd.read_csv(stores_file, encoding="utf-8-sig")
        logger.info(f"Loaded stores: {len(df_stores)} records from {os.path.basename(stores_file)}")

        # 2. Products
        products_file = self._find_file(["products.csv", "*product*.csv"], self.raw_data_dir, self.seeds_dir)
        if not products_file or not os.path.exists(products_file):
            raise FileNotFoundError(f"Cannot find products.csv in {self.raw_data_dir} or {self.seeds_dir}")
        df_products = pd.read_csv(products_file, encoding="utf-8-sig")
        logger.info(f"Loaded products: {len(df_products)} records from {os.path.basename(products_file)}")

        # 3. Orders
        orders_file = self._find_file(["orders_2024_2026.csv", "orders_sample.csv", "*order*.csv"], self.raw_data_dir, self.seeds_dir)
        if not orders_file or not os.path.exists(orders_file):
            raise FileNotFoundError(f"Cannot find orders CSV in {self.raw_data_dir} or {self.seeds_dir}")
        df_orders = pd.read_csv(orders_file, encoding="utf-8-sig", dtype=str)
        logger.info(f"Loaded orders: {len(df_orders)} records from {os.path.basename(orders_file)}")

        # 4. Order items
        items_file = self._find_file(["order_items.csv", "order_items_sample.csv", "*item*.csv"], self.raw_data_dir, self.seeds_dir)
        if not items_file or not os.path.exists(items_file):
            raise FileNotFoundError(f"Cannot find order_items CSV in {self.raw_data_dir} or {self.seeds_dir}")
        df_items = pd.read_csv(items_file, encoding="utf-8-sig")
        # Ensure correct numeric types where possible
        for num_col in ["so_luong", "don_gia", "thanh_tien"]:
            if num_col in df_items.columns:
                df_items[num_col] = pd.to_numeric(df_items[num_col], errors="coerce").fillna(0).astype(int)
        logger.info(f"Loaded order items: {len(df_items)} records from {os.path.basename(items_file)}")

        return {
            "stores": df_stores,
            "products": df_products,
            "orders": df_orders,
            "order_items": df_items
        }
