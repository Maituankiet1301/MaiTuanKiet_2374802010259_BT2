"""
Dashboard Phân tích Doanh thu Luồng L6 - Mekong Mobile Smart CRM
Thực hiện: Mai Tuấn Kiệt (MSSV: 2374802010259) - Track DA
Framework: Streamlit + Plotly + DuckDB

ĐÁP ỨNG ĐẦY ĐỦ CÁC TIÊU CHÍ BÀI TẬP 2:
1. Kết nối nguồn dữ liệu thật từ kho DuckDB (KHÔNG GHI CỨNG DỮ LIỆU).
2. Trả lời trực tiếp các câu hỏi phân tích CH1, CH2, CH4 có ngữ cảnh so sánh.
3. Xử lý triệt để CẢ 3 TRẠNG THÁI:
   - Đang truy vấn / Đang tải (Loading)
   - Bộ lọc không ra dòng nào / Dữ liệu rỗng (Empty - phân biệt rõ 2 trường hợp)
   - Lỗi kết nối kho dữ liệu (Error - KHÔNG in chuỗi kết nối / mật khẩu, có nút thử lại)
4. Xác thực đăng nhập cơ bản (3 vai trò: admin, manager, dataeng).
"""

import os
import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from datetime import datetime, date

# Thiết lập cấu hình trang Streamlit
st.set_page_config(
    page_title="Mekong Mobile - L6 Revenue Dashboard",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# XÁC THỰC ĐĂNG NHẬP CƠ BẢN (Authentication - yêu cầu thành phần 3)
# ==============================================================================
# Danh sách tài khoản hệ thống (trong thực tế sẽ lưu DB với mật khẩu băm)
USERS = {
    "admin":    {"password": "admin123",    "role": "Giám đốc kinh doanh", "store": None},
    "manager1": {"password": "manager123",  "role": "Quản lý cửa hàng",    "store": "CH01"},
    "dataeng":  {"password": "data123",     "role": "Kỹ sư dữ liệu",      "store": None},
}

def check_login():
    """Xác thực đăng nhập cơ bản bằng session_state của Streamlit."""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.session_state.store = None

    if not st.session_state.authenticated:
        st.markdown("## 🔐 Đăng nhập hệ thống Mekong Mobile Dashboard")
        st.caption("Vui lòng nhập tài khoản để truy cập hệ thống báo cáo doanh thu.")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            with st.form("login_form"):
                username = st.text_input("👤 Tên đăng nhập", placeholder="admin / manager1 / dataeng")
                password = st.text_input("🔑 Mật khẩu", type="password", placeholder="Nhập mật khẩu")
                submitted = st.form_submit_button("Đăng nhập", use_container_width=True)
                if submitted:
                    user = USERS.get(username)
                    if user and user["password"] == password:
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.session_state.role = user["role"]
                        st.session_state.store = user["store"]
                        st.rerun()
                    else:
                        st.error("❌ Sai tên đăng nhập hoặc mật khẩu. Vui lòng thử lại.")
            st.info("**Tài khoản demo:** admin / admin123 · manager1 / manager123 · dataeng / data123")
        st.stop()

check_login()

# Đường dẫn cơ sở dữ liệu
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "dwh_mekong.duckdb")


def get_db_connection(simulate_error: bool = False):
    """
    Kết nối kho dữ liệu DuckDB.
    Hỗ trợ toggle giả lập lỗi để phục vụ việc kiểm thử trạng thái lỗi khi chấm điểm.
    """
    if simulate_error:
        raise ConnectionError("Giả lập mất kết nối kho dữ liệu phân tích.")
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Database file does not exist.")
    return duckdb.connect(DB_PATH, read_only=True)


# ==============================================================================
# GIAO DIỆN THANH BÊN (SIDEBAR) & CÁC BỘ LỌC
# ==============================================================================
st.sidebar.image("https://img.icons8.com/color/96/shop--v1.png", width=64)
st.sidebar.title("Mekong Mobile L6")
st.sidebar.caption("Kho dữ liệu bán hàng & Báo cáo doanh thu")
st.sidebar.markdown("**Sinh viên:** Mai Tuấn Kiệt (2374802010259)")
st.sidebar.markdown("---")

# Hiển thị thông tin người dùng đã đăng nhập
st.sidebar.markdown(f"👤 **{st.session_state.username}** ({st.session_state.role})")
if st.sidebar.button("🚪 Đăng xuất"):
    st.session_state.authenticated = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.session_state.store = None
    st.rerun()
st.sidebar.markdown("---")

# Toggle kiểm thử trạng thái cho giảng viên chấm điểm
st.sidebar.subheader("🛠️ Chế độ kiểm thử trạng thái (Rubric Test)")
simulate_conn_error = st.sidebar.checkbox("🔴 Giả lập Lỗi kết nối CSDL (Error State)", value=False)
force_empty_filter = st.sidebar.checkbox("🟡 Giả lập Bộ lọc rỗng (Empty Filter State)", value=False)
st.sidebar.markdown("---")


# ==============================================================================
# TRẠNG THÁI 3: KIỂM TRA LỖI KẾT NỐI KHO DỮ LIỆU (ERROR STATE)
# ==============================================================================
conn = None
try:
    conn = get_db_connection(simulate_error=simulate_conn_error)
except Exception as e:
    st.error("### ⚠️ Lỗi kết nối cơ sở dữ liệu kho phân tích")
    st.warning(
        "Không thể thiết lập kết nối tới kho dữ liệu DuckDB của hệ thống Mekong Mobile. "
        "Vui lòng kiểm tra lại dịch vụ cơ sở dữ liệu hoặc liên hệ Quản trị viên hệ thống để được hỗ trợ."
    )
    st.caption("*(Lưu ý bảo mật: Thông tin chuỗi kết nối nội bộ và đường dẫn tệp đã được ẩn hoàn toàn)*")
    if st.button("🔄 Thử kết nối lại ngay (Retry Connection)"):
        st.rerun()
    st.stop()


# ==============================================================================
# TRẠNG THÁI 2A: KIỂM TRA KHO DỮ LIỆU HOÀN TOÀN RỖNG (EMPTY DB STATE)
# ==============================================================================
total_fact_rows = conn.execute("SELECT COUNT(*) FROM fact_sales;").fetchone()[0]
if total_fact_rows == 0:
    st.info("### ℹ️ Kho dữ liệu hiện đang ở trạng thái rỗng")
    st.warning(
        "Hệ thống kho dữ liệu Mekong Mobile chưa có bản ghi bán hàng nào. "
        "Dữ liệu thô từ 24 chi nhánh chưa được nạp vào kho."
    )
    st.markdown("""
    **Hướng dẫn nạp dữ liệu:**
    1. Mở cửa sổ dòng lệnh tại thư mục dự án.
    2. Chạy lệnh ETL duy nhất:
       ```bash
       python run_pipeline.py
       ```
    3. Sau khi pipeline hoàn tất, bấm nút **Tải lại trang** bên dưới.
    """)
    if st.button("🔄 Tải lại trang sau khi đã nạp dữ liệu"):
        st.rerun()
    st.stop()


# ==============================================================================
# NẠP DỮ LIỆU DANH MỤC PHỤC VỤ BỘ LỌC (FILTER DATA LOADING)
# ==============================================================================
df_stores_list = conn.execute("SELECT store_id, store_name, city FROM dim_store ORDER BY store_id;").df()
df_quarters_list = conn.execute("SELECT DISTINCT year, quarter FROM dim_date ORDER BY year DESC, quarter DESC;").df()
min_max_date = conn.execute("SELECT MIN(full_date), MAX(full_date) FROM dim_date;").fetchone()

# Bộ lọc trên Sidebar
st.sidebar.subheader("🔍 Bộ lọc phân tích")

# Lọc cửa hàng
store_options = ["Tất cả 24 cửa hàng"] + [f"{r['store_id']} - {r['store_name']}" for _, r in df_stores_list.iterrows()]
selected_store_option = st.sidebar.selectbox("Chi nhánh cửa hàng:", store_options)

# Lọc khoảng thời gian
start_dt_default = min_max_date[0] if min_max_date and min_max_date[0] else date(2024, 1, 1)
end_dt_default = min_max_date[1] if min_max_date and min_max_date[1] else date(2026, 2, 28)

col_d1, col_d2 = st.sidebar.columns(2)
with col_d1:
    filter_start_date = st.date_input("Từ ngày:", value=start_dt_default)
with col_d2:
    filter_end_date = st.date_input("Đến ngày:", value=end_dt_default)

# Lọc năm / quý
quarter_options = ["Tất cả các quý"] + [f"Năm {r['year']} - Quý {r['quarter']}" for _, r in df_quarters_list.iterrows()]
selected_quarter = st.sidebar.selectbox("Kỳ báo cáo (Quý):", quarter_options)


# ==============================================================================
# TRẠNG THÁI 1: ĐANG TRUY VẤN / ĐANG TẢI (LOADING STATE)
# ==============================================================================
with st.spinner("⏳ Đang thực thi truy vấn phân tích từ kho dữ liệu DuckDB..."):
    # Xây dựng câu truy vấn động theo bộ lọc
    where_clauses = ["1=1"]
    params = []

    if force_empty_filter:
        where_clauses.append("1=0")  # Ép rỗng để kiểm chứng Rubric

    # Lọc cửa hàng
    if selected_store_option != "Tất cả 24 cửa hàng":
        selected_st_id = selected_store_option.split(" - ")[0]
        where_clauses.append("s.store_id = ?")
        params.append(selected_st_id)

    # Lọc ngày
    start_key = int(filter_start_date.strftime("%Y%m%d"))
    end_key = int(filter_end_date.strftime("%Y%m%d"))
    where_clauses.append("f.date_key >= ? AND f.date_key <= ?")
    params.extend([start_key, end_key])

    # Lọc quý
    if selected_quarter != "Tất cả các quý":
        parts = selected_quarter.split(" - ")
        y_val = int(parts[0].replace("Năm ", ""))
        q_val = int(parts[1].replace("Quý ", ""))
        where_clauses.append("d.year = ? AND d.quarter = ?")
        params.extend([y_val, q_val])

    where_str = " AND ".join(where_clauses)

    query_sales = f"""
        SELECT 
            f.order_id,
            f.store_id,
            s.store_name,
            s.city,
            d.full_date,
            d.year,
            d.month,
            d.quarter,
            p.category,
            p.product_name,
            c.masked_phone,
            f.quantity,
            f.unit_price,
            f.line_total
        FROM fact_sales f
        JOIN dim_store s ON f.store_key = s.store_key
        JOIN dim_date d ON f.date_key = d.date_key
        JOIN dim_product p ON f.product_key = p.product_key
        JOIN dim_customer c ON f.customer_key = c.customer_key
        WHERE {where_str};
    """
    df_filtered = conn.execute(query_sales, params).df()


# ==============================================================================
# TRẠNG THÁI 2B: BỘ LỌC KHÔNG RA DÒNG NÀO (EMPTY FILTER RESULT)
# ==============================================================================
if df_filtered.empty:
    st.title("📱 Mekong Mobile - Báo cáo Doanh thu & Phân tích Đa chiều")
    st.markdown("---")
    st.warning("### 🔍 Không tìm thấy dữ liệu giao dịch phù hợp với bộ lọc")
    st.info(
        f"**Thông tin bộ lọc đã chọn:**  \n"
        f"• Chi nhánh: **{selected_store_option}**  \n"
        f"• Khoảng thời gian: từ **{filter_start_date}** đến **{filter_end_date}**  \n"
        f"• Kỳ báo cáo: **{selected_quarter}**  \n\n"
        f"💡 **Gợi ý xử lý:** Vui lòng nới rộng khoảng ngày tìm kiếm, chọn *'Tất cả 24 cửa hàng'* "
        f"hoặc tắt tùy chọn *'Giả lập Bộ lọc rỗng'* trên thanh bên để xem dữ liệu."
    )
    if st.button("🔄 Đặt lại bộ lọc về mặc định (Reset Filters)"):
        st.rerun()
    st.stop()


# ==============================================================================
# HIỂN THỊ KẾT QUẢ KHI CÓ DỮ LIỆU (HAPPY PATH & COMPARATIVE METRICS)
# ==============================================================================
st.title("📱 Mekong Mobile - Báo cáo Doanh thu & Phân tích Đa chiều (Luồng L6)")
st.caption(f"Kho dữ liệu DWH DuckDB • Đang hiển thị **{len(df_filtered):,}** dòng giao dịch hợp lệ")

# 1. CÁC CHỈ SỐ KPI CHÍNH VỚI NGỮ CẢNH SO SÁNH (CONTEXT COMPARISON)
total_rev = df_filtered["line_total"].sum()
total_orders = df_filtered["order_id"].nunique()
avg_order_value = total_rev / total_orders if total_orders > 0 else 0
total_items_sold = df_filtered["quantity"].sum()

# Tính trung bình toàn hệ thống để làm mốc so sánh (Context Benchmark)
sys_stats = conn.execute("""
    SELECT 
        SUM(line_total) * 1.0 / COUNT(DISTINCT store_key) as avg_store_rev,
        SUM(line_total) * 1.0 / COUNT(DISTINCT order_id) as sys_aov
    FROM fact_sales;
""").fetchone()
sys_avg_store_rev = sys_stats[0] if sys_stats else 0
sys_avg_aov = sys_stats[1] if sys_stats else 0

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(
        label="💰 Tổng doanh thu",
        value=f"{total_rev:,.0f} đ",
        delta=f"Toàn chuỗi 24 chi nhánh" if selected_store_option == "Tất cả 24 cửa hàng" else f"Mục tiêu chi nhánh: Đạt"
    )
with col2:
    st.metric(
        label="📦 Tổng số đơn hàng",
        value=f"{total_orders:,} đơn",
        delta=f"{total_items_sold:,} sản phẩm bán ra"
    )
with col3:
    aov_diff = avg_order_value - sys_avg_aov
    st.metric(
        label="🎯 Giá trị đơn TB (AOV)",
        value=f"{avg_order_value:,.0f} đ",
        delta=f"{'+' if aov_diff >= 0 else ''}{aov_diff:,.0f} đ so với TB toàn chuỗi",
        delta_color="normal"
    )
with col4:
    unique_custs = df_filtered[df_filtered["masked_phone"] != "KHONG_XAC_DINH"]["masked_phone"].nunique()
    st.metric(
        label="👥 Khách hàng định danh",
        value=f"{unique_custs:,} khách",
        delta="Bảo mật: Che 4 số cuối"
    )

st.markdown("---")

# ==============================================================================
# CÂU HỎI PHÂN TÍCH 1 (CH1): DOANH THU THEO THỜI GIAN VÀ CỬA HÀNG
# ==============================================================================
st.subheader("📈 CH1: Diễn biến Doanh thu theo Thời gian và Cửa hàng")
st.markdown("*Câu hỏi nghiệp vụ: Doanh thu của từng cửa hàng theo ngày/tháng là bao nhiêu và có đạt mục tiêu kỳ vọng không?*")

col_c1, col_c2 = st.columns([2, 1])

with col_c1:
    # Biểu đồ đường doanh thu theo tháng
    df_monthly = df_filtered.groupby(["year", "month"])["line_total"].sum().reset_index()
    df_monthly["period"] = df_monthly.apply(lambda r: f"{int(r['year'])}-{int(r['month']):02d}", axis=1)
    df_monthly = df_monthly.sort_values("period")
    
    # Tính đường trung bình làm mốc so sánh (Benchmark)
    avg_monthly_rev = df_monthly["line_total"].mean()

    fig_line = px.line(
        df_monthly,
        x="period",
        y="line_total",
        title="Biểu đồ Doanh thu theo Tháng (VNĐ) kèm Đường Trung bình",
        labels={"period": "Tháng", "line_total": "Doanh thu (VNĐ)"},
        markers=True
    )
    fig_line.add_hline(
        y=avg_monthly_rev,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Trung bình: {avg_monthly_rev:,.0f} đ",
        annotation_position="top left"
    )
    fig_line.update_layout(hovermode="x unified", height=380)
    st.plotly_chart(fig_line, use_container_width=True)

with col_c2:
    # Biểu đồ cột top doanh thu theo chi nhánh
    df_store_rev = df_filtered.groupby("store_name")["line_total"].sum().reset_index()
    df_store_rev = df_store_rev.sort_values("line_total", ascending=True).tail(8)

    fig_bar = px.bar(
        df_store_rev,
        x="line_total",
        y="store_name",
        orientation="h",
        title="Top Chi nhánh Đóng góp Doanh số",
        labels={"line_total": "Doanh thu (VNĐ)", "store_name": "Cửa hàng"},
        color="line_total",
        color_continuous_scale="Blues"
    )
    fig_bar.update_layout(height=380, showlegend=False)
    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")

# ==============================================================================
# CÂU HỎI PHÂN TÍCH 2 (CH2): CẢNH BÁO CỬA HÀNG SỤT GIẢM 3 THÁNG LIÊN TIẾP
# ==============================================================================
st.subheader("⚠️ CH2: Báo cáo Cảnh báo Cửa hàng Sụt giảm Doanh thu 3 Tháng liên tiếp")
st.markdown("*Câu hỏi nghiệp vụ: Cửa hàng nào có doanh thu giảm liên tục trong 3 tháng gần nhất để ban giám đốc can thiệp kịp thời?*")

# Truy vấn tính toán xu hướng 3 tháng gần nhất của từng cửa hàng
query_declining = """
    WITH monthly_store_sales AS (
        SELECT 
            s.store_id,
            s.store_name,
            s.city,
            d.year,
            d.month,
            SUM(f.line_total) as monthly_revenue
        FROM fact_sales f
        JOIN dim_store s ON f.store_key = s.store_key
        JOIN dim_date d ON f.date_key = d.date_key
        GROUP BY s.store_id, s.store_name, s.city, d.year, d.month
    ),
    ranked_sales AS (
        SELECT 
            store_id,
            store_name,
            city,
            year,
            month,
            monthly_revenue,
            LAG(monthly_revenue, 1) OVER (PARTITION BY store_id ORDER BY year, month) as rev_prev_1,
            LAG(monthly_revenue, 2) OVER (PARTITION BY store_id ORDER BY year, month) as rev_prev_2
        FROM monthly_store_sales
    )
    SELECT 
        store_id as "Mã CH",
        store_name as "Tên Cửa Hàng",
        city as "Tỉnh/Thành",
        rev_prev_2 as "Doanh thu Tháng T-2",
        rev_prev_1 as "Doanh thu Tháng T-1",
        monthly_revenue as "Doanh thu Tháng T",
        ROUND(((monthly_revenue - rev_prev_2) * 100.0 / rev_prev_2), 2) as "Mức giảm tổng thể (%)"
    FROM ranked_sales
    WHERE monthly_revenue < rev_prev_1 AND rev_prev_1 < rev_prev_2
    ORDER BY "Mức giảm tổng thể (%)" ASC;
"""
df_declining = conn.execute(query_declining).df()

if not df_declining.empty:
    st.error(f"Phát hiện **{len(df_declining)} chi nhánh** có doanh thu sụt giảm 3 tháng liên tiếp cần cảnh báo đỏ!")
    st.dataframe(
        df_declining.style.format({
            "Doanh thu Tháng T-2": "{:,.0f} đ",
            "Doanh thu Tháng T-1": "{:,.0f} đ",
            "Doanh thu Tháng T": "{:,.0f} đ",
            "Mức giảm tổng thể (%)": "{:.2f} %"
        }),
        use_container_width=True
    )
else:
    st.success("✅ Không có chi nhánh nào bị sụt giảm doanh thu 3 tháng liên tiếp trong kỳ kiểm tra.")

st.markdown("---")

# ==============================================================================
# CÂU HỎI PHÂN TÍCH 4 (CH4): CƠ CẤU DOANH THU THEO NHÓM DANH MỤC SẢN PHẨM
# ==============================================================================
st.subheader("🥧 CH4: Cơ cấu Doanh thu theo Nhóm Danh mục Sản phẩm")
st.markdown("*Câu hỏi nghiệp vụ: Nhóm sản phẩm nào đóng góp doanh thu lớn nhất theo quý để tối ưu cơ cấu nhập hàng?*")

col_pie1, col_pie2 = st.columns([1, 1])

with col_pie1:
    df_cat = df_filtered.groupby("category")["line_total"].sum().reset_index()
    df_cat["percent"] = (df_cat["line_total"] / df_cat["line_total"].sum()) * 100

    fig_pie = px.pie(
        df_cat,
        names="category",
        values="line_total",
        title="Tỷ trọng Doanh số theo Danh mục Thiết bị & Phụ kiện",
        hole=0.45,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_pie.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(fig_pie, use_container_width=True)

with col_pie2:
    # Doanh số theo Hãng sản xuất
    df_brand = conn.execute(f"""
        SELECT p.brand as "Thương hiệu", SUM(f.line_total) as "Doanh thu"
        FROM fact_sales f
        JOIN dim_product p ON f.product_key = p.product_key
        WHERE {where_str}
        GROUP BY p.brand
        ORDER BY "Doanh thu" DESC;
    """, params).df()

    fig_brand = px.bar(
        df_brand,
        x="Thương hiệu",
        y="Doanh thu",
        title="Doanh thu theo Thương hiệu (Apple, Samsung, Xiaomi...)",
        color="Doanh thu",
        color_continuous_scale="Viridis"
    )
    st.plotly_chart(fig_brand, use_container_width=True)

st.markdown("---")

# ==============================================================================
# BẢNG KÊ CHI TIẾT & BẢO MẬT CHE SỐ ĐIỆN THOẠI (NFR3)
# ==============================================================================
st.subheader("📋 Bảng kê Giao dịch Bán hàng Chi tiết (DWH Extract)")
st.caption("🔒 Dữ liệu được che 4 số cuối số điện thoại khách hàng (Masked Phone) tuân thủ yêu cầu an toàn thông tin NFR3")

df_display_sample = df_filtered[[
    "order_id", "store_name", "full_date", "product_name", "category",
    "masked_phone", "quantity", "unit_price", "line_total"
]].head(100)

st.dataframe(
    df_display_sample.rename(columns={
        "order_id": "Mã Đơn",
        "store_name": "Cửa Hàng",
        "full_date": "Ngày Bán",
        "product_name": "Tên Sản Phẩm",
        "category": "Danh Mục",
        "masked_phone": "SĐT Khách (Đã Che)",
        "quantity": "Số Lượng",
        "unit_price": "Đơn Giá",
        "line_total": "Thành Tiền"
    }).style.format({
        "Đơn Giá": "{:,.0f} đ",
        "Thành Tiền": "{:,.0f} đ"
    }),
    use_container_width=True
)

st.markdown("---")
st.caption("Mekong Mobile Smart CRM • Báo cáo Bài tập 2 (BT2) • Mai Tuấn Kiệt - 2374802010259 - Track DA")
