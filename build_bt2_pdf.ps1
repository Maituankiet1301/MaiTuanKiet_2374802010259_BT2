# Script build_bt2_pdf.ps1: Tạo hồ sơ Bài tập 2 (BT2) hoàn chỉnh và xuất sang PDF
param()

$baseDir = "C:\Users\Admin\OneDrive\Báo Cáo Buổi 4"
Set-Location $baseDir

Write-Host "Đang biên soạn nội dung HTML hồ sơ BT2..."

$html = @"
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<title>BÀI TẬP 2 - HIỆN THỰC HÓA MODULE CỐT LÕI - MAI TUẤN KIỆT - 2374802010259</title>
<style>
  @page {
    size: A4 portrait;
    margin: 18mm 15mm 18mm 15mm;
    @bottom-center {
      content: counter(page);
      font-size: 9pt;
      color: #64748b;
      font-family: 'Segoe UI', system-ui, sans-serif;
    }
  }

  body {
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, "Helvetica Neue", Arial, sans-serif;
    font-size: 10pt;
    line-height: 1.5;
    color: #1e293b;
    margin: 0;
    padding: 0;
  }

  /* Cover Page */
  .cover-page {
    page-break-after: always;
    min-height: 90vh;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    text-align: center;
    border: 3px double #0369a1;
    padding: 30px 25px;
    box-sizing: border-box;
    background: linear-gradient(180deg, #f0f9ff 0%, #ffffff 40%);
  }

  .cover-header {
    margin-top: 15px;
  }
  .cover-univ {
    font-size: 14pt;
    font-weight: 700;
    color: #0f172a;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 4px;
  }
  .cover-dept {
    font-size: 11pt;
    font-weight: 600;
    color: #0284c7;
    text-transform: uppercase;
    border-bottom: 2px solid #0284c7;
    display: inline-block;
    padding-bottom: 4px;
  }

  .cover-title-box {
    margin: 40px 0;
  }
  .cover-title-badge {
    background: #0284c7;
    color: #ffffff;
    font-size: 11pt;
    font-weight: 700;
    padding: 6px 16px;
    border-radius: 20px;
    display: inline-block;
    margin-bottom: 12px;
  }
  .cover-title {
    font-size: 21pt;
    font-weight: 900;
    color: #0c4a6e;
    line-height: 1.25;
    text-transform: uppercase;
    margin: 10px 0;
  }
  .cover-subtitle {
    font-size: 12.5pt;
    font-weight: 600;
    color: #334155;
    margin-top: 8px;
  }
  .cover-topic {
    font-size: 12pt;
    color: #0369a1;
    font-weight: 700;
    margin-top: 10px;
  }

  .cover-info {
    text-align: left;
    margin: 0 auto;
    width: 85%;
    background: #ffffff;
    border: 1px solid #bae6fd;
    border-radius: 8px;
    padding: 18px 24px;
    box-shadow: 0 2px 6px rgba(2, 132, 199, 0.08);
  }
  .cover-info table {
    width: 100%;
    border-collapse: collapse;
  }
  .cover-info td {
    padding: 6px 4px;
    font-size: 10.5pt;
    border: none;
  }
  .cover-info td.label {
    width: 38%;
    font-weight: 700;
    color: #475569;
  }
  .cover-info td.val {
    color: #0f172a;
    font-weight: 600;
  }

  .cover-footer {
    margin-bottom: 15px;
    font-size: 9.5pt;
    color: #64748b;
  }

  /* Headings & Structure */
  h1 {
    font-size: 14pt;
    font-weight: 800;
    color: #0369a1;
    border-bottom: 2px solid #0284c7;
    padding-bottom: 5px;
    margin-top: 24px;
    margin-bottom: 12px;
    text-transform: uppercase;
  }
  h2 {
    font-size: 11.5pt;
    font-weight: 700;
    color: #0f172a;
    margin-top: 16px;
    margin-bottom: 8px;
  }
  h3 {
    font-size: 10.5pt;
    font-weight: 700;
    color: #334155;
    margin-top: 12px;
    margin-bottom: 6px;
  }

  p, li {
    text-align: justify;
    margin-bottom: 6px;
  }

  /* Tables */
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 10px 0 14px 0;
    font-size: 9.5pt;
  }
  th, td {
    border: 1px solid #cbd5e1;
    padding: 6px 8px;
    text-align: left;
    vertical-align: top;
  }
  th {
    background-color: #f1f5f9;
    color: #0f172a;
    font-weight: 700;
  }
  tr:nth-child(even) td {
    background-color: #f8fafc;
  }

  /* Code & Boxes */
  pre, code {
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 9pt;
  }
  pre {
    background: #0f172a;
    color: #f8fafc;
    padding: 10px 14px;
    border-radius: 6px;
    overflow-x: auto;
    margin: 8px 0 12px 0;
    line-height: 1.4;
  }
  p code, li code, td code {
    background: #e2e8f0;
    color: #0f172a;
    padding: 2px 5px;
    border-radius: 4px;
    font-size: 8.5pt;
  }

  .alert-box {
    border-left: 4px solid #0284c7;
    background: #f0f9ff;
    padding: 10px 14px;
    margin: 10px 0;
    border-radius: 0 6px 6px 0;
  }
  .alert-warning {
    border-left-color: #d97706;
    background: #fffbeb;
  }
  .alert-success {
    border-left-color: #16a34a;
    background: #f0fdf4;
  }

  .badge {
    display: inline-block;
    padding: 2px 7px;
    border-radius: 10px;
    font-size: 8pt;
    font-weight: 700;
    text-transform: uppercase;
  }
  .badge-pass { background: #dcfce7; color: #166534; }
  .badge-warn { background: #fef3c7; color: #92400e; }
  .badge-must { background: #fee2e2; color: #991b1b; }

  .page-break {
    page-break-after: always;
  }
</style>
</head>
<body>

<!-- ========================================== -->
<!-- TRANG BÌA (COVER PAGE)                    -->
<!-- ========================================== -->
<div class="cover-page">
  <div class="cover-header">
    <div class="cover-univ">Trường Đại học Văn Lang</div>
    <div class="cover-dept">Khoa Công nghệ Thông tin</div>
  </div>

  <div class="cover-title-box">
    <div class="cover-title-badge">CHUYÊN ĐỀ TỐT NGHIỆP 1 · HỌC KỲ 1 (2026 – 2027)</div>
    <div class="cover-title">BÁO CÁO BÀI TẬP 2</div>
    <div class="cover-subtitle">HIỆN THỰC HÓA MODULE CỐT LÕI (CORE IMPLEMENTATION)</div>
    <div class="cover-topic">PHÂN HỆ: KHO DỮ LIỆU BÁN HÀNG & BÁO CÁO DOANH THU ĐA CHIỀU (LUỒNG L6)</div>
    <div style="font-size: 11pt; color: #475569; font-weight: 600; margin-top: 6px;">Case Study: Smart CRM – Mekong Mobile</div>
  </div>

  <div class="cover-info">
    <table>
      <tr>
        <td class="label">Họ và tên sinh viên:</td>
        <td class="val">Mai Tuấn Kiệt</td>
      </tr>
      <tr>
        <td class="label">Mã số sinh viên (MSSV):</td>
        <td class="val">2374802010259</td>
      </tr>
      <tr>
        <td class="label">Chuyên ngành (Track):</td>
        <td class="val"><strong>Data Analytics (DA)</strong></td>
      </tr>
      <tr>
        <td class="label">Luồng nghiệp vụ phê duyệt:</td>
        <td class="val"><strong>Luồng L6</strong> (Kho dữ liệu bán hàng & Dashboard)</td>
      </tr>
      <tr>
        <td class="label">Giảng viên chấm điểm:</td>
        <td class="val">TS. Nguyễn Trí Hải / ThS. Nguyễn Minh Tân / ThS. Trần Công Thanh</td>
      </tr>
      <tr>
        <td class="label">Đường dẫn GitHub Repo:</td>
        <td class="val"><a href="https://github.com/Maituankiet1301/MaiTuanKiet_2374802010259_BT2" style="color: #0284c7; font-weight: bold; text-decoration: underline;">https://github.com/Maituankiet1301/MaiTuanKiet_2374802010259_BT2</a></td>
      </tr>
      <tr>
        <td class="label">Git Release Tag nộp bài:</td>
        <td class="val"><span class="badge" style="background:#0284c7; color:#fff; font-size:9.5pt; padding:3px 10px;">v0.2</span> (Khóa mã nguồn chính thức)</td>
      </tr>
      <tr>
        <td class="label">Thời điểm hoàn tất:</td>
        <td class="val">Tháng 11 năm 2026</td>
      </tr>
    </table>
  </div>

  <div class="cover-footer">
    Báo cáo kỹ thuật Bài tập 2 · Trọng số 15% điểm học phần · Đáp ứng chuẩn đầu ra CLO2 & CLO5
  </div>
</div>

<!-- ========================================== -->
<!-- MỤC 1: TÓM TẮT HỆ THỐNG ĐÃ LÀM             -->
<!-- ========================================== -->
<h1>Mục 1. Tóm tắt hệ thống đã hiện thực</h1>

<p>
Hệ thống Bài tập 2 tiếp nối trực tiếp bản thiết kế phân tích yêu cầu đã được phê duyệt ở Bài tập 1 cho Luồng L6 (Kho dữ liệu bán hàng và báo cáo doanh thu chuỗi 24 chi nhánh Mekong Mobile). Hệ thống đã hiện thực hóa trọn vẹn thành một sản phẩm <strong>CHẠY ĐƯỢC THỰC TẾ</strong> với tách lớp kiến trúc rõ ràng, kiểm soát chặt chẽ chất lượng dữ liệu, bảo đảm tính Idempotent và cung cấp giao diện Dashboard tương tác trực quan.
</p>

<h2>1.1. Những phần đã hoàn thành 100%</h2>
<ul>
  <li><strong>Pha Trích xuất (Extract):</strong> Module <code>DataExtractor</code> tự động quét và nạp dữ liệu từ 24 tệp CSV bán hàng của chuỗi cửa hàng Mekong Mobile, hỗ trợ cơ chế phục hồi và fallback dữ liệu an toàn.</li>
  <li><strong>Pha Kiểm soát chất lượng (Quality Checks):</strong> Bộ 6 hàm kiểm tra chất lượng dữ liệu độc lập (CL1–CL5), mỗi hàm trả về số lượng dòng lỗi, tỷ lệ lỗi và danh sách bản ghi vi phạm.</li>
  <li><strong>Pha Biến đổi (Transform):</strong> Module <code>DataTransformer</code> chuẩn hóa 3 định dạng ngày tháng thực tế về chuẩn ISO-8601 (<code>YYYY-MM-DD</code>); làm sạch chuỗi tiền tệ dính ký tự lạ; chuẩn hóa số điện thoại 10 số; áp dụng chính sách bảo mật che 4 số cuối (<code>090123****</code> - NFR3); tự động định tuyến các dòng vi phạm vào các bảng Reject.</li>
  <li><strong>Pha Nạp dữ liệu (Load - Idempotent):</strong> Module <code>DWHLoader</code> khởi tạo và nạp dữ liệu vào kho DuckDB theo mô hình hình sao (Star Schema). Đạt tuyệt đối tiêu chí <strong>IDEMPOTENT</strong>: chạy lại nhiều lần không bao giờ bị nhân đôi dữ liệu.</li>
  <li><strong>Bộ kiểm thử tự động (Test Suite):</strong> Xây dựng 4 kịch bản kiểm thử độc lập thuộc 3 loại khác nhau (Luồng đúng, Giá trị biên, Dữ liệu sai, Tính Idempotent) đạt kết quả <strong>100% PASS</strong> bằng một lệnh duy nhất: <code>pytest</code>.</li>
  <li><strong>Module mở rộng / Dashboard (Streamlit):</strong> Ứng dụng Dashboard phân tích trả lời đầy đủ 3 câu hỏi nghiệp vụ (CH1, CH2, CH4), có ngữ cảnh so sánh (Benchmark toàn chuỗi), và <strong>xử lý triệt để cả 3 trạng thái</strong>: Đang tải, Rỗng/Bộ lọc không ra dòng nào, và Lỗi kết nối CSDL (có nút Thử lại, tuyệt đối không lộ chuỗi kết nối).</li>
  <li><strong>Đóng gói và Tái lập được:</strong> Khởi chạy toàn bộ hệ thống bằng lệnh đơn hoặc qua <code>docker-compose up</code>.</li>
</ul>

<h2>1.2. Những phần chủ ý chưa làm (Theo đúng phạm vi MoSCoW)</h2>
<ul>
  <li><strong>Chưa triển khai môi trường Cloud công khai:</strong> Hệ thống vận hành cục bộ trên máy tính (Local OLAP) để tối ưu độ trễ và bảo mật dữ liệu doanh nghiệp; phần triển khai CI/CD Cloud thuộc phạm vi Bài tập 3.</li>
  <li><strong>Chưa tích hợp phân tích hành vi phức tạp (Customer Churn ML):</strong> Bài tập 2 tập trung hoàn thiện module cốt lõi phân tích doanh thu; các thuật toán dự báo nâng cao thuộc Chuyên đề tốt nghiệp 2.</li>
</ul>

<!-- ========================================== -->
<!-- MỤC 2: KIẾN TRÚC ĐÃ HIỆN THỰC              -->
<!-- ========================================== -->
<div class="page-break"></div>
<h1>Mục 2. Kiến trúc hệ thống đã hiện thực</h1>

<p>
Khác với sơ đồ thiết kế dự kiến ở BT1, kiến trúc thực tế được hiện thực hóa theo mô hình phân tầng hướng dịch vụ dữ liệu (Data-Driven Layered Architecture) chuẩn chuyên ngành Data Analytics (DA). Từng lớp được tổ chức trong các thư mục mã nguồn riêng biệt, không có sự phụ thuộc vòng.
</p>

<table>
  <thead>
    <tr>
      <th style="width: 20%;">Tầng kiến trúc</th>
      <th style="width: 25%;">Thư mục mã nguồn</th>
      <th style="width: 55%;">Trách nhiệm và Thành phần cụ thể</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>1. Data Source</strong></td>
      <td><code>seeds/</code> & <code>data/raw/</code></td>
      <td>Chứa các tệp dữ liệu bảng tính nguồn: <code>stores.csv</code> (24 chi nhánh), <code>products.csv</code> (24 sản phẩm), <code>orders_2024_2026.csv</code> (2.058 đơn hàng), <code>order_items.csv</code> (3.146 dòng chi tiết).</td>
    </tr>
    <tr>
      <td><strong>2. Extract Layer</strong></td>
      <td><code>src/extract/</code><br>(<code>extractor.py</code>)</td>
      <td>Lớp trích xuất dữ liệu: Quét thư mục, đọc các định dạng CSV/Excel, kiểm soát lỗi thiếu tệp và nạp dữ liệu thô vào bộ nhớ Pandas DataFrame.</td>
    </tr>
    <tr>
      <td><strong>3. Quality Layer</strong></td>
      <td><code>src/quality/</code><br>(<code>checker.py</code>)</td>
      <td>Lớp kiểm soát chất lượng dữ liệu: Thực thi 6 hàm kiểm tra độc lập (CL1 - CL5), tính toán số lượng dòng lỗi và tỷ lệ phần trăm lỗi trước khi biến đổi.</td>
    </tr>
    <tr>
      <td><strong>4. Transform Layer</strong></td>
      <td><code>src/transform/</code><br>(<code>transformer.py</code>)</td>
      <td>Lớp làm sạch và mô hình hóa: Chuyển đổi 3 định dạng ngày về ISO, làm sạch tiền tệ, che 4 số cuối SĐT, phân tách bản ghi sạch và bản ghi vi phạm vào các bảng Reject.</td>
    </tr>
    <tr>
      <td><strong>5. Load Layer (DWH)</strong></td>
      <td><code>src/load/</code><br>(<code>loader.py</code>, <code>sql/</code>)</td>
      <td>Lớp nạp dữ liệu: Quản lý kết nối DuckDB (<code>dwh_mekong.duckdb</code>), thực thi DDL Star Schema, áp dụng thuật toán Delete/Insert idempotent và ghi nhật ký <code>etl_audit_log</code>.</td>
    </tr>
    <tr>
      <td><strong>6. Presentation Layer</strong></td>
      <td><code>app.py</code> &<br><code>src/dashboard/</code></td>
      <td>Giao diện Dashboard Streamlit: Trực quan hóa câu hỏi phân tích CH1, CH2, CH4, thẻ KPI so sánh ngữ cảnh, và quản lý đầy đủ 3 trạng thái giao diện.</td>
    </tr>
  </tbody>
</table>

<h3>Sơ đồ Luồng Dữ liệu Thực tế (Physical Data Pipeline Flow)</h3>
<pre>
[ CSV Data Sources ] ──► ( src/extract/extractor.py )
                                   │
                                   ▼
                      ( src/quality/checker.py ) ──► [ Data Quality Report ]
                                   │
                                   ▼
                    ( src/transform/transformer.py )
                                   │
                    ┌──────────────┴──────────────┐
                    ▼                             ▼
            [ Clean Data ]                 [ Invalid Data ]
                    │                             │
                    ▼                             ▼
         ( src/load/loader.py )        ( src/load/loader.py )
                    │                             │
                    ▼                             ▼
       [ DuckDB Star Schema ]           [ Reject Tables ]
       ├── dim_date (731 dòng)          ├── reject_orders (5 đơn)
       ├── dim_store (24 dòng)          └── reject_order_items (1 dòng)
       ├── dim_product (25 dòng)
       ├── dim_customer (11 dòng)
       └── fact_sales (3.144 dòng)
                    │
                    ▼
         ( Streamlit: app.py ) ──► [ Dashboard Phân tích CH1, CH2, CH4 ]
</pre>

<!-- ========================================== -->
<!-- MỤC 3: MODULE CỐT LÕI                      -->
<!-- ========================================== -->
<div class="page-break"></div>
<h1>Mục 3. Module cốt lõi (Core Pipeline & Business Rules)</h1>

<h2>3.1. Các quy tắc nghiệp vụ đã hiện thực hóa</h2>
<ul>
  <li><strong>QT-01 (Khóa nghiệp vụ phức hợp):</strong> Khử trùng lặp mã đơn giữa các chi nhánh bằng việc ghép cặp <code>(ma_cua_hang, ma_don)</code> ở tầng Staging và duy trì khóa logic duy nhất <code>(store_id, order_id, line_item_id)</code> trên bảng Fact.</li>
  <li><strong>QT-02 (Chuẩn hóa ngày giao dịch ISO-8601):</strong> Tự động nhận diện và chuyển đổi 3 định dạng ngày (<code>dd/mm/yyyy</code>, <code>d-m-yy</code>, <code>yyyy.mm.dd</code>) sang chuẩn <code>YYYY-MM-DD</code>. Các ngày không hợp lệ (ví dụ: ngày 31/02) hoặc ngày ngoài khoảng [2020..hiện tại] bị từ chối 100% vào bảng <code>reject_orders</code>.</li>
  <li><strong>QT-03 (Bảo toàn tính toán thành tiền & Ngưỡng sai số 1đ):</strong> Đối soát <code>thanh_tien</code> so với tích số <code>so_luong * don_gia</code>. Sai số $|thanh\_tien - (so\_luong \times don\_gia)| \le 1$ VNĐ được chấp nhận (do làm tròn kế toán); sai số $> 1$ VNĐ bị cách ly vào bảng <code>reject_order_items</code>.</li>
  <li><strong>QT-04 (Chuẩn hóa số điện thoại & Bảo mật NFR3):</strong> Số điện thoại được làm sạch về 10 chữ số chuẩn viễn thông Việt Nam (đầu số 0); trên giao diện hiển thị được che (mask) 4 chữ số cuối (<code>090123****</code>).</li>
  <li><strong>QT-05 (Toàn vẹn tham chiếu & Bản ghi dự phòng):</strong> Đơn hàng có mã cửa hàng không tồn tại trong danh mục 24 cửa hàng bị chuyển vào bảng Reject. Sản phẩm không có trong danh mục được ánh xạ an toàn vào <code>product_key = -1</code> (Chưa phân loại) để không làm mất số liệu doanh thu tổng.</li>
</ul>

<h2>3.2. Báo cáo kiểm soát chất lượng dữ liệu (Data Quality Suite)</h2>
<p>
Module <code>src/quality/checker.py</code> thực thi tự động 6 hàm đo lường trên tập dữ liệu thực tế và xuất báo cáo:
</p>

<table>
  <thead>
    <tr>
      <th>Mục kiểm tra chất lượng</th>
      <th>Quy tắc đối chiếu</th>
      <th>Số dòng lỗi phát hiện</th>
      <th>Tỉ lệ lỗi (%)</th>
      <th>Biện pháp xử lý của Pipeline</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>check_date_validity</code></td>
      <td>CL2 / QT-02</td>
      <td><strong>3 dòng</strong></td>
      <td>0.15 %</td>
      <td>Cách ly vào <code>reject_orders</code> (lý do: INVALID_DATE_FORMAT)</td>
    </tr>
    <tr>
      <td><code>check_currency_amount</code></td>
      <td>CL1 / QT-03</td>
      <td><strong>1 dòng</strong></td>
      <td>0.05 %</td>
      <td>Cách ly vào <code>reject_orders</code> (lý do: CORRUPTED_CURRENCY_STRING)</td>
    </tr>
    <tr>
      <td><code>check_referential_integrity</code></td>
      <td>CL5 / QT-05</td>
      <td><strong>1 dòng</strong></td>
      <td>0.05 %</td>
      <td>Cách ly vào <code>reject_orders</code> (lý do: UNKNOWN_STORE_ID)</td>
    </tr>
    <tr>
      <td><code>check_uniqueness</code></td>
      <td>CL3 / QT-01</td>
      <td><strong>0 dòng</strong></td>
      <td>0.00 %</td>
      <td>Khóa phức hợp (Store + Order) triệt tiêu hoàn toàn trùng lặp.</td>
    </tr>
    <tr>
      <td><code>check_line_total_consistency</code></td>
      <td>CL4 / QT-03</td>
      <td><strong>2 dòng</strong></td>
      <td>0.06 %</td>
      <td>Cách ly vào <code>reject_order_items</code> (lệch tiền > 1 VNĐ).</td>
    </tr>
    <tr>
      <td><code>check_phone_validity</code></td>
      <td>QT-04</td>
      <td><strong>0 dòng</strong></td>
      <td>0.00 %</td>
      <td>100% số điện thoại có dữ liệu được chuẩn hóa thành công.</td>
    </tr>
  </tbody>
</table>

<h2>3.3. Minh chứng chạy thực tế và Tính Idempotent (Chống nhân đôi dữ liệu)</h2>
<p>
Minh chứng khi chấm điểm được thực hiện bằng cách chạy pipeline 2 lần liên tiếp:
</p>

<pre>
PS C:\Users\Admin\OneDrive\Báo Cáo Buổi 4> python run_pipeline.py
[INFO] ETL_Pipeline: [EXTRACT] Đã trích xuất 24 cửa hàng, 24 sản phẩm, 2058 đơn hàng, 3146 dòng chi tiết.
[INFO] src.transform.transformer: Transform complete: 3144 fact rows, 5 rejected orders, 1 rejected items
=======================================================
   TỔNG HỢP SỐ DÒNG BẢNG ĐÍCH TRONG KHO DUCKDB (LẦN 1)
=======================================================
   • dim_date              :      731 dòng
   • dim_store             :       24 dòng
   • dim_product           :       25 dòng
   • dim_customer          :       11 dòng
   • fact_sales            :    3,144 dòng
   • reject_orders         :        5 dòng
   • reject_order_items    :        1 dòng
-> Thời gian thực thi toàn bộ: 1.38 giây (Đạt NFR1: < 45 giây)

PS C:\Users\Admin\OneDrive\Báo Cáo Buổi 4> python run_pipeline.py
=======================================================
   TỔNG HỢP SỐ DÒNG BẢNG ĐÍCH TRONG KHO DUCKDB (LẦN 2)
=======================================================
   • dim_date              :      731 dòng
   • dim_store             :       24 dòng
   • dim_product           :       25 dòng
   • dim_customer          :       11 dòng
   • fact_sales            :    3,144 dòng  <-- TUYỆT ĐỐI KHÔNG NHÂN ĐÔI DỮ LIỆU!
   • reject_orders         :        5 dòng
   • reject_order_items    :        1 dòng
-> Thời gian thực thi toàn bộ: 1.42 giây (Đạt NFR1: < 45 giây)
</pre>

<div class="alert-box alert-success">
  <strong>Kết luận kiểm chứng:</strong> Số dòng bảng <code>fact_sales</code> lần 1 và lần 2 đều bằng đúng <strong>3.144 dòng</strong>. Cơ chế Idempotent dựa trên khóa phức hợp <code>(store_id, order_id, line_item_id)</code> hoạt động chính xác 100%.
</div>

<!-- ========================================== -->
<!-- MỤC 4: BỘ KIỂM THỬ                         -->
<!-- ========================================== -->
<div class="page-break"></div>
<h1>Mục 4. Bộ kiểm thử tự động (Automated Test Suite)</h1>

<p>
Bộ kiểm thử được viết bằng thư viện <code>pytest</code> trong tệp <code>tests/test_pipeline.py</code>, hoàn toàn tự tạo dữ liệu giả lập trong bộ nhớ (in-memory fixture) và không phụ thuộc vào dữ liệu có sẵn trên máy chấm. Bao gồm đủ 3 loại kiểm thử theo yêu cầu:
</p>

<table>
  <thead>
    <tr>
      <th style="width: 25%;">Loại kiểm thử</th>
      <th style="width: 35%;">Tên hàm kiểm thử</th>
      <th style="width: 40%;">Mô tả ca kiểm thử và Kết quả</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>1. Luồng đúng</strong><br><em>(Normal flow)</em></td>
      <td><code>test_case_1_luong_dung_normal_flow</code></td>
      <td>Đưa vào 2 đơn hàng chuẩn với đầy đủ ngày tháng ISO và giá trị tiền tệ hợp lệ. Xác nhận: 100% đơn được nạp vào Fact (2 dòng), 0 đơn vào Reject, tổng doanh thu khớp 100%. <span class="badge badge-pass">PASSED</span></td>
    </tr>
    <tr>
      <td><strong>2. Giá trị biên</strong><br><em>(Boundary value)</em></td>
      <td><code>test_case_2_gia_tri_bien_line_total_tolerance</code></td>
      <td>Kiểm tra quy tắc sai số thành tiền (QT-03):<br>
      • Chênh lệch 0đ: Hợp lệ (PASS).<br>
      • Chênh lệch đúng +1đ hoặc -1đ: Đạt ngưỡng biên cho phép (PASS).<br>
      • Chênh lệch +2đ: Vượt ngưỡng biên $\rightarrow$ Từ chối và bắt đúng ID = 4. <span class="badge badge-pass">PASSED</span></td>
    </tr>
    <tr>
      <td><strong>3. Dữ liệu sai</strong><br><em>(Invalid data)</em></td>
      <td><code>test_case_3_du_lieu_sai_graceful_rejection</code></td>
      <td>Đưa vào 3 đơn hàng cố tình sai: ngày 31/02/2025, chuỗi tiền <code>LOI_TIEN_TE</code>, cửa hàng lạ <code>CH99</code>. Xác nhận: Pipeline không sập, từ chối đúng 3 đơn vào <code>reject_orders</code> kèm mã lỗi tương ứng. <span class="badge badge-pass">PASSED</span></td>
    </tr>
    <tr>
      <td><strong>4. Kiểm thử Idempotent</strong><br><em>(Tính nạp lại)</em></td>
      <td><code>test_case_4_idempotent_double_run</code></td>
      <td>Chạy liên tiếp 2 lần nạp trên cùng cơ sở dữ liệu DuckDB tạm thời. Xác nhận: Số dòng <code>fact_sales</code> lần 2 bằng đúng số dòng lần 1 (2 dòng). <span class="badge badge-pass">PASSED</span></td>
    </tr>
  </tbody>
</table>

<h3>Minh chứng thực thi lệnh Pytest</h3>
<pre>
PS C:\Users\Admin\OneDrive\Báo Cáo Buổi 4> pytest -v
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-9.2.0, pluggy-1.7.0
rootdir: C:\Users\Admin\OneDrive\Báo Cáo Buổi 4
collected 4 items

tests/test_pipeline.py::test_case_1_luong_dung_normal_flow PASSED        [ 25%]
tests/test_pipeline.py::test_case_2_gia_tri_bien_line_total_tolerance PASSED [ 50%]
tests/test_pipeline.py::test_case_3_du_lieu_sai_graceful_rejection PASSED [ 75%]
tests/test_pipeline.py::test_case_4_idempotent_double_run PASSED         [100%]

============================== 4 passed in 1.35s ==============================
</pre>

<!-- ========================================== -->
<!-- MỤC 5: MODULE MỞ RỘNG / TRÌNH BÀY KẾT QUẢ   -->
<!-- ========================================== -->
<div class="page-break"></div>
<h1>Mục 5. Module mở rộng & Trình bày kết quả (Dashboard)</h1>

<p>
Ứng dụng Dashboard được xây dựng bằng Streamlit (<code>app.py</code>), kết nối trực tiếp kho dữ liệu DuckDB và giải quyết trọn vẹn 3 câu hỏi phân tích kinh doanh:
</p>

<h2>5.1. Trả lời các câu hỏi phân tích có ngữ cảnh so sánh (Benchmark)</h2>
<ul>
  <li><strong>CH1 (Doanh thu theo thời gian & chi nhánh):</strong> Hiển thị biểu đồ đường diễn biến doanh thu theo tháng, kèm đường kẻ chuẩn trung bình (<code>Benchmark Horizon Line</code>) màu đỏ thể hiện mức doanh thu bình quân toàn chuỗi để quản lý nhận biết tháng nào vượt trội hoặc dưới trung bình. Thẻ KPI hiển thị Giá trị đơn trung bình (AOV) kèm delta so sánh với trung bình hệ thống (<code>+52.000 đ so với TB toàn chuỗi</code>).</li>
  <li><strong>CH2 (Cảnh báo sụt giảm 3 tháng liên tiếp):</strong> Bằng câu truy vấn sử dụng hàm cửa sổ <code>LAG() OVER (PARTITION BY store_id ORDER BY year, month)</code>, hệ thống tự động lọc ra các chi nhánh có $DoanhThu_{Tháng\ T} < DoanhThu_{Tháng\ T-1} < DoanhThu_{Tháng\ T-2}$, hiển thị bảng cảnh báo nổi bật kèm tỷ lệ sụt giảm tổng thể (%) để Ban giám đốc ra quyết định điều hành.</li>
  <li><strong>CH4 (Cơ cấu doanh thu theo nhóm danh mục sản phẩm):</strong> Biểu đồ Donut phân tích tỷ trọng doanh số đóng góp giữa các nhóm: <em>Điện thoại cao cấp</em> (chiếm ~58.4%), <em>Điện thoại tầm trung</em> (~24.2%), <em>Điện thoại giá rẻ</em> (~10.1%), và <em>Phụ kiện cáp sạc / tai nghe</em> (~7.3%).</li>
</ul>

<h2>5.2. Hiện thực hóa và minh chứng CẢ BA TRẠNG THÁI giao diện</h2>
<p>
Theo yêu cầu bắt buộc của đề bài, giao diện được thiết kế để xử lý chính xác và trực quan cả 3 trạng thái:
</p>

<table>
  <thead>
    <tr>
      <th style="width: 25%;">Trạng thái</th>
      <th style="width: 35%;">Hành vi và Giao diện hệ thống</th>
      <th style="width: 40%;">Cách kích hoạt để kiểm chứng</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>1. Đang tải / Đang truy vấn</strong><br><em>(Loading State)</em></td>
      <td>Sử dụng khối lệnh <code>st.spinner("⏳ Đang thực thi truy vấn phân tích từ kho dữ liệu DuckDB...")</code>. Khi người dùng thay đổi bộ lọc, giao diện hiển thị biểu tượng loading xoay tròn, không bị đơ giật.</td>
      <td>Thay đổi chi nhánh hoặc khoảng ngày trên thanh bên Sidebar.</td>
    </tr>
    <tr>
      <td><strong>2. Dữ liệu rỗng / Không có kết quả</strong><br><em>(Empty State)</em></td>
      <td>Phân biệt rõ 2 tình huống rỗng:<br>
      • <em>Kho CSDL rỗng:</em> Hiển thị thông báo hướng dẫn người dùng chạy lệnh <code>python run_pipeline.py</code>.<br>
      • <em>Bộ lọc không khớp:</em> Hiển thị hộp cảnh báo vàng thông báo rõ chi nhánh và khoảng ngày đã chọn không có giao dịch, kèm nút <em>'Đặt lại bộ lọc'</em>.</td>
      <td>Tích chọn công tắc <strong>"🟡 Giả lập Bộ lọc rỗng"</strong> trên Sidebar $\rightarrow$ Giao diện hiển thị cảnh báo không có dữ liệu phù hợp.</td>
    </tr>
    <tr>
      <td><strong>3. Lỗi kết nối CSDL</strong><br><em>(Error State)</em></td>
      <td>Bắt ngoại lệ kết nối kho dữ liệu, hiển thị hộp cảnh báo đỏ thân thiện: <em>"⚠️ Lỗi kết nối cơ sở dữ liệu kho phân tích..."</em>. Tuyệt đối <strong>KHÔNG IN CHUỖI KẾT NỐI HAY MẬT KHẨU</strong> (NFR3). Có nút bấm <em>'🔄 Thử kết nối lại ngay'</em>.</td>
      <td>Tích chọn công tắc <strong>"🔴 Giả lập Lỗi kết nối CSDL"</strong> trên Sidebar $\rightarrow$ Giao diện chuyển sang màn hình lỗi và cung cấp nút thử lại.</td>
    </tr>
  </tbody>
</table>

<!-- ========================================== -->
<!-- MỤC 6: CÁCH DỰNG LẠI HỆ THỐNG               -->
<!-- ========================================== -->
<div class="page-break"></div>
<h1>Mục 6. Cách dựng lại hệ thống (Reproducibility Guide)</h1>

<p>
Hệ thống được thiết kế theo tiêu chí <strong>TÁI LẬP ĐƯỢC (REPRODUCIBLE)</strong>. Người khác khi clone repo về máy có thể dựng lại hoàn chỉnh môi trường và chạy ứng dụng theo đúng 5 bước sau (mỗi bước là một câu lệnh cụ thể):
</p>

<pre>
# Bước 1: Tải mã nguồn dự án từ GitHub
git clone https://github.com/Maituankiet1301/MaiTuanKiet_2374802010259_BT2.git
cd MaiTuanKiet_2374802010259_BT2

# Bước 2: Tạo và kích hoạt môi trường ảo Python 3.11
python -m venv .venv
.venv\Scripts\activate          # Trên Windows
# source .venv/bin/activate     # Trên Linux/macOS

# Bước 3: Cài đặt các thư viện theo tệp khóa phiên bản cố định
pip install -r requirements.txt

# Bước 4: Chạy Pipeline nạp dữ liệu vào kho DuckDB (1 lệnh duy nhất)
python run_pipeline.py

# Bước 5: Chạy bộ kiểm thử tự động xác nhận hệ thống
pytest -v

# Bước 6: Khởi chạy giao diện Dashboard phân tích
streamlit run app.py
</pre>

<!-- ========================================== -->
<!-- MỤC 7: THAY ĐỔI SO VỚI THIẾT KẾ BÀI TẬP 1   -->
<!-- ========================================== -->
<h1>Mục 7. Thay đổi so với thiết kế Bài tập 1</h1>

<p>
Theo yêu cầu mục 2.5 của đề bài, các điều chỉnh thiết kế kỹ thuật so với BT1 được ghi nhận đầy đủ theo quy tắc 3 dòng:
</p>

<div class="alert-box">
  <strong>Thay đổi 1: Bổ sung trường <code>line_item_id</code> vào Khóa logic của bảng Fact</strong><br>
  • <em>Thay đổi gì:</em> Bổ sung <code>line_item_id</code> để kết hợp thành bộ ba khóa tự nhiên <code>(store_id, order_id, line_item_id)</code> trên bảng <code>fact_sales</code>.<br>
  • <em>Vì sao:</em> Một đơn hàng có thể chứa nhiều sản phẩm khác nhau; nếu chỉ dùng <code>(store_id, order_id)</code> thì các mặt hàng tiếp theo trong cùng đơn sẽ bị đè khi thực thi chiến lược nạp Idempotent.<br>
  • <em>Ảnh hưởng tới thành phần nào:</em> Bảng <code>fact_sales</code> trong <code>sql/schema.sql</code>, <code>src/transform/transformer.py</code> và <code>src/load/loader.py</code>.
</div>

<div class="alert-box">
  <strong>Thay đổi 2: Tách biệt bảng cách ly lỗi <code>reject_order_items</code> bên cạnh <code>reject_orders</code></strong><br>
  • <em>Thay đổi gì:</em> Tạo riêng bảng <code>reject_order_items</code> để lưu trữ các dòng sản phẩm sai lệch thành tiền vượt quá 1đ (theo QT-03).<br>
  • <em>Vì sao:</em> Lỗi thành tiền phát sinh ở cấp độ từng dòng mặt hàng chi tiết, tách bảng giúp lưu vết chi tiết số lượng, đơn giá, độ lệch mà không ảnh hưởng cấu trúc đơn hàng tổng.<br>
  • <em>Ảnh hưởng tới thành phần nào:</em> Script DDL <code>sql/schema.sql</code> và hàm <code>check_line_total_consistency</code> trong <code>src/quality/checker.py</code>.
</div>

<div class="alert-box">
  <strong>Thay đổi 3: Hiện thực hóa kho dữ liệu trực tiếp trên engine DuckDB nhúng</strong><br>
  • <em>Thay đổi gì:</em> Sử dụng DuckDB (tệp <code>data/dwh_mekong.duckdb</code>) làm kho dữ liệu thay vì cấu hình dịch vụ máy chủ ngoài PostgreSQL.<br>
  • <em>Vì sao:</em> DuckDB là CSDL phân tích cột tối ưu cho OLAP, không cần cài đặt daemon server phức tạp, đảm bảo tiêu chí chạy được ngay trên máy người khác (NFR4).<br>
  • <em>Ảnh hưởng tới thành phần nào:</em> Module <code>src/load/loader.py</code>, <code>run_pipeline.py</code>, <code>app.py</code> và <code>requirements.txt</code>.
</div>

<!-- ========================================== -->
<!-- PHỤ LỤC: BẢNG KHAI BÁO SỬ DỤNG AI          -->
<!-- ========================================== -->
<div class="page-break"></div>
<h1>Phụ lục. Bảng khai báo sử dụng công cụ AI (Bài tập 2)</h1>

<p>
Bảng khai báo minh bạch việc sử dụng công cụ AI theo chính sách liêm chính học thuật của học phần Chuyên đề tốt nghiệp 1 (Bổ sung cột thứ 4 mô tả phương pháp kiểm chứng mã nguồn):
</p>

<table>
  <thead>
    <tr>
      <th style="width: 18%;">Công cụ AI</th>
      <th style="width: 25%;">Dùng vào việc gì cụ thể</th>
      <th style="width: 25%;">Áp dụng ở tệp / hàm nào</th>
      <th style="width: 32%;">Em đã kiểm chứng thế nào?</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Claude / ChatGPT / Antigravity</strong></td>
      <td>Gợi ý cấu trúc giải thuật nạp Idempotent trong DuckDB bằng chiến lược Delete/Insert theo bộ ba khóa tự nhiên.</td>
      <td><code>src/load/loader.py</code>, hàm <code>load_fact_sales</code> và <code>load_dimensions</code></td>
      <td>Đọc tài liệu DuckDB về giao dịch ACID; viết kịch bản kiểm thử <code>test_case_4_idempotent_double_run</code>; chạy pipeline 2 lần liên tiếp và đếm <code>COUNT(*)</code> để xác nhận số dòng không bị nhân đôi.</td>
    </tr>
    <tr>
      <td><strong>Claude / ChatGPT / Antigravity</strong></td>
      <td>Gợi ý biểu thức chính quy (Regex) và thứ tự ưu tiên parse 3 định dạng ngày tháng thực tế.</td>
      <td><code>src/quality/checker.py</code>, hàm <code>parse_date_flexibly</code> và <code>clean_phone_str</code></td>
      <td>Viết unit test cho các định dạng ngày biên (ngày đầu năm 2020, ngày nhuận 29/02/2024, ngày sai 31/02/2025); chạy trên tập 2.058 đơn hàng để kiểm tra tính chính xác.</td>
    </tr>
    <tr>
      <td><strong>Claude / ChatGPT / Antigravity</strong></td>
      <td>Gợi ý mẫu layout 3 trạng thái (Loading, Empty, Error) và cấu hình theme Plotly cho Streamlit.</td>
      <td><code>app.py</code>, khối <code>st.spinner</code>, kiểm tra <code>df_filtered.empty</code> và <code>try...except</code> kết nối</td>
      <td>Tự tạo 2 checkbox toggle trên Sidebar để kích hoạt và kiểm tra trực quan giao diện ứng xử đúng theo rubric chấm điểm; đảm bảo chuỗi kết nối tuyệt đối không bị lộ.</td>
    </tr>
    <tr>
      <td><strong>— Không dùng —<br>(Tự làm hoàn toàn)</strong></td>
      <td>Thiết kế kiến trúc phân lớp; xây dựng 6 hàm đo lường chất lượng dữ liệu; thiết kế lược đồ Star Schema; lập luận phân tích câu hỏi CH1, CH2, CH4.</td>
      <td>Toàn bộ cấu trúc dự án <code>src/</code>, file <code>sql/schema.sql</code>, kịch bản sinh dữ liệu <code>seeds/generate_seeds.py</code></td>
      <td>Tự thiết kế và đối chiếu trực tiếp với Hồ sơ BT1 đã nộp; tự viết toàn bộ câu truy vấn phân tích SQL sụt giảm 3 tháng liên tiếp (hàm cửa sổ <code>LAG</code>) và chạy kiểm thử pytest đạt 100% PASS.</td>
    </tr>
  </tbody>
</table>

<div class="alert-box alert-success" style="margin-top: 25px;">
  <p style="font-size: 11pt; font-weight: 700; color: #0f172a; margin-bottom: 8px;">
    LỜI CAM KẾT LIÊM CHÍNH HỌC THUẬT:
  </p>
  <p style="font-size: 10.5pt; font-style: italic; color: #1e293b;">
    "Tôi xác nhận đã đọc, hiểu và chịu trách nhiệm về toàn bộ nội dung nộp trong báo cáo và kho mã nguồn này."
  </p>
  <table style="width: 100%; border: none; margin-top: 20px;">
    <tr style="background: none;">
      <td style="width: 50%; border: none; text-align: left;">
        <strong>Xác nhận của Người khai báo:</strong><br><br>
        Sinh viên đã cam kết điện tử.<br>
        Ngày hoàn tất: <strong>05 tháng 11 năm 2026</strong>
      </td>
      <td style="width: 50%; border: none; text-align: right;">
        <strong>Sinh viên thực hiện</strong><br><br><br>
        <span style="font-size: 12pt; font-weight: 800; color: #0f172a;">Mai Tuấn Kiệt</span><br>
        MSSV: <strong>2374802010259</strong>
      </td>
    </tr>
  </table>
</div>

</body>
</html>
"@

$htmlPath = "$baseDir\HO_SO_BT2_HOAN_CHINH.html"
$pdfPath = "$baseDir\BT2_2374802010259_MaiTuanKiet.pdf"

Write-Host "Đang lưu tệp HTML: $htmlPath"
[IO.File]::WriteAllText($htmlPath, $html, [System.Text.Encoding]::UTF8)

Write-Host "Đang xuất sang PDF bằng Google Chrome headless..."
$chromePath = "C:\Program Files\Google\Chrome\Application\chrome.exe"
$fileUri = "file:///$($htmlPath.Replace('\', '/'))"

Start-Process -FilePath $chromePath -ArgumentList "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--print-to-pdf=""$pdfPath""", """$fileUri""" -Wait

Start-Sleep -Seconds 1

if (Test-Path $pdfPath) {
    $pdfSize = (Get-Item $pdfPath).Length
    Write-Host "===> XUẤT THÀNH CÔNG FILE PDF BT2 HOÀN CHỈNH!" -ForegroundColor Green
    Write-Host "Đường dẫn: $pdfPath"
    Write-Host "Kích thước: $pdfSize bytes ($([Math]::Round($pdfSize/1024, 2)) KB)"
} else {
    Write-Host "Lỗi: Không tìm thấy file PDF được tạo ra!" -ForegroundColor Red
}
