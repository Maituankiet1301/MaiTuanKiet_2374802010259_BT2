#!/usr/bin/env python3
"""
Điểm khởi chạy duy nhất cho Pipeline ETL Luồng L6 - Mekong Mobile Smart CRM
Cách dùng:
    python run_pipeline.py
"""

import sys
import os

# Đảm bảo import được module trong src/
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.pipeline import MekongDataPipeline

def main():
    print("\n" + "#" * 70)
    print("   MEKONG MOBILE SMART CRM - KHO DỮ LIỆU BÁN HÀNG & BÁO CÁO DOANH THU (L6)")
    print("   Thực hiện: Mai Tuấn Kiệt - MSSV: 2374802010259 - Track DA")
    print("#" * 70)
    
    pipeline = MekongDataPipeline()
    result = pipeline.run(verbose=True)
    
    if result["fact_rows_loaded"] > 0:
        print("[SUCCESS] Pipeline chạy thành công và đã nạp kho dữ liệu DuckDB.")
        sys.exit(0)
    else:
        print("[ERROR] Không có dòng nào được nạp vào Fact.")
        sys.exit(1)

if __name__ == "__main__":
    main()
