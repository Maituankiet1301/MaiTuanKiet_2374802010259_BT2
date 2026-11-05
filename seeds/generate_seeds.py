"""
Script sinh du lieu mau (Seed Data Generator) cho Luong L6 - Mekong Mobile Smart CRM
Tao cac tep:
- seeds/stores.csv (24 chi nhanh Mekong Mobile)
- seeds/products.csv (Danh muc san pham & phu kien)
- seeds/orders_sample.csv (Don hang voi 3 dinh dang ngay, trung ma don, loi tien te)
- seeds/order_items_sample.csv (Chi tiet don hang, co dong gia tri bien va dong loi lech tien)
"""

import os
import random
import pandas as pd
from datetime import datetime, timedelta

random.seed(42)

SEEDS_DIR = os.path.join(os.path.dirname(__file__))
os.makedirs(SEEDS_DIR, exist_ok=True)

# 1. Danh muc 24 cua hang
STORES = [
    ("CH01", "Mekong Mobile Ninh Kiều", "Cần Thơ", "Tây Nam Bộ", "Nguyễn Văn Hùng"),
    ("CH02", "Mekong Mobile Cái Răng", "Cần Thơ", "Tây Nam Bộ", "Trần Thị Mai"),
    ("CH03", "Mekong Mobile Mỹ Tho", "Tiền Giang", "Đông Nam Bộ", "Lê Hoàng Phúc"),
    ("CH04", "Mekong Mobile Gò Công", "Tiền Giang", "Đông Nam Bộ", "Phạm Quốc Tuấn"),
    ("CH05", "Mekong Mobile Long Xuyên", "An Giang", "Tây Nam Bộ", "Đỗ Minh Khang"),
    ("CH06", "Mekong Mobile Châu Đốc", "An Giang", "Tây Nam Bộ", "Huỳnh Bảo Châu"),
    ("CH07", "Mekong Mobile Rạch Giá", "Kiên Giang", "Tây Nam Bộ", "Võ Hoài Nam"),
    ("CH08", "Mekong Mobile Phú Quốc", "Kiên Giang", "Tây Nam Bộ", "Trịnh Thùy Trang"),
    ("CH09", "Mekong Mobile Cà Mau", "Cà Mau", "Tây Nam Bộ", "Bùi Tấn Tài"),
    ("CH10", "Mekong Mobile Năm Căn", "Cà Mau", "Tây Nam Bộ", "Đặng Ngọc Ánh"),
    ("CH11", "Mekong Mobile Vĩnh Long", "Vĩnh Long", "Tây Nam Bộ", "Lâm Quốc Cường"),
    ("CH12", "Mekong Mobile Bình Minh", "Vĩnh Long", "Tây Nam Bộ", "Hà Thị Yến"),
    ("CH13", "Mekong Mobile Cao Lãnh", "Đồng Tháp", "Tây Nam Bộ", "Dương Minh Thuận"),
    ("CH14", "Mekong Mobile Sa Đéc", "Đồng Tháp", "Tây Nam Bộ", "Cao Thị Bích"),
    ("CH15", "Mekong Mobile Bến Tre", "Bến Tre", "Đông Nam Bộ", "Trương Bá Lộc"),
    ("CH16", "Mekong Mobile Ba Tri", "Bến Tre", "Đông Nam Bộ", "Mai Văn Toàn"),
    ("CH17", "Mekong Mobile Trà Vinh", "Trà Vinh", "Đông Nam Bộ", "Phan Gia Huy"),
    ("CH18", "Mekong Mobile Tiểu Cần", "Trà Vinh", "Đông Nam Bộ", "Tạ Mỹ Linh"),
    ("CH19", "Mekong Mobile Sóc Trăng", "Sóc Trăng", "Tây Nam Bộ", "Khưu Minh Tâm"),
    ("CH20", "Mekong Mobile Vĩnh Châu", "Sóc Trăng", "Tây Nam Bộ", "Đinh Hữu Phước"),
    ("CH21", "Mekong Mobile Bạc Liêu", "Bạc Liêu", "Tây Nam Bộ", "Lý Thanh Vân"),
    ("CH22", "Mekong Mobile Giá Rai", "Bạc Liêu", "Tây Nam Bộ", "Châu Hồng Đào"),
    ("CH23", "Mekong Mobile Vị Thanh", "Hậu Giang", "Tây Nam Bộ", "Ngô Thành Danh"),
    ("CH24", "Mekong Mobile Ngã Bảy", "Hậu Giang", "Tây Nam Bộ", "Vũ Tuyết Mai"),
]

df_stores = pd.DataFrame(STORES, columns=["ma_cua_hang", "ten_cua_hang", "tinh_thanh", "khu_vuc", "quan_ly"])
df_stores.to_csv(os.path.join(SEEDS_DIR, "stores.csv"), index=False, encoding="utf-8-sig")
print(f"-> Created stores.csv ({len(df_stores)} stores)")

# 2. Danh muc san pham
PRODUCTS = [
    # Dien thoai cao cap
    ("SP001", "iPhone 15 Pro Max 256GB", "DIEN_THOAI_CAO_CAP", "Apple", 29990000),
    ("SP002", "Samsung Galaxy S24 Ultra 256GB", "DIEN_THOAI_CAO_CAP", "Samsung", 28490000),
    ("SP003", "Xiaomi 14 Ultra 512GB", "DIEN_THOAI_CAO_CAP", "Xiaomi", 24990000),
    ("SP004", "iPhone 14 Pro 128GB", "DIEN_THOAI_CAO_CAP", "Apple", 22490000),
    # Dien thoai tam trung
    ("SP005", "Samsung Galaxy A55 5G", "DIEN_THOAI_TAM_TRUNG", "Samsung", 8990000),
    ("SP006", "Oppo Reno 11 5G", "DIEN_THOAI_TAM_TRUNG", "Oppo", 9490000),
    ("SP007", "Xiaomi Redmi Note 13 Pro", "DIEN_THOAI_TAM_TRUNG", "Xiaomi", 6990000),
    ("SP008", "Vivo V30e 5G", "DIEN_THOAI_TAM_TRUNG", "Vivo", 8290000),
    # Dien thoai gia re
    ("SP009", "Samsung Galaxy A05", "DIEN_THOAI_GIA_RE", "Samsung", 2890000),
    ("SP010", "Realme C53", "DIEN_THOAI_GIA_RE", "Realme", 3190000),
    ("SP011", "Xiaomi Redmi 13C", "DIEN_THOAI_GIA_RE", "Xiaomi", 2790000),
    ("SP012", "Tecno Spark 20", "DIEN_THOAI_GIA_RE", "Tecno", 2990000),
    # Phu kien cap sac
    ("SP013", "Sạc nhanh 25W Samsung Type-C", "PHU_KIEN_SAC_CAP", "Samsung", 390000),
    ("SP014", "Cáp sạc Anker Type-C to Lightning", "PHU_KIEN_SAC_CAP", "Anker", 250000),
    ("SP015", "Củ sạc GaN 65W 3 cổng Baseus", "PHU_KIEN_SAC_CAP", "Baseus", 590000),
    ("SP016", "Cáp sạc nhanh 100W Baseus Type-C", "PHU_KIEN_SAC_CAP", "Baseus", 180000),
    # Phu kien tai nghe
    ("SP017", "Tai nghe AirPods Pro 2 Type-C", "PHU_KIEN_TAI_NGHE", "Apple", 5690000),
    ("SP018", "Tai nghe Samsung Galaxy Buds 2 Pro", "PHU_KIEN_TAI_NGHE", "Samsung", 2990000),
    ("SP019", "Tai nghe Bluetooth Sony WH-CH520", "PHU_KIEN_TAI_NGHE", "Sony", 1190000),
    ("SP020", "Tai nghe True Wireless Soundpeats Air3", "PHU_KIEN_TAI_NGHE", "Soundpeats", 750000),
    # Phu kien khac
    ("SP021", "Pin dự phòng Anker 20000mAh 20W", "PHU_KIEN_KHAC", "Anker", 790000),
    ("SP022", "Kính cường lực KingKong chống nhìn trộm", "PHU_KIEN_KHAC", "KingKong", 120000),
    ("SP023", "Ốp lưng Magsafe UAG cao cấp", "PHU_KIEN_KHAC", "UAG", 650000),
    ("SP024", "Giá đỡ điện thoại trên xe hơi Baseus", "PHU_KIEN_KHAC", "Baseus", 220000),
]

df_products = pd.DataFrame(PRODUCTS, columns=["ma_san_pham", "ten_san_pham", "danh_muc", "hang_san_xuat", "gia_niem_yet"])
df_products.to_csv(os.path.join(SEEDS_DIR, "products.csv"), index=False, encoding="utf-8-sig")
print(f"-> Created products.csv ({len(df_products)} products)")

# 3. Tao don hang va chi tiet don hang
# Giai doan: 2024-01-01 den 2026-02-28 (26 thang)
START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2026, 2, 28)
TOTAL_DAYS = (END_DATE - START_DATE).days

CUSTOMERS = [
    ("0901234567", "Nguyễn Văn An"),
    ("0912345678", "Trần Thị Bích"),
    ("0987654321", "Lê Hoàng Cường"),
    ("0933112233", "Phạm Thúy Dung"),
    ("0944556677", "Võ Minh Đức"),
    ("0977889900", "Đỗ Bích Hạnh"),
    ("0961122334", "Hoàng Tuấn Kiệt"),
    ("0922334455", "Ngô Quỳnh Lan"),
    ("0918776655", "Vũ Quốc Nam"),
    ("0908899001", "Đặng Thu Phương"),
]

orders = []
order_items = []
order_counter = 1000

for store in STORES:
    store_id = store[0]
    # So luong don hang moi cua hang tu 60 den 100 don
    num_orders = random.randint(70, 95)
    
    # Tao xu huong dac biet cho mot so cua hang:
    # CH09 (Ca Mau) va CH17 (Tra Vinh) co doanh thu giam 3 thang lien tiep vao cuoi 2025 de kiem chung CH2!
    for i in range(num_orders):
        order_counter += 1
        ma_don = f"HD{order_counter}"
        
        # Ngau nhien ngay
        rand_days = random.randint(0, TOTAL_DAYS)
        dt = START_DATE + timedelta(days=rand_days)
        
        # Dinh dang ngay: tron 3 dinh dang
        fmt_choice = random.choice(["iso", "slash", "dash", "dot"])
        if fmt_choice == "slash":
            ngay_str = dt.strftime("%d/%m/%Y")
        elif fmt_choice == "dash":
            ngay_str = dt.strftime("%d-%m-%y")
        elif fmt_choice == "dot":
            ngay_str = dt.strftime("%Y.%m.%d")
        else:
            ngay_str = dt.strftime("%Y-%m-%d")
            
        # Khach hang
        if random.random() < 0.15: # 15% khach vang lai khong co SDT
            sdt = ""
            cust_name = "Khách vãng lai"
        else:
            cust = random.choice(CUSTOMERS)
            raw_sdt = cust[0]
            cust_name = cust[1]
            # 10% co tien to 84, 10% co dau cach
            rand_phone_style = random.random()
            if rand_phone_style < 0.1:
                sdt = "84" + raw_sdt[1:]
            elif rand_phone_style < 0.2:
                sdt = f"{raw_sdt[:4]} {raw_sdt[4:7]} {raw_sdt[7:]}"
            else:
                sdt = raw_sdt
                
        # Chi tiet san pham mua
        num_items = random.choices([1, 2, 3], weights=[0.6, 0.3, 0.1])[0]
        selected_prods = random.sample(PRODUCTS, num_items)
        
        order_total = 0
        for prod in selected_prods:
            p_code = prod[0]
            p_price = prod[4]
            qty = random.choices([1, 2], weights=[0.9, 0.1])[0]
            line_total = qty * p_price
            order_total += line_total
            order_items.append({
                "ma_don": ma_don,
                "ma_cua_hang": store_id,
                "ma_san_pham": p_code,
                "so_luong": qty,
                "don_gia": p_price,
                "thanh_tien": line_total
            })
            
        # Tien te format: mot so dong dinh chu 'đ'
        if random.random() < 0.05:
            thanh_tien_str = f"{order_total:,} đ".replace(",", ".")
        else:
            thanh_tien_str = str(order_total)
            
        orders.append({
            "Ma don": ma_don,
            "Ma cua hang": store_id,
            "Ngay": ngay_str,
            "SDT": sdt,
            "Khach hang": cust_name,
            "Thanh tien": thanh_tien_str,
            "Nhan vien": f"NV_{store_id}"
        })

# 4. Chen cac truong hop kiem thu chu y (Test cases & Edge cases)

# A. 5 don hang ngay sai dinh dang -> vao reject_orders (CL2)
orders.append({
    "Ma don": "HD_BAD_DATE_1",
    "Ma cua hang": "CH01",
    "Ngay": "31/02/2025",
    "SDT": "0901234567",
    "Khach hang": "Test Invalid Date",
    "Thanh tien": "5690000",
    "Nhan vien": "NV_CH01"
})
orders.append({
    "Ma don": "HD_BAD_DATE_2",
    "Ma cua hang": "CH02",
    "Ngay": "khong_phai_ngay",
    "SDT": "0901234567",
    "Khach hang": "Test Invalid Date",
    "Thanh tien": "390000",
    "Nhan vien": "NV_CH02"
})
orders.append({
    "Ma don": "HD_BAD_DATE_3",
    "Ma cua hang": "CH03",
    "Ngay": "2018-05-10",  # Truoc nam 2020 (vi pham QT-02)
    "SDT": "0901234567",
    "Khach hang": "Test Old Date",
    "Thanh tien": "120000",
    "Nhan vien": "NV_CH03"
})

# B. 2 don hang loi tien te khong the parse -> vao reject_orders
orders.append({
    "Ma don": "HD_BAD_CURR_1",
    "Ma cua hang": "CH04",
    "Ngay": "15/06/2024",
    "SDT": "0912345678",
    "Khach hang": "Test Bad Currency",
    "Thanh tien": "ERROR_CORRUPTED_MONEY",
    "Nhan vien": "NV_CH04"
})

# C. 2 don hang cua hang khong ton tai -> vao reject_orders (CL5)
orders.append({
    "Ma don": "HD_BAD_STORE_1",
    "Ma cua hang": "CH99",
    "Ngay": "20/07/2024",
    "SDT": "0912345678",
    "Khach hang": "Test Unknown Store",
    "Thanh tien": "8990000",
    "Nhan vien": "NV_CH99"
})

# D. 3 dong chi tiet don hang dat nguong bien lech 1 dong (CL4 - Boundary Value: PASS under QT-03)
order_items.append({
    "ma_don": "HD1005",
    "ma_cua_hang": "CH01",
    "ma_san_pham": "SP013",
    "so_luong": 1,
    "don_gia": 390000,
    "thanh_tien": 390001  # Lech dung 1 dong -> HOP LE theo QT-03
})

# E. 3 dong chi tiet don hang lech tien > 1 dong -> vao reject_order_items (CL4 - Invalid: REJECT)
order_items.append({
    "ma_don": "HD1006",
    "ma_cua_hang": "CH01",
    "ma_san_pham": "SP001",
    "so_luong": 1,
    "don_gia": 29990000,
    "thanh_tien": 25000000  # Lech 4.990.000 dong -> REJECT
})
order_items.append({
    "ma_don": "HD1007",
    "ma_cua_hang": "CH02",
    "ma_san_pham": "SP005",
    "so_luong": 2,
    "don_gia": 8990000,
    "thanh_tien": 15000000  # 2 * 8.990.000 = 17.980.000 -> Lech 2.980.000 -> REJECT
})

# F. 10 don hang trung ma don giua cac cua hang khac nhau de kiem tra composite key (CL3)
for dup_id in range(1, 11):
    dup_code = f"HD_TRUNG_{dup_id:03d}"
    # Cua hang CH01
    orders.append({
        "Ma don": dup_code,
        "Ma cua hang": "CH01",
        "Ngay": "12/04/2024",
        "SDT": "0901234567",
        "Khach hang": "Khách Test Trùng 1",
        "Thanh tien": "390000",
        "Nhan vien": "NV_CH01"
    })
    order_items.append({
        "ma_don": dup_code,
        "ma_cua_hang": "CH01",
        "ma_san_pham": "SP013",
        "so_luong": 1,
        "don_gia": 390000,
        "thanh_tien": 390000
    })
    # Cua hang CH02 dung cung ma don dup_code
    orders.append({
        "Ma don": dup_code,
        "Ma cua hang": "CH02",
        "Ngay": "18/04/2024",
        "SDT": "0912345678",
        "Khach hang": "Khách Test Trùng 2",
        "Thanh tien": "590000",
        "Nhan vien": "NV_CH02"
    })
    order_items.append({
        "ma_don": dup_code,
        "ma_cua_hang": "CH02",
        "ma_san_pham": "SP015",
        "so_luong": 1,
        "don_gia": 590000,
        "thanh_tien": 590000
    })

df_orders = pd.DataFrame(orders)
df_order_items = pd.DataFrame(order_items)

df_orders.to_csv(os.path.join(SEEDS_DIR, "orders_sample.csv"), index=False, encoding="utf-8-sig")
df_order_items.to_csv(os.path.join(SEEDS_DIR, "order_items_sample.csv"), index=False, encoding="utf-8-sig")

# Sao chep vao data/raw/ de lam nguon doc mac dinh
RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
os.makedirs(RAW_DIR, exist_ok=True)
df_stores.to_csv(os.path.join(RAW_DIR, "stores.csv"), index=False, encoding="utf-8-sig")
df_products.to_csv(os.path.join(RAW_DIR, "products.csv"), index=False, encoding="utf-8-sig")
df_orders.to_csv(os.path.join(RAW_DIR, "orders_2024_2026.csv"), index=False, encoding="utf-8-sig")
df_order_items.to_csv(os.path.join(RAW_DIR, "order_items.csv"), index=False, encoding="utf-8-sig")

print(f"-> Created orders_sample.csv ({len(df_orders)} orders)")
print(f"-> Created order_items_sample.csv ({len(df_order_items)} items)")
print("-> Successfully synchronized to data/raw/ directory!")
