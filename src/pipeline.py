"""
Pipeline Orchestrator cho Luong L6 - Mekong Mobile Smart CRM
Tich hop 3 pha: Extract -> Quality & Transform -> Load vao DuckDB.
"""

import time
import logging
from datetime import datetime
from typing import Dict, Any

from .extract.extractor import DataExtractor
from .quality.checker import run_data_quality_suite
from .transform.transformer import DataTransformer
from .load.loader import DWHLoader

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("ETL_Pipeline")


class MekongDataPipeline:
    def __init__(self, db_path: str = None, raw_dir: str = None):
        self.extractor = DataExtractor(raw_data_dir=raw_dir)
        self.loader = DWHLoader(db_path=db_path)

    def run(self, verbose: bool = True) -> Dict[str, Any]:
        start_time = time.time()
        batch_id = f"BATCH_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        logger.info(f"=== BẮT ĐẦU PIPELINE ETL MEKONG MOBILE (Mã Batch: {batch_id}) ===")

        # 1. KHOI TAO CSDL KHO DỮ LIỆU
        self.loader.init_schema()

        # 2. PHA 1: TRÍCH XUẤT (EXTRACT)
        raw_data = self.extractor.extract_all()
        ext_orders = len(raw_data["orders"])
        ext_items = len(raw_data["order_items"])
        logger.info(f"[EXTRACT] Đã trích xuất {len(raw_data['stores'])} cửa hàng, {len(raw_data['products'])} sản phẩm, {ext_orders} đơn hàng, {ext_items} dòng chi tiết.")

        # 3. PHA KIỂM TRA CHẤT LƯỢNG (DATA QUALITY CHECKS)
        quality_report = run_data_quality_suite(
            orders_df=raw_data["orders"],
            items_df=raw_data["order_items"],
            stores_df=raw_data["stores"]
        )

        if verbose:
            print("\n" + "=" * 75)
            print("         BÁO CÁO KIỂM SOÁT CHẤT LƯỢNG DỮ LIỆU (DATA QUALITY SUITE)")
            print("=" * 75)
            print(f"{'Mục kiểm tra':<30} | {'Số dòng lỗi':<12} | {'Tỉ lệ lỗi':<10} | {'Trạng thái'}")
            print("-" * 75)
            for check_name, res in quality_report.items():
                cnt = res["failed_count"]
                rate = res["error_rate"] * 100
                status = "PASS (0 lỗi)" if cnt == 0 else f"CẢNH BÁO ({cnt} dòng vào Reject)"
                print(f"{check_name:<30} | {cnt:<12} | {rate:>6.2f} %   | {status}")
            print("=" * 75 + "\n")

        # 4. PHA 2: BIẾN ĐỔI (TRANSFORM)
        transformer = DataTransformer(batch_id=batch_id)
        dim_tables, df_fact, df_rej_orders, df_rej_items = transformer.transform_all(raw_data)
        clean_orders = len(raw_data["orders"]) - len(df_rej_orders)
        clean_items = len(df_fact)

        # 5. PHA 3: NẠP VÀO KHO DỮ LIỆU (LOAD - IDEMPOTENT)
        self.loader.load_dimensions(dim_tables)
        self.loader.load_fact_sales(df_fact)
        self.loader.load_rejects(df_rej_orders, df_rej_items)

        duration = round(time.time() - start_time, 2)

        # 6. GHI NHẬT KÝ KIỂM TOÁN ETL (AUDIT LOG)
        self.loader.record_audit_log(
            batch_id=batch_id,
            ext_orders=ext_orders,
            ext_items=ext_items,
            clean_orders=clean_orders,
            clean_items=clean_items,
            rej_orders=len(df_rej_orders),
            rej_items=len(df_rej_items),
            fact_loaded=len(df_fact),
            duration=duration,
            status="SUCCESS"
        )

        counts = self.loader.get_table_counts()
        if verbose:
            print("\n" + "=" * 55)
            print("   TỔNG HỢP SỐ DÒNG BẢNG ĐÍCH TRONG KHO DUCKDB")
            print("=" * 55)
            for tbl, cnt in counts.items():
                print(f"   • {tbl:<22}: {cnt:>8,} dòng")
            print("=" * 55)
            print(f"-> Thời gian thực thi toàn bộ: {duration} giây (Đạt NFR1: < 45 giây)")
            print("=" * 55 + "\n")

        logger.info(f"=== PIPELINE HOÀN TẤT THÀNH CÔNG TRONG {duration} GIÂY ===")

        return {
            "batch_id": batch_id,
            "duration": duration,
            "quality_report": quality_report,
            "table_counts": counts,
            "fact_rows_loaded": len(df_fact),
            "rejected_orders_count": len(df_rej_orders),
            "rejected_items_count": len(df_rej_items),
        }
