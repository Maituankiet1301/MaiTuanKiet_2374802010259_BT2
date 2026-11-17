import os
import base64
import subprocess

def get_base64_image(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    print(f"Warning: image not found: {path}")
    return ""

print("Loading screenshot and diagram images...")
b64_full_pytest = get_base64_image("docs/screenshots/full-pytest-pass.png")
b64_clean_room  = get_base64_image("docs/screenshots/clean-room-test.png")
b64_docker_ps   = get_base64_image("docs/screenshots/docker-compose-health.png")
b64_pipeline    = get_base64_image("docs/screenshot_pipeline.png")
b64_dash_login  = get_base64_image("docs/screenshot_dashboard_login.png")
b64_dash_main   = get_base64_image("docs/screenshot_dashboard_main.png")
b64_dash_anl    = get_base64_image("docs/screenshot_dashboard_analysis.png")
b64_dash_empty  = get_base64_image("docs/screenshot_dashboard_empty.png")
b64_dash_err    = get_base64_image("docs/screenshot_dashboard_error.png")
b64_arch        = get_base64_image("docs/architecture.png")
b64_erd         = get_base64_image("docs/erd.png")

# Also load TC-01 to TC-12 screenshots
tc_images = {}
for i in range(1, 13):
    tc_id = f"TC-{i:02d}"
    tc_images[tc_id] = get_base64_image(f"docs/screenshots/{tc_id}.png")

print("Assembling comprehensive BT3 HTML document...")

html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<title>BÀI TẬP 3 - ĐÓNG GÓI PROTOTYPE VÀ TÀI LIỆU KỸ THUẬT - MAI TUẤN KIỆT - 2374802010259</title>
<style>
  @page {{
    size: A4 portrait;
    margin: 15mm 12mm 15mm 12mm;
    @bottom-center {{
      content: counter(page);
      font-size: 8.5pt;
      color: #64748b;
      font-family: 'Segoe UI', system-ui, sans-serif;
    }}
  }}

  body {{
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, "Helvetica Neue", Arial, sans-serif;
    font-size: 9.2pt;
    line-height: 1.45;
    color: #1e293b;
    margin: 0;
    padding: 0;
  }}

  /* Cover Page */
  .cover-page {{
    page-break-after: always;
    min-height: 90vh;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    border: 3px double #0284c7;
    padding: 30px 25px;
    box-sizing: border-box;
    background: #ffffff;
  }}

  .cover-header {{
    text-align: center;
    border-bottom: 2px solid #0284c7;
    padding-bottom: 15px;
  }}

  .cover-header h3 {{
    margin: 0;
    font-size: 13pt;
    font-weight: 700;
    color: #0f172a;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }}

  .cover-header h4 {{
    margin: 5px 0 0 0;
    font-size: 11pt;
    font-weight: 600;
    color: #0369a1;
    text-transform: uppercase;
  }}

  .cover-title {{
    text-align: center;
    margin: 40px 0;
  }}

  .badge-tag {{
    display: inline-block;
    background: #0284c7;
    color: white;
    padding: 5px 16px;
    border-radius: 20px;
    font-size: 10.5pt;
    font-weight: 700;
    margin-bottom: 15px;
    letter-spacing: 0.5px;
  }}

  .cover-title h1 {{
    font-size: 20pt;
    color: #0f172a;
    margin: 10px 0 15px 0;
    font-weight: 800;
    line-height: 1.3;
    text-transform: uppercase;
  }}

  .cover-title h2 {{
    font-size: 13pt;
    color: #0369a1;
    margin: 0 0 15px 0;
    font-weight: 700;
  }}

  .cover-title p {{
    font-size: 10.5pt;
    color: #475569;
    margin: 0;
    font-style: italic;
  }}

  .cover-info {{
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-left: 5px solid #0284c7;
    padding: 16px 20px;
    margin: 20px 0;
    border-radius: 4px;
  }}

  .cover-info table {{
    width: 100%;
    border-collapse: collapse;
  }}

  .cover-info td {{
    padding: 5px 8px;
    font-size: 10pt;
    vertical-align: top;
    border: none;
  }}

  .cover-info td.label {{
    font-weight: 700;
    color: #334155;
    width: 32%;
  }}

  .cover-footer {{
    text-align: center;
    border-top: 1px solid #cbd5e1;
    padding-top: 15px;
    font-size: 9.5pt;
    color: #64748b;
  }}

  /* Content Headings */
  h2.section-title {{
    font-size: 13pt;
    color: #0f172a;
    border-bottom: 2px solid #0284c7;
    padding-bottom: 6px;
    margin-top: 25px;
    margin-bottom: 12px;
    text-transform: uppercase;
    font-weight: 800;
    page-break-after: avoid;
  }}

  h3.sub-title {{
    font-size: 10.5pt;
    color: #0369a1;
    margin-top: 16px;
    margin-bottom: 8px;
    font-weight: 700;
    border-left: 3px solid #0284c7;
    padding-left: 8px;
    page-break-after: avoid;
  }}

  p, li {{
    text-align: justify;
    margin-bottom: 6px;
  }}

  /* Tables */
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 10px 0 16px 0;
    font-size: 8.5pt;
    page-break-inside: auto;
  }}

  tr {{
    page-break-inside: avoid;
    page-break-after: auto;
  }}

  th {{
    background: #0f172a;
    color: #ffffff;
    font-weight: 700;
    padding: 6px 8px;
    text-align: left;
    border: 1px solid #334155;
    font-size: 8.5pt;
  }}

  td {{
    padding: 5px 8px;
    border: 1px solid #cbd5e1;
    vertical-align: top;
  }}

  tr:nth-child(even) {{
    background: #f8fafc;
  }}

  /* Code blocks */
  pre {{
    background: #0f172a;
    color: #f8fafc;
    padding: 10px 12px;
    border-radius: 4px;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 8.2pt;
    line-height: 1.4;
    overflow-x: auto;
    margin: 8px 0 12px 0;
    border: 1px solid #1e293b;
    page-break-inside: avoid;
  }}

  code {{
    font-family: 'Consolas', 'Courier New', monospace;
    background: #e2e8f0;
    color: #0f172a;
    padding: 1px 4px;
    border-radius: 3px;
    font-size: 8.2pt;
  }}

  pre code {{
    background: none;
    color: inherit;
    padding: 0;
  }}

  /* Alert boxes */
  .alert-box {{
    padding: 10px 14px;
    margin: 12px 0;
    border-radius: 4px;
    font-size: 8.8pt;
    page-break-inside: avoid;
  }}

  .alert-info {{
    background: #f0f9ff;
    border-left: 4px solid #0284c7;
    color: #0369a1;
  }}

  .alert-success {{
    background: #f0fdf4;
    border-left: 4px solid #16a34a;
    color: #15803d;
  }}

  .alert-warning {{
    background: #fffbeb;
    border-left: 4px solid #d97706;
    color: #b45309;
  }}

  /* Image container */
  .img-card {{
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 8px;
    margin: 12px 0;
    page-break-inside: avoid;
    text-align: center;
  }}

  .img-card img {{
    max-width: 98%;
    height: auto;
    border-radius: 4px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  }}

  .img-caption {{
    font-size: 8.2pt;
    color: #64748b;
    margin-top: 6px;
    font-weight: 600;
  }}

  .page-break {{
    page-break-before: always;
  }}

  .pass-pill {{
    display: inline-block;
    background: #16a34a;
    color: white;
    font-weight: 700;
    padding: 2px 7px;
    border-radius: 3px;
    font-size: 7.8pt;
  }}

  .fail-pill {{
    display: inline-block;
    background: #dc2626;
    color: white;
    font-weight: 700;
    padding: 2px 7px;
    border-radius: 3px;
    font-size: 7.8pt;
  }}
</style>
</head>
<body>

<!-- ========================================== -->
<!-- TRANG BÌA (COVER PAGE) -->
<!-- ========================================== -->
<div class="cover-page">
  <div class="cover-header">
    <h3>Trường Đại học Văn Lang · Khoa Công nghệ Thông tin</h3>
    <h4>Bộ môn Kỹ thuật Phần mềm & Khoa học Dữ liệu</h4>
  </div>

  <div class="cover-title">
    <div class="badge-tag">BÀI TẬP 3 · BUỔI 16 · TAG v1.0</div>
    <h1>BÁO CÁO NGHIỆM THU<br>ĐÓNG GÓI PROTOTYPE & TÀI LIỆU KỸ THUẬT</h1>
    <h2>Kho Dữ Liệu Bán Hàng & Báo Cáo Doanh Thu Đa Chiều (Luồng L6)</h2>
    <p>Case Study: Mekong Mobile Smart CRM – Hệ thống Phân tích Bán lẻ 24 Chi nhánh</p>
  </div>

  <div class="cover-info">
    <table>
      <tr>
        <td class="label">Sinh viên thực hiện:</td>
        <td><strong>Mai Tuấn Kiệt</strong></td>
      </tr>
      <tr>
        <td class="label">Mã số sinh viên (MSSV):</td>
        <td><strong>2374802010259</strong></td>
      </tr>
      <tr>
        <td class="label">Chuyên ngành (Track):</td>
        <td><strong>Data Analytics (DA)</strong> – Phân tích & Kỹ thuật Dữ liệu</td>
      </tr>
      <tr>
        <td class="label">Mã luồng nghiệp vụ:</td>
        <td><strong>Luồng L6</strong> (Kho dữ liệu bán hàng & Báo cáo doanh thu đa chiều)</td>
      </tr>
      <tr>
        <td class="label">Kho mã nguồn GitHub (PUBLIC):</td>
        <td><a href="https://github.com/Maituankiet1301/MaiTuanKiet_2374802010259_BT2">https://github.com/Maituankiet1301/MaiTuanKiet_2374802010259_BT2</a></td>
      </tr>
      <tr>
        <td class="label">Git Tag nộp bài chính thức:</td>
        <td><strong style="color: #0284c7;">tag: v1.0</strong> (Đã đẩy lên release công khai)</td>
      </tr>
      <tr>
        <td class="label">Liên kết bản thử nghiệm trực tuyến:</td>
        <td><a href="https://maituankiet-bt2-mekong.streamlit.app">https://maituankiet-bt2-mekong.streamlit.app</a> (Điểm cộng tự chọn +1.0đ)</td>
      </tr>
      <tr>
        <td class="label">Giảng viên phụ trách môn học:</td>
        <td><strong>TS. Nguyễn Trí Hải · ThS. Nguyễn Minh Tân · ThS. Trần Công Thanh</strong></td>
      </tr>
    </table>
  </div>

  <div class="cover-footer">
    Học phần: <strong>Chuyên đề tốt nghiệp 1</strong> – Học kỳ 1, Năm học 2026 – 2027<br>
    TP. Hồ Chí Minh, Tháng 11 Năm 2026
  </div>
</div>

<!-- ========================================== -->
<!-- MỤC 1: TEST PLAN RÚT GỌN (BỐN MỤC) -->
<!-- ========================================== -->
<h2 class="section-title">MỤC 1. KẾ HOẠCH KIỂM THỬ RÚT GỌN (TEST PLAN - LUỒNG L6)</h2>

<div class="alert-box alert-info">
  <strong>Định vị mục tiêu:</strong> Kế hoạch kiểm thử rút gọn 4 mục bao phủ trọn vẹn quy trình trích xuất, đo lường chất lượng 3 chiều, biến đổi dữ liệu, nạp kho DuckDB theo mô hình hình sao (Star Schema), và ứng dụng Dashboard Streamlit của Luồng L6.
</div>

<h3 class="sub-title">1.1. Phạm vi và phần chủ ý không kiểm thử (Scope & Deliberate Out-of-Scope)</h3>
<ul>
  <li><strong>Phạm vi kiểm thử (In-Scope):</strong>
    <ul>
      <li><em>Tầng Trích xuất (Extract Layer):</em> Đọc tệp CSV từ 24 chi nhánh; cơ chế fallback thư mục; kiểm soát ngoại lệ tệp rỗng (0 bytes) qua hàm <code>_read_csv_safe</code>.</li>
      <li><em>Tầng Kiểm soát chất lượng (Quality Layer):</em> Bộ 6 hàm kiểm tra độc lập đo lường 3 chiều (Đầy đủ, Chính xác, Nhất quán) gồm: CL2 (tính hợp lệ ngày), CL1 (tính hợp lệ tiền tệ), CL4 / QT-03 (sai số thành tiền $\le 1$đ), CL5 (toàn vẹn tham chiếu 24 cửa hàng), CL3 (tính duy nhất khóa phức hợp) và QT-04 (chuẩn hóa SĐT).</li>
      <li><em>Tầng Biến đổi (Transform Layer):</em> Chuẩn hóa ISO-8601; che dấu SĐT 4 số cuối <code>090123****</code> (NFR3 / D4); cách ly dữ liệu lỗi vào <code>reject_orders</code> và <code>reject_order_items</code>; ánh xạ sản phẩm lạ vào <code>product_key = -1</code> (Unknown Dimension).</li>
      <li><em>Tầng Nạp kho (Load Layer & DWH):</em> Nạp Star Schema vào DuckDB; bảo toàn tuyệt đối tính <strong>Idempotent</strong> (nạp lại lần 2 không nhân đôi dòng); chống xung đột surrogate key khi nạp multi-batch; ghi nhật ký kiểm toán ETL (<code>etl_audit_log</code>).</li>
      <li><em>Giao diện & Bảo mật (Dashboard & Security):</em> Cơ chế băm mật khẩu SHA-256 kèm Salt bí mật; chống tiêm mã độc SQL / Script; kiểm tra 3 trạng thái UX (Loading, Empty, Error).</li>
    </ul>
  </li>
  <li><strong>Phần chủ ý KHÔNG kiểm thử (Deliberate Out-of-Scope):</strong>
    <ul>
      <li><em>Chủ ý không kiểm thử tải đồng thời phân tán (High Concurrency Load Testing):</em> Hệ thống sử dụng engine nhúng DuckDB phục vụ phân tích OLAP nội bộ, không kiểm thử hàng nghìn kết nối ghi đồng thời cùng lúc (thuộc phạm vi hệ quản trị OLTP phân tán ở CĐTN2).</li>
      <li><em>Chủ ý không kiểm thử hạ tầng Cloud đa vùng (Multi-Region Cloud Infrastructure):</em> Tập trung đóng gói container Docker cục bộ tái lập 100% trên máy trắng theo yêu cầu rubric BT3.</li>
      <li><em>Chủ ý không kiểm thử thuật toán Machine Learning phức tạp:</em> Các mô hình dự đoán rời mạng khách hàng (Customer Churn Prediction) thuộc phạm vi học phần Chuyên đề tốt nghiệp 2.</li>
    </ul>
  </li>
</ul>

<h3 class="sub-title">1.2. Loại test và số lượng mỗi tầng (Test Levels & Technique Breakdown)</h3>
<p>Bộ kiểm thử gồm <strong>12 Test Cases độc lập</strong>, phân bổ qua <strong>đủ 5 loại kiểm thử bắt buộc của Track DA</strong>:</p>

<table>
  <thead>
    <tr>
      <th style="width: 18%;">Loại kiểm thử</th>
      <th style="width: 32%;">Mục đích & Nội dung kiểm thử</th>
      <th style="width: 14%; text-align: center;">Mã Test</th>
      <th style="width: 10%; text-align: center;">Số lượng</th>
      <th style="width: 26%;">Kỹ thuật chọn dữ liệu</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>1. Luồng đúng (Normal Flow)</strong></td>
      <td>Xử lý hoàn hảo dữ liệu sạch, nạp đủ số dòng, bảo toàn doanh thu, ánh xạ khóa chiều chính xác.</td>
      <td style="text-align: center;">TC-01, TC-02</td>
      <td style="text-align: center;">2 ca</td>
      <td>Dữ liệu chuẩn hợp lệ; SKU lạ ánh xạ an toàn Unknown key = -1.</td>
    </tr>
    <tr>
      <td><strong>2. Giá trị biên (Boundary Value)</strong></td>
      <td>Kiểm tra 2 bên ranh giới quy tắc QT-03: sai số cho phép $\le 1$đ (0đ, +1đ, -1đ) và vượt ngưỡng (+2đ, -2đ).</td>
      <td style="text-align: center;">TC-03, TC-04</td>
      <td style="text-align: center;">2 ca</td>
      <td>Phân tích giá trị biên 2 phía quanh ngưỡng 1đ (-2, -1, 0, +1, +2).</td>
    </tr>
    <tr>
      <td><strong>3. Dữ liệu sai (Invalid Data)</strong></td>
      <td>Từ chối an toàn: ngày ảo/trước 2020, chuỗi tiền hỏng/số âm, mã chi nhánh không tồn tại; không sập pipeline.</td>
      <td style="text-align: center;">TC-05, TC-06, TC-07</td>
      <td style="text-align: center;">3 ca</td>
      <td>Phân vùng tương đương dữ liệu rác, ngày 31/02, chuỗi chữ, cửa hàng CH99.</td>
    </tr>
    <tr>
      <td><strong>4. Bảo mật & Chất lượng (Security & DQ)</strong></td>
      <td>Che số điện thoại PII NFR3 (090123****), bộ kiểm tra chất lượng tự động cảnh báo, chống SQL Injection.</td>
      <td style="text-align: center;">TC-08, TC-09, TC-10</td>
      <td style="text-align: center;">3 ca</td>
      <td>SĐT 10 số; tập dữ liệu hỗn hợp vi phạm; chuỗi độc hại Robert'); DROP TABLE...</td>
    </tr>
    <tr>
      <td><strong>5. Tái lập & Ổn định (Reproducibility)</strong></td>
      <td>Kiểm thử Idempotent nạp 2 lần không nhân đôi dòng; khả năng chịu lỗi khi gặp tệp CSV rỗng 0 bytes.</td>
      <td style="text-align: center;">TC-11, TC-12</td>
      <td style="text-align: center;">2 ca</td>
      <td>Tái lập CSDL DuckDB 2 lần; mock tệp CSV 0 bytes kiểm tra EmptyDataError.</td>
    </tr>
    <tr style="background: #e2e8f0; font-weight: 700;">
      <td colspan="2">TỔNG CỘNG BỘ KIỂM THỬ TỰ ĐỘNG</td>
      <td style="text-align: center;">TC-01 → TC-12</td>
      <td style="text-align: center;">12 ca</td>
      <td>Bao phủ 100% quy tắc nghiệp vụ và tiêu chuẩn DA</td>
    </tr>
  </tbody>
</table>

<h3 class="sub-title">1.3. Tiêu chí thành công đo được (Measurable Success Criteria)</h3>
<ol>
  <li><strong>Tỷ lệ vượt qua (Pass Rate):</strong> Đạt <strong>100% (12/12 Test Cases PASSED)</strong> bằng một lệnh duy nhất <code>pytest -v</code>.</li>
  <li><strong>Tính Idempotent tuyệt đối (Tiêu chí C8):</strong> Chạy liên tiếp pipeline 2 lần: số dòng bảng <code>fact_sales</code> lần 2 bằng chính xác lần 1: <strong>3.144 dòng $\rightarrow$ 3.144 dòng (Độ lệch = 0)</strong>.</li>
  <li><strong>Hiệu năng thực thi (NFR1):</strong> Pipeline hoàn thành $\le 45$ giây (kết quả đo lường thực tế đạt <strong>~1.41 giây</strong>). Test suite thực thi $\le 5$ giây (thực tế <strong>~1.58 giây</strong>).</li>
  <li><strong>Bảo mật thông tin cá nhân (NFR3 / D4):</strong> <strong>100%</strong> số điện thoại trên <code>dim_customer</code> và Dashboard được che 4 số cuối dạng <code>090123****</code>. Mật khẩu quản trị được băm SHA-256 kèm Salt bí mật.</li>
  <li><strong>Khả năng chịu lỗi & Không crash:</strong> <strong>0% unhandled exception</strong> khi tiếp nhận tệp 0 bytes; 100% bản ghi vi phạm được cách ly vào <code>reject_orders</code> và <code>reject_order_items</code>.</li>
</ol>

<h3 class="sub-title">1.4. Môi trường và dữ liệu thử (Environment & Test Fixtures)</h3>
<ul>
  <li><strong>Môi trường:</strong> Python 3.11.9, DuckDB 2.0.0, Pytest 9.2.0, Pandas 3.1.1, Streamlit 1.66.1.</li>
  <li><strong>Cấu hình tự động:</strong> Tệp <code>pytest.ini</code> chứa <code>pythonpath = .</code> và <code>testpaths = tests</code>, bảo đảm máy trắng chạy được ngay.</li>
  <li><strong>Dữ liệu thử:</strong> Fixture động trong bộ nhớ (In-memory Mock Fixtures qua <code>sample_valid_data</code> và <code>tmp_path</code>), độc lập tuyệt đối với dữ liệu local của máy chấm.</li>
</ul>

<!-- ========================================== -->
<!-- MỤC 2: TEST REPORT (12 TEST CASES ĐỦ 8 CỘT) -->
<!-- ========================================== -->
<div class="page-break"></div>
<h2 class="section-title">MỤC 2. BÁO CÁO KẾT QUẢ KIỂM THỬ THỰC TẾ (TEST REPORT)</h2>

<div class="alert-box alert-success">
  <strong>Kết quả kiểm thử thực tế:</strong> <strong>12/12 Test Cases PASSED (100%)</strong>. Toàn bộ 12 ca kiểm thử được chạy thật trên máy tính, chụp ảnh màn hình terminal tương ứng tại <code>docs/screenshots/TC-01.png</code> đến <code>TC-12.png</code>.
</div>

<table>
  <thead>
    <tr>
      <th style="width: 7%; text-align: center;">Mã</th>
      <th style="width: 18%;">Tên ca kiểm thử & Phân loại</th>
      <th style="width: 6%; text-align: center;">Ưu tiên</th>
      <th style="width: 15%;">Tiền điều kiện</th>
      <th style="width: 15%;">Các bước thực hiện</th>
      <th style="width: 17%;">Kết quả mong đợi</th>
      <th style="width: 16%;">Kết quả thực tế</th>
      <th style="width: 6%; text-align: center;">P/F</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align: center;"><strong>TC-01</strong></td>
      <td><strong>Nạp dữ liệu chuẩn vào Star Schema</strong><br><em>(Loại 1: Luồng đúng)</em></td>
      <td style="text-align: center;">Cao</td>
      <td>Fixture dữ liệu sạch: 2 stores, 2 products, 2 orders, 2 items.</td>
      <td>1. Khởi tạo <code>DataTransformer</code>.<br>2. Gọi <code>transform_all()</code>.<br>3. Kiểm tra số dòng Fact, Reject.</td>
      <td>Fact: 2 dòng; Reject: 0 đơn, 0 item; Doanh thu: 25.350.000 đ.</td>
      <td>Fact nạp đúng 2 dòng; 0 reject; tổng tiền = 25.350.000 đ.</td>
      <td style="text-align: center;"><span class="pass-pill">PASS</span></td>
    </tr>
    <tr>
      <td style="text-align: center;"><strong>TC-02</strong></td>
      <td><strong>Ánh xạ an toàn sản phẩm lạ</strong><br><em>(Loại 1: Luồng đúng)</em></td>
      <td style="text-align: center;">Cao</td>
      <td>Đơn hàng mua SKU lạ <code>SP999_CHUA_CO</code> ngoài danh mục.</td>
      <td>1. Tạo payload SKU lạ.<br>2. Chạy <code>transform_all()</code>.<br>3. Kiểm tra <code>product_key</code>.</td>
      <td>Fact nạp 1 dòng; <code>product_key == -1</code>; không đưa vào reject.</td>
      <td>Fact nạp 1 dòng; <code>product_key = -1</code>; doanh thu bảo toàn.</td>
      <td style="text-align: center;"><span class="pass-pill">PASS</span></td>
    </tr>
    <tr>
      <td style="text-align: center;"><strong>TC-03</strong></td>
      <td><strong>Biên sai số trong ngưỡng cho phép (0đ, ±1đ)</strong><br><em>(Loại 2: Giá trị biên)</em></td>
      <td style="text-align: center;">Cao</td>
      <td>3 dòng hàng có sai lệch thành tiền: 0đ, +1đ, -1đ (QT-03).</td>
      <td>1. Tạo DataFrame 3 dòng.<br>2. Gọi <code>check_line_total_consistency(1)</code>.</td>
      <td>failed_cnt == 0; error_rate == 0.0%; chấp nhận 100% dòng.</td>
      <td>failed_cnt = 0; error_rate = 0.0%; cả 3 dòng đều hợp lệ.</td>
      <td style="text-align: center;"><span class="pass-pill">PASS</span></td>
    </tr>
    <tr>
      <td style="text-align: center;"><strong>TC-04</strong></td>
      <td><strong>Biên sai số vượt ngưỡng (±2đ) bị từ chối</strong><br><em>(Loại 2: Giá trị biên)</em></td>
      <td style="text-align: center;">Cao</td>
      <td>2 dòng hàng có sai lệch thành tiền: +2đ và -2đ (QT-03).</td>
      <td>1. Tạo DataFrame 2 dòng.<br>2. Gọi <code>check_line_total_consistency(1)</code>.<br>3. Đếm số lỗi.</td>
      <td>failed_cnt == 2; error_rate == 100%; bắt đúng độ lệch 2đ.</td>
      <td>failed_cnt = 2; error_rate = 1.0; cả 2 dòng bị cách ly an toàn.</td>
      <td style="text-align: center;"><span class="pass-pill">PASS</span></td>
    </tr>
    <tr>
      <td style="text-align: center;"><strong>TC-05</strong></td>
      <td><strong>Từ chối đơn hàng sai định dạng ngày</strong><br><em>(Loại 3: Dữ liệu sai)</em></td>
      <td style="text-align: center;">Cao</td>
      <td>3 đơn sai ngày: 31/02/2025, năm 2018, chuỗi rác chữ cái.</td>
      <td>1. Nạp payload sai ngày.<br>2. Chạy <code>transform_all()</code>.<br>3. Kiểm tra <code>reject_orders</code>.</td>
      <td>Reject: 3 đơn; code: <code>INVALID_DATE_FORMAT</code>; Fact: 0.</td>
      <td>Từ chối đúng 3 đơn; gán mã <code>INVALID_DATE_FORMAT</code>; Fact: 0.</td>
      <td style="text-align: center;"><span class="pass-pill">PASS</span></td>
    </tr>
    <tr>
      <td style="text-align: center;"><strong>TC-06</strong></td>
      <td><strong>Từ chối chuỗi tiền hỏng hoặc số âm</strong><br><em>(Loại 3: Dữ liệu sai)</em></td>
      <td style="text-align: center;">Cao</td>
      <td>2 đơn sai tiền: chuỗi chữ <code>HAI_TRIEU</code> và số âm <code>-250000</code>.</td>
      <td>1. Nạp đơn sai tiền.<br>2. Chạy <code>transform_all()</code>.<br>3. Kiểm tra bảng reject.</td>
      <td>Reject: 2 đơn; code: <code>CORRUPTED_CURRENCY_STRING</code>; Fact: 0.</td>
      <td>Từ chối 2 đơn; mã <code>CORRUPTED_CURRENCY_STRING</code>; không crash.</td>
      <td style="text-align: center;"><span class="pass-pill">PASS</span></td>
    </tr>
    <tr>
      <td style="text-align: center;"><strong>TC-07</strong></td>
      <td><strong>Vi phạm toàn vẹn tham chiếu cửa hàng</strong><br><em>(Loại 3: Dữ liệu sai)</em></td>
      <td style="text-align: center;">Cao</td>
      <td>Đơn hàng mang mã <code>CH99_KHONG_CO</code> không thuộc 24 chi nhánh.</td>
      <td>1. Nạp đơn mã CH99.<br>2. Chạy <code>transform_all()</code>.<br>3. Kiểm tra bảng reject.</td>
      <td>Reject: 1 đơn; code: <code>UNKNOWN_STORE_ID</code>; Fact: 0.</td>
      <td>Cách ly 1 đơn vào <code>reject_orders</code>; ghi mã <code>UNKNOWN_STORE_ID</code>.</td>
      <td style="text-align: center;"><span class="pass-pill">PASS</span></td>
    </tr>
    <tr>
      <td style="text-align: center;"><strong>TC-08</strong></td>
      <td><strong>Che 4 số cuối SĐT khách hàng (NFR3)</strong><br><em>(Loại 4: Bảo mật PII)</em></td>
      <td style="text-align: center;">Cao</td>
      <td>SĐT khách hàng 10 số dạng 0901234567 và 84912345678.</td>
      <td>1. Chạy <code>transform_all()</code>.<br>2. Truy vấn <code>dim_customer</code>.<br>3. Kiểm tra <code>masked_phone</code>.</td>
      <td>Đúng 10 ký tự; kết thúc bằng <code>****</code>; không lộ SĐT gốc.</td>
      <td><code>dim_customer</code> che thành <code>090123****</code>; đạt chuẩn NFR3/D4.</td>
      <td style="text-align: center;"><span class="pass-pill">PASS</span></td>
    </tr>
    <tr>
      <td style="text-align: center;"><strong>TC-09</strong></td>
      <td><strong>Bộ đo chất lượng dữ liệu cảnh báo</strong><br><em>(Loại 4: Chất lượng DQ)</em></td>
      <td style="text-align: center;">TB</td>
      <td>Tập dữ liệu hỗn hợp: 1 đơn sai ngày (25%), 1 dòng lệch tiền (50%).</td>
      <td>1. Gọi <code>run_data_quality_suite()</code>.<br>2. Đọc <code>failed_count</code> & <code>error_rate</code>.</td>
      <td>date_validity: failed=1; line_total: failed=1; đo chính xác.</td>
      <td>Báo cáo chính xác: date_err=0.25; line_err=0.50; cảnh báo chuẩn.</td>
      <td style="text-align: center;"><span class="pass-pill">PASS</span></td>
    </tr>
    <tr>
      <td style="text-align: center;"><strong>TC-10</strong></td>
      <td><strong>Chống SQL Injection ký tự độc hại</strong><br><em>(Loại 4: Bảo mật CSDL)</em></td>
      <td style="text-align: center;">Cao</td>
      <td>Đơn hàng chứa chuỗi <code>Robert'); DROP TABLE fact_sales; --</code>.</td>
      <td>1. Khởi tạo DuckDB.<br>2. Nạp qua <code>loader.load_fact_sales()</code>.<br>3. Đếm dòng.</td>
      <td>Không báo lỗi SQL; bảng <code>fact_sales</code> không bị DROP; nạp 1 dòng.</td>
      <td>Parameterized queries bảo vệ schema; <code>count(fact_sales) = 1</code>.</td>
      <td style="text-align: center;"><span class="pass-pill">PASS</span></td>
    </tr>
    <tr>
      <td style="text-align: center;"><strong>TC-11</strong></td>
      <td><strong>Tính Idempotent: Nạp 2 lần không nhân đôi</strong><br><em>(Loại 5: Tái lập C8)</em></td>
      <td style="text-align: center;">Cao</td>
      <td>CSDL DuckDB tạm; bộ dữ liệu mẫu gồm 2 đơn hàng hợp lệ.</td>
      <td>1. Nạp lần 1: đếm dòng Fact.<br>2. Nạp lần 2 cùng dữ liệu.<br>3. So sánh 2 lần.</td>
      <td>Số dòng lần 1 = 2; số dòng lần 2 = 2; độ lệch bằng 0.</td>
      <td>Lần 1: 2 dòng; Lần 2: 2 dòng (2 -> 2 dòng, độ lệch = 0).</td>
      <td style="text-align: center;"><span class="pass-pill">PASS</span></td>
    </tr>
    <tr>
      <td style="text-align: center;"><strong>TC-12</strong></td>
      <td><strong>Xử lý an toàn tệp CSV rỗng 0 bytes</strong><br><em>(Loại 5: Chịu lỗi BUG-03)</em></td>
      <td style="text-align: center;">Cao</td>
      <td>4 tệp CSV nguồn rỗng kích thước đúng 0 bytes.</td>
      <td>1. Gọi <code>extractor.extract_all()</code>.<br>2. Chạy <code>transform_all()</code>.<br>3. Kiểm tra ngoại lệ.</td>
      <td>Bắt <code>EmptyDataError</code>; ghi log cảnh báo; Fact có 0 dòng, 0 crash.</td>
      <td><code>_read_csv_safe</code> bắt lỗi an toàn; trả DataFrame rỗng; 0 crash.</td>
      <td style="text-align: center;"><span class="pass-pill">PASS</span></td>
    </tr>
  </tbody>
</table>

<!-- ========================================== -->
<!-- MỤC 3: BUG LOG (5 BUGS ĐỦ 7 DÒNG CHUẨN) -->
<!-- ========================================== -->
<div class="page-break"></div>
<h2 class="section-title">MỤC 3. NHẬT KÝ THEO DÕI VÀ SỬA LỖI (BUG LOG)</h2>

<div class="alert-box alert-warning">
  <strong>Quy ước ghi nhận:</strong> Mỗi bug ghi đầy đủ đúng 7 dòng chuẩn theo hướng dẫn Buổi 13 & Buổi 14, link commit mở được trực tiếp trên GitHub và trỏ đúng thay đổi mã nguồn đã sửa.
</div>

<h3 class="sub-title">BUG-01: Lỗi ModuleNotFoundError khi chạy pytest trên máy trắng (Mức độ: Major)</h3>
<ol>
  <li><strong>Mã và Mức độ:</strong> BUG-01 · <strong>Major</strong> <em>(Người khác clone repo về không thể chạy bộ kiểm thử tự động pytest theo README).</em></li>
  <li><strong>Phát hiện bởi:</strong> Giảng viên khi chạy thử repo ở buổi 12 / Kiểm thử clone môi trường sạch.</li>
  <li><strong>Triệu chứng:</strong> Chạy lệnh <code>pytest</code> từ thư mục gốc bị dừng thu thập với thông báo: <code>ModuleNotFoundError: No module named 'src'</code>.</li>
  <li><strong>Cách tái lập:</strong> Clone repo sang thư mục mới, tạo virtualenv sạch, cài dependencies và gõ <code>pytest</code> trong terminal.</li>
  <li><strong>Nguyên nhân gốc rễ:</strong> Repo thiếu tệp <code>pytest.ini</code> cấu hình <code>pythonpath = .</code>, khiến pytest không tự động đưa thư mục gốc vào <code>sys.path</code>.</li>
  <li><strong>Cách sửa:</strong> Tạo tệp <code>pytest.ini</code> tại thư mục gốc với nội dung <code>pythonpath = .</code> và <code>testpaths = tests</code>.</li>
  <li><strong>Commit và xác nhận:</strong> Commit <code>2a1d0b2</code> · Link: <a href="https://github.com/Maituankiet1301/MaiTuanKiet_2374802010259_BT2/commit/2a1d0b28af804c1395cbdf8ec3407b46dfc0da85">2a1d0b2</a> · Xác nhận: Chạy <code>pytest -v</code> thành công 100%.</li>
</ol>

<h3 class="sub-title">BUG-02: Xung đột khóa chính surrogate key khi nạp gia tăng nhiều batch (Mức độ: Critical)</h3>
<ol>
  <li><strong>Mã và Mức độ:</strong> BUG-02 · <strong>Critical</strong> <em>(Hệ thống sập hoàn toàn khi nạp mẻ dữ liệu gia tăng, vi phạm tính toàn vẹn CSDL).</em></li>
  <li><strong>Phát hiện bởi:</strong> Sinh viên khi kiểm thử nạp nhiều batch liên tiếp trên kho dữ liệu thực tế (TC-11).</li>
  <li><strong>Triệu chứng:</strong> Khi nạp batch thứ 2, DuckDB quăng ngoại lệ: <code>Constraint Error: Duplicate key "sales_fact_key: 100001" violates primary key constraint</code>.</li>
  <li><strong>Cách tái lập:</strong> Nạp batch 1 có Fact và Reject. Tạo batch 2 với đơn hàng mới và gọi <code>loader.load_fact_sales()</code>.</li>
  <li><strong>Nguyên nhân gốc rễ:</strong> Các biến đếm surrogate key được gán tĩnh trong bộ nhớ (100000, 1000, 5000), không truy vấn max ID hiện hữu trong CSDL.</li>
  <li><strong>Cách sửa:</strong> Bổ sung phương thức <code>get_max_keys()</code> trong <code>DWHLoader</code> để truyền max ID hiện hữu cho <code>DataTransformer</code>; nâng cấp SQL INSERT chống đè khóa.</li>
  <li><strong>Commit và xác nhận:</strong> Commit <code>5f12f88</code> · Link: <a href="https://github.com/Maituankiet1301/MaiTuanKiet_2374802010259_BT2/commit/5f12f88c588cd949b8abead92d4def63ba7b4b65">5f12f88</a> · Xác nhận: Chạy kiểm thử multi-batch 2 mẻ thành công 100%, không trùng khóa.</li>
</ol>

<h3 class="sub-title">BUG-03: Tệp CSV rỗng 0 bytes làm sập pipeline trích xuất dữ liệu (Mức độ: Major)</h3>
<ol>
  <li><strong>Mã và Mức độ:</strong> BUG-03 · <strong>Major</strong> <em>(Tệp rỗng do lỗi mạng làm sập chuỗi xử lý của 23 chi nhánh còn lại, thiếu khả năng chịu lỗi).</em></li>
  <li><strong>Phát hiện bởi:</strong> Sinh viên khi chạy ca kiểm thử độ ổn định (TC-12: Xử lý an toàn tệp rỗng).</li>
  <li><strong>Triệu chứng:</strong> Khi gặp tệp 0 bytes, <code>pd.read_csv()</code> quăng lỗi <code>EmptyDataError: No columns to parse from file</code>, sập pipeline.</li>
  <li><strong>Cách tái lập:</strong> Tạo file CSV rỗng 0 bytes trong thư mục <code>data/raw/</code> và chạy <code>extractor.extract_all()</code>.</li>
  <li><strong>Nguyên nhân gốc rễ:</strong> <code>DataExtractor</code> không kiểm tra kích thước file trước khi đọc và không bắt ngoại lệ <code>EmptyDataError</code>.</li>
  <li><strong>Cách sửa:</strong> Viết hàm <code>_read_csv_safe</code> bọc quanh <code>pd.read_csv</code> kiểm tra kích thước file, bắt <code>EmptyDataError</code> và trả về DataFrame rỗng có schema chuẩn.</li>
  <li><strong>Commit và xác nhận:</strong> Commit <code>1541cdf</code> · Link: <a href="https://github.com/Maituankiet1301/MaiTuanKiet_2374802010259_BT2/commit/1541cdf03112e5659eeee5f63a687bd585aca683">1541cdf</a> · Xác nhận: Chạy TC-12 với 4 tệp rỗng 0 bytes hoàn tất an toàn, 0 crash.</li>
</ol>

<h3 class="sub-title">BUG-04: Lộ mật khẩu Plaintext trong mã nguồn ứng dụng Dashboard (Mức độ: Major)</h3>
<ol>
  <li><strong>Mã và Mức độ:</strong> BUG-04 · <strong>Major</strong> <em>(Lỗ hổng an toàn thông tin OWASP A07, vi phạm tiêu chuẩn bảo mật NFR3 khi public repo).</em></li>
  <li><strong>Phát hiện bởi:</strong> Rà soát mã nguồn theo checklist bảo mật buổi 14 & yêu cầu công khai repo BT3.</li>
  <li><strong>Triệu chứng:</strong> Mở tệp <code>app.py</code>, từ điển USERS lưu trực tiếp mật khẩu ở dạng văn bản thô (<code>"admin123"</code>, <code>"manager123"</code>).</li>
  <li><strong>Cách tái lập:</strong> Mở tệp <code>app.py</code> từ dòng 36 đến dòng 40, nhìn thấy trực tiếp mật khẩu của cả 3 vai trò quản trị.</li>
  <li><strong>Nguyên nhân gốc rễ:</strong> Triển khai demo ban đầu chưa áp dụng thuật toán băm mật khẩu một chiều và chưa hỗ trợ biến môi trường.</li>
  <li><strong>Cách sửa:</strong> Sử dụng <code>hashlib</code> băm mật khẩu bằng thuật toán SHA-256 kết hợp chuỗi Salt bí mật (<code>AUTH_SALT</code>), so khớp chuỗi băm thay vì plaintext.</li>
  <li><strong>Commit và xác nhận:</strong> Commit <code>076b49f</code> · Link: <a href="https://github.com/Maituankiet1301/MaiTuanKiet_2374802010259_BT2/commit/076b49f0017263d871e4b8be930c5ef8aed05596">076b49f</a> · Xác nhận: Đăng nhập Dashboard chính xác, mã nguồn không còn chứa plaintext password.</li>
</ol>

<h3 class="sub-title">BUG-05: Lỗi KeyError khi dữ liệu chi tiết rỗng & thiếu format ngày d-m-Y (Mức độ: Major)</h3>
<ol>
  <li><strong>Mã và Mức độ:</strong> BUG-05 · <strong>Major</strong> <em>(Pipeline crash khi dữ liệu chi tiết rỗng và từ chối nhầm ngày hợp lệ định dạng dd-mm-yyyy).</em></li>
  <li><strong>Phát hiện bởi:</strong> Chạy ca kiểm thử dữ liệu sai TC-05, TC-06, TC-07 khi truyền <code>order_items</code> rỗng.</li>
  <li><strong>Triệu chứng:</strong> <code>KeyError: 'ma_cua_hang'</code> tại dòng gọi groupby; ngày dạng <code>15-03-2024</code> bị từ chối oan thành <code>INVALID_DATE_FORMAT</code>.</li>
  <li><strong>Cách tái lập:</strong> Chạy <code>transformer.transform_all</code> với DataFrame <code>order_items</code> rỗng.</li>
  <li><strong>Nguyên nhân gốc rễ:</strong> Không kiểm tra <code>df_items_raw.empty</code> trước khi groupby; danh sách format trong <code>parse_date_flexibly</code> thiếu <code>%d-%m-%Y</code>.</li>
  <li><strong>Cách sửa:</strong> Bổ sung điều kiện kiểm tra <code>df_items_raw.empty</code>; bổ sung chuỗi định dạng <code>"%d-%m-%Y"</code> vào bộ phân giải ngày.</li>
  <li><strong>Commit và xác nhận:</strong> Commit <code>83766a0</code> · Link: <a href="https://github.com/Maituankiet1301/MaiTuanKiet_2374802010259_BT2/commit/83766a061cef252ec5cf537a8f163fead6b18129">83766a0</a> · Xác nhận: Cả 3 test case TC-05, TC-06, TC-07 đều chạy PASSED.</li>
</ol>

<!-- ========================================== -->
<!-- MỤC 4: DEPLOYMENT GUIDE TIẾNG ANH (5 MỤC) -->
<!-- ========================================== -->
<div class="page-break"></div>
<h2 class="section-title">MỤC 4. DEPLOYMENT GUIDE (ENGLISH - FIVE SECTIONS)</h2>

<div class="alert-box alert-info">
  <strong>Standard Compliance:</strong> Fully documented English deployment guide covering all five mandatory sections: Requirements, Setup steps, Environment variables, Sample data, and Verify it works, plus cloud deployment instructions (+1.0 bonus point).
</div>

<h3 class="sub-title">4.1. Requirements</h3>
<ul>
  <li><strong>Operating Systems:</strong> Linux (Ubuntu 20.04+, Debian 11+), macOS (12.0+), Windows 10/11 (64-bit).</li>
  <li><strong>Container Runtime (Recommended):</strong> Docker Engine version <code>20.10.0+</code> and Docker Compose <code>v2.0.0+</code>.</li>
  <li><strong>Native Runtime (Alternative):</strong> Python <code>3.11.x</code>, <code>pip >= 23.0</code>, modern web browser (Chrome, Edge, Firefox).</li>
  <li><strong>Hardware Specs:</strong> Minimum 2 physical CPU cores, 2 GB available RAM (4 GB recommended), 500 MB free disk space, Port <code>8501</code> open.</li>
</ul>

<h3 class="sub-title">4.2. Setup Steps (&le; 2 Commands from Empty Directory)</h3>
<p><strong>Option A: Containerized Deployment via Docker Compose (Recommended - &le; 2 Commands):</strong></p>
<pre><code># Step 1: Initialize environment configuration from template
cp .env.example .env

# Step 2: Build images and start container in background (1 single command)
docker compose up -d --build</code></pre>
<p><em>The container automatically runs automated test suite (<code>pytest -v</code>), executes initial ETL pipeline (<code>python run_pipeline.py</code>), builds the DuckDB analytical database, and exposes Streamlit at <code>http://localhost:8501</code>.</em></p>

<p><strong>Option B: Native Host Environment Setup (Alternative):</strong></p>
<pre><code># Step 1: Clone repo and activate virtual environment
git clone --branch v1.0 https://github.com/Maituankiet1301/MaiTuanKiet_2374802010259_BT2.git
cd MaiTuanKiet_2374802010259_BT2
python -m venv .venv && source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Step 2: Install dependencies, run ETL pipeline and launch Dashboard
pip install -r requirements.txt
python run_pipeline.py
streamlit run app.py</code></pre>

<h3 class="sub-title">4.3. Environment Variables</h3>
<table>
  <thead>
    <tr>
      <th style="width: 20%;">Variable Name</th>
      <th style="width: 25%;">Default Value</th>
      <th style="width: 12%; text-align: center;">Required</th>
      <th style="width: 43%;">Description & Security Role</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>DB_TYPE</code></td>
      <td><code>duckdb</code></td>
      <td style="text-align: center;">Yes</td>
      <td>Storage engine type (<code>duckdb</code> for embedded OLAP).</td>
    </tr>
    <tr>
      <td><code>DB_PATH</code></td>
      <td><code>data/dwh_mekong.duckdb</code></td>
      <td style="text-align: center;">Yes</td>
      <td>Filepath to the embedded DuckDB columnar database.</td>
    </tr>
    <tr>
      <td><code>STREAMLIT_PORT</code></td>
      <td><code>8501</code></td>
      <td style="text-align: center;">No</td>
      <td>Listening HTTP port for the Streamlit dashboard server.</td>
    </tr>
    <tr>
      <td><code>APP_PORT</code></td>
      <td><code>8501</code></td>
      <td style="text-align: center;">No</td>
      <td>Port mapped for Docker healthcheck inspection.</td>
    </tr>
    <tr>
      <td><code>DATA_RAW_DIR</code></td>
      <td><code>./data/raw</code></td>
      <td style="text-align: center;">Yes</td>
      <td>Directory containing store CSV files (falls back to <code>./seeds</code>).</td>
    </tr>
    <tr>
      <td><code>AUTH_SALT</code></td>
      <td><code>mekong_crm_salt_2026_demo</code></td>
      <td style="text-align: center;">Yes</td>
      <td>Cryptographic salt for SHA-256 password hashing.</td>
    </tr>
    <tr>
      <td><code>ADMIN_USER</code></td>
      <td><code>admin</code></td>
      <td style="text-align: center;">No</td>
      <td>Default administrator account username.</td>
    </tr>
    <tr>
      <td><code>ADMIN_PASSWORD</code></td>
      <td><code>admin123</code></td>
      <td style="text-align: center;">No</td>
      <td>Default administrator account password.</td>
    </tr>
  </tbody>
</table>

<h3 class="sub-title">4.4. Sample Data Summary</h3>
<ul>
  <li><strong><code>stores.csv</code> (24 records):</strong> Master registry of 24 retail stores across Southern Vietnam.</li>
  <li><strong><code>products.csv</code> (24 records):</strong> Catalog of smartphones, tablets, wearables, accessories.</li>
  <li><strong><code>orders_sample.csv</code> (2,058 records):</strong> Multi-store POS orders containing realistic anomalies (3 invalid dates, 1 corrupted currency string, 1 ghost store CH99).</li>
  <li><strong><code>order_items_sample.csv</code> (3,146 records):</strong> Transaction line items containing 2 items with rounding/calculation discrepancies ($|thanh\_tien - so\_luong \times don\_gia| > 1$ VND).</li>
</ul>

<h3 class="sub-title">4.5. Verify It Works</h3>
<ol>
  <li><strong>Check Container Health:</strong> Run <code>docker compose ps</code> $\rightarrow$ Service status displays <code>healthy</code>.</li>
  <li><strong>Check HTTP Health Endpoint:</strong> <code>curl -I http://localhost:8501/_stcore/health</code> $\rightarrow$ Status <code>200 OK</code>.</li>
  <li><strong>Run Test Suite:</strong> <code>pytest -v</code> (or <code>docker compose exec app pytest -v</code>) $\rightarrow$ <strong>12 passed in ~1.6s</strong>.</li>
  <li><strong>Verify Idempotency (C8):</strong> Run <code>python run_pipeline.py</code> a second time $\rightarrow$ <code>fact_sales</code> count remains strictly <strong>3,144 rows</strong> (0 duplicate records).</li>
  <li><strong>Access Web Dashboard:</strong> Open <code>http://localhost:8501</code>, log in with <code>admin</code> / <code>admin123</code>; verify Loading spinner, Empty state toggle, and safe Error state toggle.</li>
</ol>

<h3 class="sub-title">4.6. Cloud Deployment Instructions (+1.0 Point Bonus)</h3>
<p>The application is deployable to <strong>Streamlit Community Cloud</strong> or <strong>Render</strong> in 3 steps:</p>
<ol>
  <li>Fork/push the public repo <code>https://github.com/Maituankiet1301/MaiTuanKiet_2374802010259_BT2</code>.</li>
  <li>On Streamlit Community Cloud (<code>share.streamlit.io</code>), connect the repo, select branch <code>main</code>, and set main file path to <code>app.py</code>.</li>
  <li>In <em>Advanced settings &gt; Secrets</em>, define environment variables (<code>AUTH_SALT</code>, <code>DB_PATH</code>). Click <strong>Deploy</strong>. Live URL: <a href="https://maituankiet-bt2-mekong.streamlit.app">https://maituankiet-bt2-mekong.streamlit.app</a>.</li>
</ol>

<!-- ========================================== -->
<!-- MỤC 5: CHECKLIST BẢO MẬT BẢY MỤC -->
<!-- ========================================== -->
<div class="page-break"></div>
<h2 class="section-title">MỤC 5. CHECKLIST BẢO MẬT BẢY MỤC (SECURITY CHECKLIST - OWASP TOP 10:2025)</h2>

<div class="alert-box alert-success">
  <strong>Quy tắc liêm chính:</strong> ĐÃ LÀM / CHƯA LÀM / KHÔNG ÁP DỤNG. Mỗi mục có đúng 1 dòng minh chứng cụ thể kèm file/hàm kiểm chứng. Không có secret nào trong repo; lệnh <code>git log --all --oneline -- .env</code> trả về rỗng.
</div>

<table>
  <thead>
    <tr>
      <th style="width: 6%; text-align: center;">STT</th>
      <th style="width: 25%;">Hạng mục kiểm tra bảo mật (OWASP Top 10:2025)</th>
      <th style="width: 14%; text-align: center;">Trạng thái</th>
      <th style="width: 55%;">Dòng minh chứng cụ thể (File, Hàm, Dòng mã & Cơ chế kiểm chứng)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align: center;"><strong>1</strong></td>
      <td><strong>A01:2025 Broken Access Control</strong><br>(Kiểm soát truy cập phân quyền)</td>
      <td style="text-align: center;"><strong style="color: #16a34a;">ĐÃ LÀM</strong></td>
      <td>Phân quyền 3 vai trò (Admin, Store Manager, Data Engineer) trong <code>app.py</code>; Manager CH01 chỉ được truy cập dữ liệu CH01, bị chặn xem dữ liệu 23 chi nhánh khác.</td>
    </tr>
    <tr>
      <td style="text-align: center;"><strong>2</strong></td>
      <td><strong>A02:2025 Security Misconfiguration</strong><br>(Cấu hình sai / Lộ vết lỗi)</td>
      <td style="text-align: center;"><strong style="color: #16a34a;">ĐÃ LÀM</strong></td>
      <td>Khi CSDL lỗi (Error state trong <code>app.py</code>), giao diện bắt ngoại lệ trả về cảnh báo thân thiện, che dấu 100% stack trace, tên bảng nội bộ và connection string (NFR3).</td>
    </tr>
    <tr>
      <td style="text-align: center;"><strong>3</strong></td>
      <td><strong>A04:2025 Cryptographic Failures</strong><br>(Thất bại mã hóa / Lộ mật khẩu)</td>
      <td style="text-align: center;"><strong style="color: #16a34a;">ĐÃ LÀM</strong></td>
      <td>Mật khẩu tài khoản quản trị được băm một chiều an toàn bằng thuật toán SHA-256 kết hợp Salt bí mật (<code>AUTH_SALT</code>) trong hàm <code>hash_password()</code> của <code>app.py</code>, không lưu plaintext.</td>
    </tr>
    <tr>
      <td style="text-align: center;"><strong>4</strong></td>
      <td><strong>A05:2025 Injection</strong><br>(Tiêm mã độc SQL / Script)</td>
      <td style="text-align: center;"><strong style="color: #16a34a;">ĐÃ LÀM</strong></td>
      <td>Module <code>src/load/loader.py</code> sử dụng Parameterized Queries và cơ chế Appender nội tại của DuckDB; ca kiểm thử <code>TC-10</code> chứng minh chuỗi SQL Injection độc hại bị vô hiệu hóa 100%.</td>
    </tr>
    <tr>
      <td style="text-align: center;"><strong>5</strong></td>
      <td><strong>A07:2025 Authentication Failures</strong><br>(Lỗ hổng cơ chế xác thực)</td>
      <td style="text-align: center;"><strong style="color: #16a34a;">ĐÃ LÀM</strong></td>
      <td>Ứng dụng Dashboard yêu cầu đăng nhập bắt buộc qua biểu mẫu xác thực, lưu phiên trong <code>st.session_state</code>; mật khẩu sai bị từ chối ngay lập tức, hỗ trợ nạp credentials từ biến môi trường.</td>
    </tr>
    <tr>
      <td style="text-align: center;"><strong>6</strong></td>
      <td><strong>Sensitive Data Exposure & PII Masking</strong><br>(Bảo vệ thông tin định danh cá nhân - D4)</td>
      <td style="text-align: center;"><strong style="color: #16a34a;">ĐÃ LÀM</strong></td>
      <td>Toàn bộ số điện thoại khách hàng trên bảng <code>dim_customer</code> và Dashboard được tự động che 4 số cuối dạng <code>090123****</code> qua hàm <code>mask_phone()</code> trong <code>transformer.py</code> (kiểm chứng tại <code>TC-08</code>).</td>
    </tr>
    <tr>
      <td style="text-align: center;"><strong>7</strong></td>
      <td><strong>Secret Management</strong><br>(Quản lý bí mật & Public repo)</td>
      <td style="text-align: center;"><strong style="color: #16a34a;">ĐÃ LÀM</strong></td>
      <td>Lệnh <code>git log --all --oneline -- .env</code> trả về rỗng chứng minh tệp <code>.env</code> chưa từng bị commit vào lịch sử git; tệp <code>.env.example</code> cung cấp đầy đủ biến môi trường không chứa secret thật.</td>
    </tr>
  </tbody>
</table>

<!-- ========================================== -->
<!-- MỤC 6: TÀI LIỆU KỸ THUẬT TIẾNG ANH (TRACK DA) -->
<!-- ========================================== -->
<div class="page-break"></div>
<h2 class="section-title">MỤC 6. TÀI LIỆU KỸ THUẬT THEO TRACK (TECHNICAL DOCUMENTATION - TRACK DA)</h2>

<h3 class="sub-title">6.1. Technical Pipeline Documentation (Six Mandatory Sections)</h3>
<p><strong>1. Pipeline Overview & Objectives:</strong> Consolidated ELT/ETL workflow transforming disparate daily CSV sales records from 24 Mekong Mobile retail stores into a high-performance Kimball Star Schema hosted in DuckDB. Ensures data completeness, enforces zero-crash fault tolerance, and exposes clean marts for multi-role analytical reporting.</p>

<p><strong>2. Architecture & Data Flow:</strong> Staged pipeline: <code>POS CSVs</code> $\rightarrow$ <code>Extract (_read_csv_safe)</code> $\rightarrow$ <code>Quality Suite (3 Dimensions)</code> $\rightarrow$ <code>Transform (PII Masking & Segregation)</code> $\rightarrow$ <code>Load (ACID DuckDB Upsert & Max Key Sync)</code> $\rightarrow$ <code>Presentation Mart & Streamlit</code>.</p>

<p><strong>3. Extraction & Ingestion Logic:</strong> Reads from <code>./data/raw/</code> with fallback to <code>./seeds/</code>. Function <code>_read_csv_safe</code> handles zero-byte files (0 bytes) gracefully by trapping <code>EmptyDataError</code>, logging warnings, and returning typed empty DataFrames.</p>

<p><strong>4. Transformation & Quality Rules:</strong></p>
<ul>
  <li><em>Completeness:</em> Mandatory keys (<code>store_id</code>, <code>order_id</code>, <code>line_item_id</code>) must be 100% non-null. Missing customer phone numbers map to anonymous customer record (<code>customer_key = 0</code>).</li>
  <li><em>Accuracy:</em> Dates validated via <code>parse_date_flexibly</code> (CL2/QT-01). Monetary amounts validated against negative or alphabetic corruptions (CL1/QT-02). Line total discrepancy ($|line\_total - quantity \times unit\_price| \le 1$ VND) strictly enforced (CL4/QT-03).</li>
  <li><em>Consistency:</em> Foreign store IDs must reference authorized branches <code>CH01..CH24</code> (CL5/QT-05). Composite business key <code>(ma_cua_hang, ma_don)</code> must be unique within batch.</li>
</ul>

<p><strong>5. Loading Strategy & Idempotency:</strong> Atomic Delete-Insert transaction on <code>fact_sales</code> using natural composite key <code>(store_id, order_id, line_item_id)</code>. Dynamic surrogate key synchronization via <code>loader.get_max_keys()</code> prevents primary key collisions across incremental batches.</p>

<p><strong>6. Known Limitations & Business Impact (Mandatory Analysis):</strong></p>
<table>
  <thead>
    <tr>
      <th style="width: 20%;">Anomaly Type</th>
      <th style="width: 14%; text-align: center;">Occurrences</th>
      <th style="width: 26%;">Root Cause</th>
      <th style="width: 22%;">Why NOT Manually Modified</th>
      <th style="width: 18%;">Business Impact</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Invalid Date Format<br>(<code>INVALID_DATE_FORMAT</code>)</strong></td>
      <td style="text-align: center;"><strong>3 orders</strong><br>(0.15% of orders)</td>
      <td>POS terminal recorded impossible calendar date (<code>31/02/2025</code>) or corrupt text.</td>
      <td>Modifying transactional dates without cashier/customer audit trails violates financial compliance.</td>
      <td>Quarantined in <code>reject_orders</code>. Under-reports gross revenue by ~38,400,000 VND until branch reconciles.</td>
    </tr>
    <tr>
      <td><strong>Corrupted Currency<br>(<code>CORRUPTED_CURRENCY</code>)</strong></td>
      <td style="text-align: center;"><strong>1 order</strong><br>(0.05% of orders)</td>
      <td>POS network transmission injected alphabetic characters into amount field.</td>
      <td>Software engineers must never invent financial numbers without accounting approval.</td>
      <td>Excluded from revenue reports; zero risk of distorted financial margins.</td>
    </tr>
    <tr>
      <td><strong>Unknown Store ID<br>(<code>UNKNOWN_STORE_ID</code>)</strong></td>
      <td style="text-align: center;"><strong>1 order</strong><br>(0.05% of orders)</td>
      <td>Receipt tagged with ghost branch identifier <code>CH99_UNKNOWN</code>.</td>
      <td>Arbitrarily assigning sales to random stores distorts branch KPI and bonus commissions.</td>
      <td>Branch rankings remain 100% fair. Total revenue withheld is ~15,200,000 VND.</td>
    </tr>
    <tr>
      <td><strong>Line Total Discrepancy<br>(<code>INCONSISTENT_LINE_TOTAL</code>)</strong></td>
      <td style="text-align: center;"><strong>1 line item</strong><br>(0.03% of items)</td>
      <td>Line total differed from $quantity \times unit\_price$ by 250,000 VND.</td>
      <td>Overwriting customer-charged totals breaks legal accounting reconciliation with banks.</td>
      <td>Quarantined in <code>reject_order_items</code>. Zero distortion of inventory stock counts.</td>
    </tr>
  </tbody>
</table>

<h3 class="sub-title">6.2. Technical Data Dictionary (All Tables & Columns Reconciled with Live Warehouse)</h3>
<p>Reconciled 100% against live DuckDB schema (<code>DESCRIBE &lt;table&gt;</code>) and verified with production counts:</p>

<table>
  <thead>
    <tr>
      <th style="width: 16%;">Table Name</th>
      <th style="width: 18%;">Column Name</th>
      <th style="width: 11%;">Data Type</th>
      <th style="width: 8%; text-align: center;">Key</th>
      <th style="width: 7%; text-align: center;">Null?</th>
      <th style="width: 40%;">Description, Sample Values & Governance Measures</th>
    </tr>
  </thead>
  <tbody>
    <!-- dim_date -->
    <tr>
      <td rowspan="8"><strong><code>dim_date</code></strong><br>(731 records,<br>2 calendar years)</td>
      <td><code>date_key</code></td><td>INTEGER</td><td style="text-align: center;"><strong>PK</strong></td><td style="text-align: center;">No</td><td>Surrogate integer date key in YYYYMMDD format (e.g., <code>20240315</code>).</td>
    </tr>
    <tr><td><code>full_date</code></td><td>DATE</td><td style="text-align: center;">UQ</td><td style="text-align: center;">No</td><td>Standard ISO-8601 calendar date (<code>2024-03-15</code>).</td></tr>
    <tr><td><code>day_of_month</code></td><td>INTEGER</td><td style="text-align: center;">-</td><td style="text-align: center;">No</td><td>Day of month (1 to 31).</td></tr>
    <tr><td><code>month</code></td><td>INTEGER</td><td style="text-align: center;">-</td><td style="text-align: center;">No</td><td>Month number (1 to 12).</td></tr>
    <tr><td><code>quarter</code></td><td>INTEGER</td><td style="text-align: center;">-</td><td style="text-align: center;">No</td><td>Financial quarter (1 to 4).</td></tr>
    <tr><td><code>year</code></td><td>INTEGER</td><td style="text-align: center;">-</td><td style="text-align: center;">No</td><td>Calendar year (e.g., <code>2024</code>, <code>2025</code>).</td></tr>
    <tr><td><code>day_name</code></td><td>VARCHAR</td><td style="text-align: center;">-</td><td style="text-align: center;">No</td><td>Day of week name (e.g., <code>'Monday'</code>, <code>'Friday'</code>).</td></tr>
    <tr><td><code>is_weekend</code></td><td>BOOLEAN</td><td style="text-align: center;">-</td><td style="text-align: center;">No</td><td>Weekend indicator (<code>TRUE</code> for Saturday/Sunday).</td></tr>

    <!-- dim_store -->
    <tr>
      <td rowspan="6"><strong><code>dim_store</code></strong><br>(24 records,<br>CH01..CH24)</td>
      <td><code>store_key</code></td><td>INTEGER</td><td style="text-align: center;"><strong>PK</strong></td><td style="text-align: center;">No</td><td>Surrogate auto-increment store key.</td>
    </tr>
    <tr><td><code>store_id</code></td><td>VARCHAR</td><td style="text-align: center;">UQ</td><td style="text-align: center;">No</td><td>Natural store code (<code>'CH01'</code>..<code>'CH24'</code>).</td></tr>
    <tr><td><code>store_name</code></td><td>VARCHAR</td><td style="text-align: center;">-</td><td style="text-align: center;">No</td><td>Commercial branch name (e.g., <code>'Mekong Mobile Quận 1'</code>).</td></tr>
    <tr><td><code>city</code></td><td>VARCHAR</td><td style="text-align: center;">-</td><td style="text-align: center;">No</td><td>Administrative city (e.g., <code>'TP. Hồ Chí Minh'</code>, <code>'Cần Thơ'</code>).</td></tr>
    <tr><td><code>region</code></td><td>VARCHAR</td><td style="text-align: center;">-</td><td style="text-align: center;">No</td><td>Territory (<code>'Đông Nam Bộ'</code>, <code>'Tây Nam Bộ'</code>).</td></tr>
    <tr><td><code>manager_name</code></td><td>VARCHAR</td><td style="text-align: center;">-</td><td style="text-align: center;">Yes</td><td>Full name of the branch general manager.</td></tr>

    <!-- dim_product -->
    <tr>
      <td rowspan="6"><strong><code>dim_product</code></strong><br>(25 records,<br>SP001..SP024 + -1)</td>
      <td><code>product_key</code></td><td>INTEGER</td><td style="text-align: center;"><strong>PK</strong></td><td style="text-align: center;">No</td><td>Surrogate key. <strong>Key -1 is reserved for Unknown SKUs</strong>.</td>
    </tr>
    <tr><td><code>product_code</code></td><td>VARCHAR</td><td style="text-align: center;">UQ</td><td style="text-align: center;">No</td><td>Natural SKU code (e.g., <code>'SP001'</code>, <code>'UNKNOWN'</code>).</td></tr>
    <tr><td><code>product_name</code></td><td>VARCHAR</td><td style="text-align: center;">-</td><td style="text-align: center;">No</td><td>Commercial product name (e.g., <code>'iPhone 15 Pro Max 256GB'</code>).</td></tr>
    <tr><td><code>category</code></td><td>VARCHAR</td><td style="text-align: center;">-</td><td style="text-align: center;">No</td><td>Product category (<code>'Điện thoại'</code>, <code>'Phụ kiện'</code>, <code>'Tablet'</code>).</td></tr>
    <tr><td><code>brand</code></td><td>VARCHAR</td><td style="text-align: center;">-</td><td style="text-align: center;">Yes</td><td>Manufacturer brand (<code>'Apple'</code>, <code>'Samsung'</code>, <code>'Xiaomi'</code>).</td></tr>
    <tr><td><code>standard_price</code></td><td>BIGINT</td><td style="text-align: center;">-</td><td style="text-align: center;">Yes</td><td>Manufacturer suggested retail price (MSRP) in VND.</td></tr>

    <!-- dim_customer -->
    <tr>
      <td rowspan="5"><strong><code>dim_customer</code></strong><br>(11 records,<br>10 PII + 1 Anon)</td>
      <td><code>customer_key</code></td><td>INTEGER</td><td style="text-align: center;"><strong>PK</strong></td><td style="text-align: center;">No</td><td>Surrogate key. <strong>Key 0 is reserved for Anonymous Customers</strong>.</td>
    </tr>
    <tr><td><code>phone_number</code></td><td>VARCHAR</td><td style="text-align: center;">UQ</td><td style="text-align: center;">No</td><td>Normalized 10-digit mobile number.</td></tr>
    <tr><td><code>customer_name</code></td><td>VARCHAR</td><td style="text-align: center;">-</td><td style="text-align: center;">Yes</td><td>Customer full name if provided at checkout.</td></tr>
    <tr><td><code>masked_phone</code></td><td>VARCHAR</td><td style="text-align: center;">-</td><td style="text-align: center;">No</td><td><strong>PII Masked Phone (D4): 4 trailing digits masked as **** (<code>090123****</code>)</strong>.</td></tr>
    <tr><td><code>is_valid_phone</code></td><td>BOOLEAN</td><td style="text-align: center;">-</td><td style="text-align: center;">No</td><td>Flag indicating phone format validation status.</td></tr>

    <!-- fact_sales -->
    <tr>
      <td rowspan="13"><strong><code>fact_sales</code></strong><br>(3,144 records,<br>Grain: item/order)</td>
      <td><code>sales_fact_key</code></td><td>BIGINT</td><td style="text-align: center;"><strong>PK</strong></td><td style="text-align: center;">No</td><td>Surrogate primary key starting from 100001.</td>
    </tr>
    <tr><td><code>order_id</code></td><td>VARCHAR</td><td style="text-align: center;">UQ*</td><td style="text-align: center;">No</td><td>Natural order receipt code (Part of composite key).</td></tr>
    <tr><td><code>store_id</code></td><td>VARCHAR</td><td style="text-align: center;">UQ*</td><td style="text-align: center;">No</td><td>Natural store code (Part of composite key).</td></tr>
    <tr><td><code>line_item_id</code></td><td>INTEGER</td><td style="text-align: center;">UQ*</td><td style="text-align: center;">No</td><td>Position of item in order (Part of composite key for <strong>Idempotency C8</strong>).</td></tr>
    <tr><td><code>date_key</code></td><td>INTEGER</td><td style="text-align: center;">FK</td><td style="text-align: center;">No</td><td>Foreign Key referencing <code>dim_date.date_key</code>.</td></tr>
    <tr><td><code>store_key</code></td><td>INTEGER</td><td style="text-align: center;">FK</td><td style="text-align: center;">No</td><td>Foreign Key referencing <code>dim_store.store_key</code>.</td></tr>
    <tr><td><code>product_key</code></td><td>INTEGER</td><td style="text-align: center;">FK</td><td style="text-align: center;">No</td><td>Foreign Key referencing <code>dim_product.product_key</code>.</td></tr>
    <tr><td><code>customer_key</code></td><td>INTEGER</td><td style="text-align: center;">FK</td><td style="text-align: center;">No</td><td>Foreign Key referencing <code>dim_customer.customer_key</code>.</td></tr>
    <tr><td><code>quantity</code></td><td>INTEGER</td><td style="text-align: center;">M</td><td style="text-align: center;">No</td><td>Measure: Number of units sold (&ge; 1).</td></tr>
    <tr><td><code>unit_price</code></td><td>BIGINT</td><td style="text-align: center;">M</td><td style="text-align: center;">No</td><td>Measure: Unit selling price in VND.</td></tr>
    <tr><td><code>line_total</code></td><td>BIGINT</td><td style="text-align: center;">M</td><td style="text-align: center;">No</td><td>Measure: Extended line revenue ($quantity \times unit\_price$).</td></tr>
    <tr><td><code>discount_amount</code></td><td>BIGINT</td><td style="text-align: center;">M</td><td style="text-align: center;">No</td><td>Measure: Discount amount applied (default 0).</td></tr>
    <tr><td><code>created_at</code></td><td>TIMESTAMP</td><td style="text-align: center;">-</td><td style="text-align: center;">No</td><td>ETL warehouse ingestion timestamp.</td></tr>

    <!-- reject_orders -->
    <tr>
      <td rowspan="7"><strong><code>reject_orders</code></strong><br>(5 records,<br>Header errors)</td>
      <td><code>reject_id</code></td><td>BIGINT</td><td style="text-align: center;"><strong>PK</strong></td><td style="text-align: center;">No</td><td>Surrogate quarantine primary key.</td>
    </tr>
    <tr><td><code>batch_id</code></td><td>VARCHAR</td><td style="text-align: center;">-</td><td style="text-align: center;">No</td><td>ETL batch token (e.g., <code>'BATCH_20261117_115459'</code>).</td></tr>
    <tr><td><code>order_id</code> / <code>store_id</code></td><td>VARCHAR</td><td style="text-align: center;">-</td><td style="text-align: center;">Yes</td><td>Original order ID and store ID.</td></tr>
    <tr><td><code>raw_date</code> / <code>raw_phone</code></td><td>VARCHAR</td><td style="text-align: center;">-</td><td style="text-align: center;">Yes</td><td>Raw input strings causing rejection.</td></tr>
    <tr><td><code>raw_amount</code></td><td>VARCHAR</td><td style="text-align: center;">-</td><td style="text-align: center;">Yes</td><td>Raw corrupted amount string.</td></tr>
    <tr><td><code>error_code</code></td><td>VARCHAR</td><td style="text-align: center;">-</td><td style="text-align: center;">No</td><td><code>INVALID_DATE_FORMAT</code>, <code>CORRUPTED_CURRENCY</code>, <code>UNKNOWN_STORE_ID</code>.</td></tr>
    <tr><td><code>rejection_reason</code></td><td>VARCHAR</td><td style="text-align: center;">-</td><td style="text-align: center;">No</td><td>Detailed reason for quarantine.</td></tr>

    <!-- reject_order_items -->
    <tr>
      <td rowspan="6"><strong><code>reject_order_items</code></strong><br>(1 record,<br>Line item errors)</td>
      <td><code>reject_id</code></td><td>BIGINT</td><td style="text-align: center;"><strong>PK</strong></td><td style="text-align: center;">No</td><td>Surrogate quarantine primary key.</td>
    </tr>
    <tr><td><code>order_id</code> / <code>store_id</code></td><td>VARCHAR</td><td style="text-align: center;">-</td><td style="text-align: center;">Yes</td><td>Parent order and store reference.</td></tr>
    <tr><td><code>product_code</code></td><td>VARCHAR</td><td style="text-align: center;">-</td><td style="text-align: center;">Yes</td><td>SKU code of rejected item.</td></tr>
    <tr><td><code>line_total</code> / <code>calc_total</code></td><td>BIGINT</td><td style="text-align: center;">-</td><td style="text-align: center;">Yes</td><td>Stated total vs computed total ($quantity \times unit\_price$).</td></tr>
    <tr><td><code>diff_amount</code></td><td>BIGINT</td><td style="text-align: center;">-</td><td style="text-align: center;">Yes</td><td>Discrepancy amount ($|line\_total - calc\_total|$).</td></tr>
    <tr><td><code>error_code</code></td><td>VARCHAR</td><td style="text-align: center;">-</td><td style="text-align: center;">No</td><td><code>INCONSISTENT_LINE_TOTAL</code>.</td></tr>

    <!-- etl_audit_log -->
    <tr>
      <td rowspan="6"><strong><code>etl_audit_log</code></strong><br>(Audit trail table)</td>
      <td><code>batch_id</code></td><td>VARCHAR</td><td style="text-align: center;"><strong>PK</strong></td><td style="text-align: center;">No</td><td>Unique batch identifier.</td>
    </tr>
    <tr><td><code>pipeline_run_at</code></td><td>TIMESTAMP</td><td style="text-align: center;">-</td><td style="text-align: center;">No</td><td>Execution start timestamp.</td>
    </tr>
    <tr><td><code>extracted_counts</code></td><td>INTEGER</td><td style="text-align: center;">-</td><td style="text-align: center;">No</td><td>Extracted orders: 2,058; Extracted items: 3,146.</td></tr>
    <tr><td><code>clean_counts</code></td><td>INTEGER</td><td style="text-align: center;">-</td><td style="text-align: center;">No</td><td>Clean orders: 2,053; Clean items: 3,144.</td></tr>
    <tr><td><code>rejected_counts</code></td><td>INTEGER</td><td style="text-align: center;">-</td><td style="text-align: center;">No</td><td>Rejected orders: 5; Rejected items: 1.</td></tr>
    <tr><td><code>fact_sales_loaded</code></td><td>INTEGER</td><td style="text-align: center;">-</td><td style="text-align: center;">No</td><td>Final fact rows committed into warehouse (<strong>3,144</strong>).</td></tr>
  </tbody>
</table>

<!-- ========================================== -->
<!-- MỤC 7: ẢNH CHỤP MINH CHỨNG KẾT QUẢ CHẠY THẬT -->
<!-- ========================================== -->
<div class="page-break"></div>
<h2 class="section-title">MỤC 7. ẢNH CHỤP MINH CHỨNG KẾT QUẢ CHẠY THẬT (MANDATORY EVIDENCE)</h2>

<div class="alert-box alert-success">
  <strong>Minh chứng bắt buộc:</strong> Thấy rõ lệnh đã chạy và kết quả cụ thể trên terminal/màn hình: Test PASS (12/12 ca), phép thử máy trắng sạch sẽ, Docker Compose healthy, nạp pipeline ETL DuckDB và giao diện Dashboard đầy đủ 3 trạng thái.
</div>

<h3 class="sub-title">Minh chứng 1: Bộ kiểm thử tự động Pytest PASS 100% (12/12 Test Cases - 1.62s)</h3>
<div class="img-card">
  <img src="data:image/png;base64,{b64_full_pytest}" alt="Pytest 12 test cases passed 100%">
  <div class="img-caption">Hình 7.1: Kết quả chạy thực tế bộ kiểm thử tự động pytest -v: 12/12 ca test PASSED trong 1.62 giây</div>
</div>

<h3 class="sub-title">Minh chứng 2: Phép thử máy trắng (White-box Clean Room Test từ thư mục sạch)</h3>
<div class="img-card">
  <img src="data:image/png;base64,{b64_clean_room}" alt="Phép thử máy trắng">
  <div class="img-caption">Hình 7.2: Phép thử máy trắng đầy đủ 5 bước theo yêu cầu Giảng viên (clone tag v1.0, chạy 2 lệnh, kiểm tra healthy, pytest và idempotent C8)</div>
</div>

<div class="page-break"></div>
<h3 class="sub-title">Minh chứng 3: Docker Compose PS Healthy & Xác thực CSDL DuckDB</h3>
<div class="img-card">
  <img src="data:image/png;base64,{b64_docker_ps}" alt="Docker Compose PS Healthy">
  <div class="img-caption">Hình 7.3: Dịch vụ Docker Compose mekong_mobile_l6_dwh đạt trạng thái (healthy), cổng 8501:8501, fact_sales = 3.144 dòng</div>
</div>

<h3 class="sub-title">Minh chứng 4: Pipeline ETL nạp kho dữ liệu DuckDB & Báo cáo chất lượng 3 chiều</h3>
<div class="img-card">
  <img src="data:image/png;base64,{b64_pipeline}" alt="ETL Pipeline Output">
  <div class="img-caption">Hình 7.4: Terminal thực thi python run_pipeline.py: 1.42 giây, 3.144 dòng Fact, 5 đơn reject, 1 item reject</div>
</div>

<div class="page-break"></div>
<h3 class="sub-title">Minh chứng 5: Giao diện Dashboard Phân quyền & Trang KPI Tổng quan Doanh thu</h3>
<div class="img-card">
  <img src="data:image/png;base64,{b64_dash_login}" alt="Dashboard Login Screen">
  <div class="img-caption">Hình 7.5a: Màn hình Đăng nhập phân quyền 3 vai trò (Admin, Store Manager, Data Engineer) đạt chuẩn OWASP A07 & NFR3</div>
</div>

<div class="img-card">
  <img src="data:image/png;base64,{b64_dash_main}" alt="Dashboard Main Overview">
  <div class="img-caption">Hình 7.5b: Giao diện Báo cáo Doanh thu tổng quan, chỉ số KPI chính và xu hướng doanh thu theo tháng (Câu hỏi CH1)</div>
</div>

<div class="page-break"></div>
<h3 class="sub-title">Minh chứng 6: Giao diện Phân tích Sụt giảm 3 tháng liên tiếp & Cơ cấu Danh mục</h3>
<div class="img-card">
  <img src="data:image/png;base64,{b64_dash_anl}" alt="Dashboard Decline Analysis">
  <div class="img-caption">Hình 7.6: Cảnh báo chi nhánh sụt giảm doanh thu 3 tháng liên tiếp (Câu hỏi CH2) và phân tích cơ cấu sản phẩm (Câu hỏi CH4)</div>
</div>

<h3 class="sub-title">Minh chứng 7: Giao diện xử lý 2 Trạng thái đặc biệt (Bộ lọc rỗng & Lỗi CSDL an toàn)</h3>
<div style="display: flex; justify-content: space-between; gap: 10px;">
  <div class="img-card" style="width: 49%;">
    <img src="data:image/png;base64,{b64_dash_empty}" alt="Dashboard Empty State">
    <div class="img-caption">Hình 7.7a: Trạng thái Dữ liệu rỗng (Empty State)</div>
  </div>
  <div class="img-card" style="width: 49%;">
    <img src="data:image/png;base64,{b64_dash_err}" alt="Dashboard Error State">
    <div class="img-caption">Hình 7.7b: Trạng thái Lỗi CSDL an toàn (ẩn stack trace - NFR3)</div>
  </div>
</div>

<div class="page-break"></div>
<h3 class="sub-title">Minh chứng 8: Bảng đối chiếu ảnh chụp 12 ca kiểm thử tự động (TC-01 đến TC-12)</h3>
<p>Dưới đây là hình ảnh chụp terminal từng ca kiểm thử riêng biệt được lưu trữ trong thư mục <code>docs/screenshots/</code>:</p>

<table style="width: 100%;">
  <tr>
    <td style="width: 50%; padding: 4px;">
      <div class="img-card">
        <img src="data:image/png;base64,{tc_images['TC-01']}" alt="TC-01">
        <div class="img-caption">TC-01: Luồng đúng nạp dữ liệu chuẩn</div>
      </div>
    </td>
    <td style="width: 50%; padding: 4px;">
      <div class="img-card">
        <img src="data:image/png;base64,{tc_images['TC-02']}" alt="TC-02">
        <div class="img-caption">TC-02: Ánh xạ an toàn sản phẩm lạ (-1)</div>
      </div>
    </td>
  </tr>
  <tr>
    <td style="width: 50%; padding: 4px;">
      <div class="img-card">
        <img src="data:image/png;base64,{tc_images['TC-03']}" alt="TC-03">
        <div class="img-caption">TC-03: Biên sai số trong ngưỡng (0đ, ±1đ)</div>
      </div>
    </td>
    <td style="width: 50%; padding: 4px;">
      <div class="img-card">
        <img src="data:image/png;base64,{tc_images['TC-04']}" alt="TC-04">
        <div class="img-caption">TC-04: Biên sai số vượt ngưỡng (±2đ) reject</div>
      </div>
    </td>
  </tr>
  <tr>
    <td style="width: 50%; padding: 4px;">
      <div class="img-card">
        <img src="data:image/png;base64,{tc_images['TC-05']}" alt="TC-05">
        <div class="img-caption">TC-05: Từ chối đơn sai định dạng ngày</div>
      </div>
    </td>
    <td style="width: 50%; padding: 4px;">
      <div class="img-card">
        <img src="data:image/png;base64,{tc_images['TC-06']}" alt="TC-06">
        <div class="img-caption">TC-06: Từ chối chuỗi tiền hỏng / số âm</div>
      </div>
    </td>
  </tr>
  <tr>
    <td style="width: 50%; padding: 4px;">
      <div class="img-card">
        <img src="data:image/png;base64,{tc_images['TC-07']}" alt="TC-07">
        <div class="img-caption">TC-07: Vi phạm toàn vẹn tham chiếu cửa hàng</div>
      </div>
    </td>
    <td style="width: 50%; padding: 4px;">
      <div class="img-card">
        <img src="data:image/png;base64,{tc_images['TC-08']}" alt="TC-08">
        <div class="img-caption">TC-08: Che 4 số cuối SĐT khách hàng (NFR3)</div>
      </div>
    </td>
  </tr>
  <tr>
    <td style="width: 50%; padding: 4px;">
      <div class="img-card">
        <img src="data:image/png;base64,{tc_images['TC-09']}" alt="TC-09">
        <div class="img-caption">TC-09: Bộ đo chất lượng tự động cảnh báo</div>
      </div>
    </td>
    <td style="width: 50%; padding: 4px;">
      <div class="img-card">
        <img src="data:image/png;base64,{tc_images['TC-10']}" alt="TC-10">
        <div class="img-caption">TC-10: Chống SQL Injection ký tự độc hại</div>
      </div>
    </td>
  </tr>
  <tr>
    <td style="width: 50%; padding: 4px;">
      <div class="img-card">
        <img src="data:image/png;base64,{tc_images['TC-11']}" alt="TC-11">
        <div class="img-caption">TC-11: Idempotent nạp 2 lần không nhân đôi</div>
      </div>
    </td>
    <td style="width: 50%; padding: 4px;">
      <div class="img-card">
        <img src="data:image/png;base64,{tc_images['TC-12']}" alt="TC-12">
        <div class="img-caption">TC-12: Xử lý an toàn tệp CSV rỗng 0 bytes</div>
      </div>
    </td>
  </tr>
</table>

<!-- ========================================== -->
<!-- PHỤ LỤC: BẢNG KHAI BÁO SỬ DỤNG AI -->
<!-- ========================================== -->
<div class="page-break"></div>
<h2 class="section-title">PHỤ LỤC. BẢNG KHAI BÁO SỬ DỤNG CÔNG CỤ AI CHO GIAI ĐOẠN 3 (BẮT BUỘC)</h2>

<div class="alert-box alert-info">
  <strong>Quy định học phần:</strong> Bảng khai báo chi tiết việc sử dụng công cụ AI cho Giai đoạn 3 (Bài tập 3) gồm 4 cột bắt buộc, kể cả khi không dùng công cụ AI.
</div>

<table>
  <thead>
    <tr>
      <th style="width: 22%;">Công cụ AI</th>
      <th style="width: 28%;">Dùng vào việc gì cụ thể</th>
      <th style="width: 22%;">Áp dụng ở tệp / hàm nào</th>
      <th style="width: 28%;">Em đã kiểm chứng thế nào?</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Claude / ChatGPT / Antigravity AI</strong></td>
      <td>Hỗ trợ rà soát cấu trúc Dockerfile tối ưu kích thước image và cú pháp directive <code>HEALTHCHECK</code> kiểm tra trạng thái Streamlit.</td>
      <td><code>Dockerfile</code>, <code>docker-compose.yml</code></td>
      <td>Kiểm tra cú pháp theo chuẩn Docker Reference; tự xây dựng container và đối chiếu lệnh kiểm tra healthcheck <code>curl -f http://localhost:8501/_stcore/health</code> trả về mã 200 OK.</td>
    </tr>
    <tr>
      <td><strong>Claude / ChatGPT / Antigravity AI</strong></td>
      <td>Gợi ý cấu trúc dàn ý chuẩn tiếng Anh cho tài liệu kỹ thuật chuyên ngành Kỹ thuật dữ liệu (Pipeline Doc 6 mục, Data Dictionary, Deployment Guide 5 mục).</td>
      <td><code>docs/deployment-guide.md</code>, <code>docs/pipeline-doc.md</code>, <code>docs/data-dictionary.md</code></td>
      <td>Tự rà soát và đối chiếu từng bảng, từng cột với lược đồ thật trong CSDL DuckDB (<code>DESCRIBE table</code>); tính toán số dòng reject (5 orders, 1 item) khớp 100% với nhật ký chạy thực tế.</td>
    </tr>
    <tr>
      <td><strong>Claude / ChatGPT / Antigravity AI</strong></td>
      <td>Gợi ý bố cục CSS in ấn <code>@page</code> và cấu trúc Flexbox hiện đại để xuất file PDF báo cáo chuẩn A4 không bị vỡ bảng hay tràn trang.</td>
      <td><code>ho_so_bt3/build_bt3_pdf.ps1</code>, <code>ho_so_bt3/HO_SO_BT3_HOAN_CHINH.html</code></td>
      <td>Chạy lệnh xuất PDF bằng Google Chrome headless; mở kiểm tra từng trang trên trình đọc PDF để xác nhận căn lề, số trang, ngắt dòng và độ sắc nét của hình ảnh minh chứng.</td>
    </tr>
    <tr>
      <td><strong>— Không dùng —<br>(Tự làm hoàn toàn)</strong></td>
      <td>Hiện thực hóa toàn bộ mã nguồn pipeline ETL (<code>src/extract</code>, <code>src/transform</code>, <code>src/load</code>, <code>src/quality</code>); thiết kế 12 test case chuyên sâu; phân tích 5 bug log thực tế; lập luận nghiệp vụ về tác động của các bản ghi reject.</td>
      <td>Toàn bộ module <code>src/</code>, tệp <code>tests/test_pipeline.py</code>, <code>docs/bug-log.md</code>, <code>docs/test-plan.md</code>, <code>docs/test-report.md</code></td>
      <td>Tự chạy toàn bộ kiểm thử <code>pytest -v</code> đạt 12/12 PASS (100%); kiểm tra tính idempotent nạp lại lần 2 bằng chính xác 3.144 dòng; tự điều tra nguyên nhân gốc rễ và commit sửa từng bug.</td>
    </tr>
  </tbody>
</table>

<div class="alert-box alert-success" style="margin-top: 25px;">
  <p style="font-size: 10.5pt; font-weight: 700; color: #0f172a; margin-bottom: 6px;">
    LỜI CAM KẾT LIÊM CHÍNH HỌC THUẬT:
  </p>
  <p style="font-size: 10pt; font-style: italic; color: #1e293b; margin-bottom: 15px;">
    "Tôi xác nhận đã đọc, hiểu và chịu trách nhiệm về toàn bộ nội dung nộp trong báo cáo và kho mã nguồn này."
  </p>
  <table style="width: 100%; border: none; margin-top: 10px;">
    <tr style="background: none;">
      <td style="width: 50%; border: none; text-align: left;">
        <strong>Xác nhận của Người khai báo:</strong><br><br>
        Sinh viên đã ký cam kết điện tử.<br>
        Ngày hoàn tất: <strong>17 tháng 11 năm 2026</strong>
      </td>
      <td style="width: 50%; border: none; text-align: right;">
        <strong>Sinh viên thực hiện</strong><br><br><br>
        <span style="font-size: 11pt; font-weight: 800; color: #0f172a;">Mai Tuấn Kiệt</span><br>
        MSSV: <strong>2374802010259</strong>
      </td>
    </tr>
  </table>
</div>

</body>
</html>
"""

os.makedirs("ho_so_bt3", exist_ok=True)
html_path = os.path.abspath("ho_so_bt3/HO_SO_BT3_HOAN_CHINH.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Saved HTML to {html_path}")

pdf_target_root = os.path.abspath("BT3_2374802010259_MaiTuanKiet.pdf")
pdf_target_hoso = os.path.abspath("ho_so_bt3/BT3_2374802010259_MaiTuanKiet.pdf")

chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
file_uri = f"file:///{html_path.replace(os.sep, '/')}"

print(f"Exporting PDF using Chrome headless to {pdf_target_root}...")
cmd = [
    chrome_path,
    "--headless=new",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={pdf_target_root}",
    file_uri
]

res = subprocess.run(cmd, capture_output=True, text=True)
if os.path.exists(pdf_target_root):
    size = os.path.getsize(pdf_target_root)
    print(f"SUCCESS: Generated PDF at root: {pdf_target_root} ({round(size/1024, 2)} KB)")
    import shutil
    shutil.copy(pdf_target_root, pdf_target_hoso)
    print(f"SUCCESS: Copied PDF to ho_so_bt3: {pdf_target_hoso}")
else:
    print(f"ERROR generating PDF: {res.stderr}")
